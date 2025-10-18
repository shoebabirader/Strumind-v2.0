"""
WebSocket manager for real-time collaboration
"""
from fastapi import WebSocket
from typing import Dict, List, Set
import json
import asyncio
from datetime import datetime


# SECURITY FIX: Use timezone-aware datetime
from app.core.datetime_utils import utc_now
class ConnectionManager:
    """Manages WebSocket connections for real-time collaboration"""
    
    def __init__(self):
        # project_id -> set of websocket connections
        self.active_connections: Dict[int, Set[WebSocket]] = {}
        # websocket -> user_id mapping
        self.connection_users: Dict[WebSocket, int] = {}
        # project_id -> current state
        self.project_states: Dict[int, dict] = {}
        
    async def connect(self, websocket: WebSocket, project_id: int, user_id: int):
        """Connect a user to a project room"""
        await websocket.accept()
        
        if project_id not in self.active_connections:
            self.active_connections[project_id] = set()
        
        self.active_connections[project_id].add(websocket)
        self.connection_users[websocket] = user_id
        
        # Send current project state to new user
        if project_id in self.project_states:
            await websocket.send_json({
                "type": "state_sync",
                "data": self.project_states[project_id],
                "timestamp": utc_now().isoformat()
            })
        
        # Notify others that user joined
        await self.broadcast_to_project(project_id, {
            "type": "user_joined",
            "user_id": user_id,
            "timestamp": utc_now().isoformat()
        }, exclude=websocket)
    
    def disconnect(self, websocket: WebSocket, project_id: int):
        """Disconnect a user from a project room"""
        if project_id in self.active_connections:
            self.active_connections[project_id].discard(websocket)
            if not self.active_connections[project_id]:
                del self.active_connections[project_id]
        
        user_id = self.connection_users.pop(websocket, None)
        
        # Notify others that user left
        if user_id:
            asyncio.create_task(self.broadcast_to_project(project_id, {
                "type": "user_left",
                "user_id": user_id,
                "timestamp": utc_now().isoformat()
            }))
    
    async def broadcast_to_project(self, project_id: int, message: dict, exclude: WebSocket = None):
        """Broadcast message to all users in a project"""
        if project_id not in self.active_connections:
            return
        
        disconnected = []
        for connection in self.active_connections[project_id]:
            if connection == exclude:
                continue
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for connection in disconnected:
            self.disconnect(connection, project_id)
    
    async def send_to_user(self, websocket: WebSocket, message: dict):
        """Send message to specific user"""
        try:
            await websocket.send_json(message)
        except Exception:
            pass
    
    async def update_project_state(self, project_id: int, state_update: dict, user_id: int):
        """Update project state and broadcast to all users"""
        if project_id not in self.project_states:
            self.project_states[project_id] = {}
        
        # Merge state update
        self.project_states[project_id].update(state_update)
        
        # Broadcast update
        await self.broadcast_to_project(project_id, {
            "type": "state_update",
            "data": state_update,
            "user_id": user_id,
            "timestamp": utc_now().isoformat()
        })
    
    async def send_analysis_progress(self, project_id: int, progress: dict):
        """Send analysis progress updates"""
        await self.broadcast_to_project(project_id, {
            "type": "analysis_progress",
            "data": progress,
            "timestamp": utc_now().isoformat()
        })
    
    async def send_cursor_position(self, project_id: int, user_id: int, position: dict, exclude: WebSocket = None):
        """Send cursor position for collaborative editing"""
        await self.broadcast_to_project(project_id, {
            "type": "cursor_move",
            "user_id": user_id,
            "position": position,
            "timestamp": utc_now().isoformat()
        }, exclude=exclude)
    
    def get_active_users(self, project_id: int) -> List[int]:
        """Get list of active users in a project"""
        if project_id not in self.active_connections:
            return []
        
        return [
            self.connection_users[ws]
            for ws in self.active_connections[project_id]
            if ws in self.connection_users
        ]


# Global connection manager instance
manager = ConnectionManager()
