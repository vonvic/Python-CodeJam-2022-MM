from dataclasses import dataclass, field
from datetime import datetime
from random import choice
from typing import Dict, List

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from string import ascii_letters, digits

app = FastAPI()

templates = Jinja2Templates(directory="static")

@dataclass
class User:
    name: str
    id: int
    current_room: "Room"
    connection: WebSocket

    async def send_message(self, message: str):
        self.connection.send_json(
            {
                "type": "message",
                "content": message
            }
        )

@dataclass
class Room:
    room_id: str
    users: List[User] = field(default_factory=list)
    owner: User = None
    messages: List[Dict] = field(default_factory=dict)
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        
        user_data = await websocket.receive_json()

        await websocket.send_json(
            {
                "type": "room_join_success",
                "room_id": self.room_id
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
        self.users.remove(list(filter(lambda x: x.client == websocket.client, self.users))[0])
        
        await self.send_all(
            {
                "type": "room_disconnect_success",
                "room_id": self.room_id,
                "time": datetime.utcnow().timestamp()
            }
        )
    
    async def send_all(self, message: object):
        for user in self.users:
            await user.send_message(message)

@dataclass
class ConnectionManager:
    rooms: List[Room] = field(default_factory=list)

    async def broadcast(self, message: object):
        for room in self.rooms:
            await room.send_all(message)
    
    async def locate_room(self, room_id: str):
        for i in self.rooms:
            if room_id == i.room_id:
                return i
        
        return None

manager = ConnectionManager()

# @app.get("/")
# async def home(request: Request):
#     return templates.TemplateResponse("index2.html", {"request": request})

@app.get("/ws/{room_id}/{client_id}")
async def chat_room(websocket: WebSocket, room_id: str, client_id: str):
    room = manager.locate_room(room_id=room_id)
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