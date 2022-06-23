from fastapi import WebSocket
from typing import List,Any

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def disconnectAll(self):
        self.active_connections = []
        
    async def broadcast(self, message: Any):
        for connection in self.active_connections:
            await connection.send_json(message)
