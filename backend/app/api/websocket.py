"""
WebSocket endpoints for real-time collaboration
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from app.core.websocket_manager import manager
from app.core.security import decode_access_token
import json

router = APIRouter()


@router.websocket("/ws/projects/{project_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    project_id: int,
    token: str = Query(...)
):
    """
    WebSocket endpoint for real-time project collaboration
    
    Usage:
    ws://localhost:8000/api/ws/projects/1?token=YOUR_JWT_TOKEN
    
    Message Types:
    - state_update: Update project state
    - cursor_move: Send cursor position
    - chat: Send chat message
    - analysis_start: Notify analysis started
    - analysis_complete: Notify analysis completed
    """
    
    # Authenticate user
    try:
        token_data = decode_access_token(token)
        user_id = token_data.user_id
    except Exception:
        await websocket.close(code=1008, reason="Authentication failed")
        return
    
    # Connect user to project room
    await manager.connect(websocket, project_id, user_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            message_type = message.get("type")
            
            if message_type == "state_update":
                # Update project state
                await manager.update_project_state(
                    project_id,
                    message.get("data", {}),
                    user_id
                )
            
            elif message_type == "cursor_move":
                # Broadcast cursor position
                await manager.send_cursor_position(
                    project_id,
                    user_id,
                    message.get("position", {}),
                    exclude=websocket
                )
            
            elif message_type == "chat":
                # Broadcast chat message
                await manager.broadcast_to_project(project_id, {
                    "type": "chat",
                    "user_id": user_id,
                    "message": message.get("message", ""),
                    "timestamp": message.get("timestamp")
                })
            
            elif message_type == "analysis_start":
                # Notify analysis started
                await manager.broadcast_to_project(project_id, {
                    "type": "analysis_start",
                    "user_id": user_id,
                    "analysis_type": message.get("analysis_type")
                })
            
            elif message_type == "analysis_progress":
                # Send analysis progress
                await manager.send_analysis_progress(
                    project_id,
                    message.get("progress", {})
                )
            
            elif message_type == "ping":
                # Respond to ping
                await manager.send_to_user(websocket, {
                    "type": "pong",
                    "timestamp": message.get("timestamp")
                })
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, project_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket, project_id)


@router.get("/projects/{project_id}/active-users")
async def get_active_users(project_id: int):
    """Get list of currently active users in a project"""
    active_users = manager.get_active_users(project_id)
    return {
        "project_id": project_id,
        "active_users": active_users,
        "count": len(active_users)
    }
