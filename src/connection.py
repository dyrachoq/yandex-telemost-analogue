from fastapi import WebSocket


class Connection:
    def __init__(self):
        self.rooms: dict[str, list[WebSocket]] = {}

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        if room_id not in self.rooms:
            self.rooms[room_id] = []
        self.rooms[room_id].append(websocket)

        if len(self.rooms[room_id]) == 2:
            await websocket.send_json({"type": "init"})

    def disconnect(self, room_id: str, websocket: WebSocket):
        self.rooms[room_id].remove(websocket)

    async def broadcast(self, room_id: str, message: str, sender: WebSocket):
        for websocket in self.rooms[room_id]:
            if websocket == sender:
                continue
            await websocket.send_json(message)
