from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from app.core.database import get_db
from app.models.project import Node

router = APIRouter()

class NodeCreate(BaseModel):
    project_id: int
    node_id: str
    x: float
    y: float
    z: float
    restraints: Optional[List[bool]] = [False, False, False, False, False, False]

class NodeUpdate(BaseModel):
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None
    restraints: Optional[List[bool]] = None

class NodeResponse(BaseModel):
    id: int
    project_id: int
    node_id: str
    x: float
    y: float
    z: float
    restraints: List[bool]
    
    class Config:
        from_attributes = True

@router.post("/create", response_model=NodeResponse)
def create_node(node: NodeCreate, db: Session = Depends(get_db)):
    """Create a new node"""
    try:
        db_node = Node(
            project_id=node.project_id,
            node_id=node.node_id,
            x=node.x,
            y=node.y,
            z=node.z,
            restraints=node.restraints
        )
        db.add(db_node)
        db.commit()
        db.refresh(db_node)
        return db_node
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/list/{project_id}", response_model=List[NodeResponse])
def list_nodes(project_id: int, db: Session = Depends(get_db)):
    """List all nodes for a project"""
    nodes = db.query(Node).filter(Node.project_id == project_id).all()
    return nodes

@router.get("/{node_id}", response_model=NodeResponse)
def get_node(node_id: int, db: Session = Depends(get_db)):
    """Get a specific node"""
    node = db.query(Node).filter(Node.id == node_id).first()
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return node

@router.put("/{node_id}", response_model=NodeResponse)
def update_node(node_id: int, node_update: NodeUpdate, db: Session = Depends(get_db)):
    """Update a node"""
    db_node = db.query(Node).filter(Node.id == node_id).first()
    if not db_node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    if node_update.x is not None:
        db_node.x = node_update.x
    if node_update.y is not None:
        db_node.y = node_update.y
    if node_update.z is not None:
        db_node.z = node_update.z
    if node_update.restraints is not None:
        db_node.restraints = node_update.restraints
    
    db.commit()
    db.refresh(db_node)
    return db_node

@router.delete("/{node_id}")
def delete_node(node_id: int, db: Session = Depends(get_db)):
    """Delete a node"""
    db_node = db.query(Node).filter(Node.id == node_id).first()
    if not db_node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    db.delete(db_node)
    db.commit()
    return {"status": "success", "message": "Node deleted"}
