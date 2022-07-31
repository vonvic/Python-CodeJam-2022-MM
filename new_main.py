from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates

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
        print(user_data)
        await websocket.send_json(
            {
                "type": "room_join_success",
                "room_id": self.room_id,
                "username": user_data["name"]
            }
        )

        await self.send_all(
            {
                "type": "user_join",
                "username": user_data["name"],
                "time": datetime.utcnow().timestamp()
            }
        )

        self.users.append(User(name=user_data["name"], id=user_data["id"], current_room=self, connection=websocket))

    async def disconnect(self, websocket: WebSocket):
        """Removes the user defined in `websocket` from the room."""
        user_to_remove: User = list(filter(lambda x: x.connection.client == websocket.client, self.users))[0]
        self.users.remove(user_to_remove)

        await self.send_all(
            {
                "type": "room_disconnect_success",
                "username": user_to_remove.name,
                "room_id": self.room_id,
                "time": datetime.utcnow().timestamp()
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

# @app.get("/")
# async def home(request: Request):
#     return templates.TemplateResponse("index2.html", {"request": request})


@app.websocket("/ws/{room_id}/{client_id}")
async def chat_room(websocket: WebSocket, room_id: str, client_id: str):
    """Todo (firestar): write docstring"""
    room = await manager.locate_room(room_id=room_id)
    user = await manager.locate_user(client_id=client_id)

    if user is not None and user.current_room != room:
        await user.current_room.disconnect(user.connection)

    if room is None:
        room = Room(room_id=room_id, users=[], messages=[])
        manager.rooms.append(room)

    await room.connect(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            if data["type"] == "message_sent":
                await room.send_all(data)

    except WebSocketDisconnect:
        await room.disconnect(websocket)
