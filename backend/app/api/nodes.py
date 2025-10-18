from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError
from pydantic import BaseModel, field_validator, Field
from typing import List, Optional
import logging
from app.core.database import get_db
from app.models.project import Node
from app.core.validators import NodeValidator
from app.core.errors import (
    InvalidNodeError, DuplicateNodeError, ProjectNotFoundError,
    error_to_http_response
)

router = APIRouter()
logger = logging.getLogger(__name__)

class NodeCreate(BaseModel):
    project_id: int
    node_id: str
    x: float = Field(..., description="X coordinate (mm)")
    y: float = Field(..., description="Y coordinate (mm)")
    z: float = Field(..., description="Z coordinate (mm)")
    restraints: Optional[List[bool]] = [False, False, False, False, False, False]
    
    @field_validator('x', 'y', 'z')
    @classmethod
    def validate_coordinates(cls, v, info):
        """Validate coordinate values"""
        is_valid, error = NodeValidator.validate_coordinates(v, v, v)
        if not is_valid:
            raise ValueError(error)
        return v
    
    @field_validator('restraints')
    @classmethod
    def validate_restraints(cls, v, info):
        """Validate restraints list"""
        if v is not None and len(v) != 6:
            raise ValueError("Restraints must have exactly 6 values [ux, uy, uz, rx, ry, rz]")
        return v

class NodeUpdate(BaseModel):
    x: Optional[float] = Field(None, description="X coordinate (mm)")
    y: Optional[float] = Field(None, description="Y coordinate (mm)")
    z: Optional[float] = Field(None, description="Z coordinate (mm)")
    restraints: Optional[List[bool]] = None
    
    @field_validator('x', 'y', 'z')
    @classmethod
    def validate_coordinates(cls, v, info):
        """Validate coordinate values"""
        if v is not None:
            is_valid, error = NodeValidator.validate_coordinates(v, v, v)
            if not is_valid:
                raise ValueError(error)
        return v

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
    """
    Create a new node with comprehensive validation
    
    Validates:
    - Coordinate ranges and finite values
    - Duplicate node detection
    - Project existence
    """
    try:
        # Validate coordinates
        is_valid, error = NodeValidator.validate_coordinates(node.x, node.y, node.z)
        if not is_valid:
            raise InvalidNodeError(error)
        
        # Check for duplicate nodes
        existing_nodes = db.query(Node).filter(Node.project_id == node.project_id).all()
        is_duplicate, error = NodeValidator.check_duplicate(node.x, node.y, node.z, existing_nodes)
        if is_duplicate:
            raise DuplicateNodeError(node.node_id, "existing", 0.0)
        
        # Create node
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
        
        logger.info(f"Created node {node.node_id} at ({node.x}, {node.y}, {node.z})")
        return db_node
        
    except (InvalidNodeError, DuplicateNodeError) as e:
        db.rollback()
        response = error_to_http_response(e)
        raise HTTPException(status_code=response['status_code'], detail=response['detail'])
    
    except IntegrityError as e:
        db.rollback()
        if "unique constraint" in str(e).lower():
            raise HTTPException(status_code=409, detail=f"Node with ID '{node.node_id}' already exists")
        elif "foreign key" in str(e).lower():
            raise HTTPException(status_code=404, detail=f"Project {node.project_id} not found")
        raise HTTPException(status_code=400, detail=str(e))
    
    except OperationalError as e:
        db.rollback()
        logger.error(f"Database error creating node: {e}")
        raise HTTPException(status_code=503, detail="Database temporarily unavailable")
    
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error creating node: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

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
    """Update a node with validation"""
    try:
        db_node = db.query(Node).filter(Node.id == node_id).first()
        if not db_node:
            raise HTTPException(status_code=404, detail="Node not found")
        
        # Get updated coordinates
        new_x = node_update.x if node_update.x is not None else db_node.x
        new_y = node_update.y if node_update.y is not None else db_node.y
        new_z = node_update.z if node_update.z is not None else db_node.z
        
        # Validate new coordinates
        is_valid, error = NodeValidator.validate_coordinates(new_x, new_y, new_z)
        if not is_valid:
            raise InvalidNodeError(error)
        
        # Update fields
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
        
        logger.info(f"Updated node {node_id}")
        return db_node
        
    except InvalidNodeError as e:
        db.rollback()
        response = error_to_http_response(e)
        raise HTTPException(status_code=response['status_code'], detail=response['detail'])
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating node {node_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{node_id}")
def delete_node(node_id: int, db: Session = Depends(get_db)):
    """Delete a node"""
    db_node = db.query(Node).filter(Node.id == node_id).first()
    if not db_node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    db.delete(db_node)
    db.commit()
    return {"status": "success", "message": "Node deleted"}
