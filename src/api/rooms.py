from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from uuid import uuid4, UUID
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

from src.connection import Connection
from src.schemas.rooms import RoomCreateSchema,RoomGetSchema
from fastapi.responses import FileResponse
import os


router = APIRouter()


rooms = []

manager = Connection()

HTML_DIR = os.path.join(os.getcwd(), "frontend")

@router.get("/", summary="Главная страница")
async def get_index():
    return FileResponse(os.path.join(HTML_DIR, "index.html"))

@router.get("/room/{room_id}", summary="Страница комнаты")
async def get_room(room_id: str):
    return FileResponse(os.path.join(HTML_DIR, "room.html"))

@router.post("/rooms", summary="Создание комнаты", tags=["rooms"])
async def create_room(room: RoomCreateSchema):
    new_room = RoomGetSchema(id=uuid4(), name=room.name)
    rooms.append(new_room)
    return {"ok": new_room, "msg": "Room created!"}

@router.get("/rooms", summary="Показать все комнаты", tags=["rooms"])
def all_rooms() -> list[RoomGetSchema]:
    return rooms

@router.get("/rooms/{room_id}", summary="Конкретная комната", tags=["rooms"])
def get_room(room_id: UUID) -> RoomGetSchema:
    for room in rooms:
        if room.id == room_id:
            return room
    raise HTTPException(status_code=404, detail="Room not found")



@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await manager.connect(room_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast(room_id, data, websocket)
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
        await manager.broadcast(room_id, {"type": "user-left"}, websocket)
