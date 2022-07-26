from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates

from utils import utils

app = FastAPI()

templates = Jinja2Templates(directory="static")


@dataclass
class User:
    """User class to send messages to its `connection`."""

    name: str
    id: int
    current_room: "Room"
    connection: WebSocket

    async def send_message(self, message: object):
        """Sends `message` to its connection."""
        await self.connection.send_json(
            message
        )


@dataclass
class Room:
    """Room that hosts users as websocket connections."""

    room_id: str
    users: List[User] = field(default_factory=list)
    owner: User = None
    messages: List[Dict] = field(default_factory=dict)

    async def connect(self, websocket: WebSocket):
        """Connects the user defined `websocket` and sends a join to all other users in the room."""
        await websocket.accept()

        user_data = await websocket.receive_json()

        self.users.append(User(name=user_data["name"], id=user_data["id"], current_room=self, connection=websocket))

        await websocket.send_json(
            {
                "type": "room_join_success",
                "room_id": self.room_id,
                "username": user_data["name"],
                "users": [i.name for i in self.users]
            }
        )

        await self.send_all(
            {
                "type": "user_join",
                "username": user_data["name"],
                "time": datetime.utcnow().timestamp(),
                "users": [i.name for i in self.users]
            }
        )

    async def disconnect(self, websocket: WebSocket):
        """Removes the user defined in `websocket` from the room."""
        user_to_remove: User = list(filter(lambda x: x.connection.client == websocket.client, self.users))[0]
        self.users.remove(user_to_remove)

        await self.send_all(
            {
                "type": "room_disconnect_success",
                "username": user_to_remove.name,
                "room_id": self.room_id,
                "time": datetime.utcnow().timestamp(),
                "users": [i.name for i in self.users]
            }
        )

    async def send_all(self, message: object):
        """Sends `message` to all users in the room."""
        for user in self.users:
            await user.send_message(message)


@dataclass
class ConnectionManager:
    """Manager that holds a list of all the open rooms."""

    rooms: List[Room] = field(default_factory=list)

    async def broadcast(self, message: object):
        """Sends `message` to all the rooms."""
        for room in self.rooms:
            await room.send_all(message)

    async def locate_room(self, room_id: str):
        """Returns the room with id `room_id` from self.rooms."""
        for i in self.rooms:
            if room_id == i.room_id:
                return i

        return None

    async def locate_user(self, client_id: int):
        """Returns the user with id `client_id`."""
        for i in self.rooms:
            for user in i.users:
                if client_id == user.id:
                    return user

        return None


manager = ConnectionManager()


@app.websocket("/ws/{room_id}")
async def chat_room(websocket: WebSocket, room_id: str):
    """Puts user into proper room and relays messages between the clients in the same room"""
    room = await manager.locate_room(room_id=room_id)

    if room is None:
        room = Room(room_id=room_id, users=[], messages=[])
        manager.rooms.append(room)

    await room.connect(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            if data["type"] == "message_sent":
                data["content"] = utils.scramble_sentence(data["content"])
                room.messages.append({"user": data["username"], "content": data["content"]})
                await room.send_all(data)

    except WebSocketDisconnect:
        await room.disconnect(websocket)
        if len(room.users) == 0:
            manager.rooms.remove(room)
