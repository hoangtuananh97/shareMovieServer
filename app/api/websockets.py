from typing import List

from fastapi import APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        await websocket.send_text("Connection established")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            print("broadcast :", message)
            await connection.send_text(message)


websocketsManager = ConnectionManager()
router = APIRouter()


@router.websocket("")
async def websocket_endpoint(websocket: WebSocket):
    # TODO _: models.User = Depends(get_current_user)
    await websocketsManager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print("Received data:", data)
            await websocketsManager.broadcast(data)
    except WebSocketDisconnect:
        websocketsManager.disconnect(websocket)
        await websocketsManager.broadcast(f"Client disconnected")
