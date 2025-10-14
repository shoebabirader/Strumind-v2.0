from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime

router = APIRouter()

class Comment(BaseModel):
    id: int
    element_id: str
    user: str
    text: str
    timestamp: str

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, project_id: str):
        await websocket.accept()
        if project_id not in self.active_connections:
            self.active_connections[project_id] = []
        self.active_connections[project_id].append(websocket)
    
    def disconnect(self, websocket: WebSocket, project_id: str):
        self.active_connections[project_id].remove(websocket)
    
    async def broadcast(self, message: dict, project_id: str):
        for connection in self.active_connections.get(project_id, []):
            await connection.send_json(message)

manager = ConnectionManager()

@router.websocket("/ws/{project_id}")
async def websocket_endpoint(websocket: WebSocket, project_id: str):
    await manager.connect(websocket, project_id)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast(data, project_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, project_id)

@router.post("/comments/add")
def add_comment(comment: Comment):
    return {"status": "success", "comment": comment}

@router.get("/comments/{element_id}")
def get_comments(element_id: str):
    return {"comments": []}
