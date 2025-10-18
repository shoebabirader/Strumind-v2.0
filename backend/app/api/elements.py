from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError
from pydantic import BaseModel, field_validator, Field
from typing import List, Optional
import logging
from app.core.database import get_db
from app.models.project import Element, Node
from app.core.validators import GeometryValidator
from app.core.errors import (
    InvalidElementError, ZeroLengthElementError, DisconnectedElementError,
    error_to_http_response
)

router = APIRouter()
logger = logging.getLogger(__name__)

class ElementCreate(BaseModel):
    project_id: int
    element_id: str = Field(..., description="Unique element identifier")
    node_i: str = Field(..., description="Start node ID")
    node_j: str = Field(..., description="End node ID")
    element_type: str = Field(..., description="Element type (beam, column, truss, etc.)")
    material_id: Optional[str] = Field(None, description="Material ID")
    section_type: Optional[str] = Field("rectangular", description="Section type")
    width: Optional[float] = Field(0.3, gt=0, description="Width (m)")
    height: Optional[float] = Field(0.5, gt=0, description="Height (m)")
    
    @field_validator('node_i', 'node_j')
    @classmethod
    def validate_node_ids(cls, v, info):
        """Validate node IDs are not empty"""
        if not v or v.strip() == "":
            raise ValueError("Node ID cannot be empty")
        return v
    
    @field_validator('node_j')
    @classmethod
    def validate_different_nodes(cls, v, info):
        """Ensure start and end nodes are different"""
        if 'node_i' in values and v == info.data.get('node_i'):
            raise ValueError("Start and end nodes must be different")
        return v
    
    @field_validator('element_type')
    @classmethod
    def validate_element_type(cls, v, info):
        """Validate element type"""
        valid_types = ['beam', 'column', 'truss', 'brace', 'slab', 'wall', 'shell']
        if v.lower() not in valid_types:
            raise ValueError(f"Element type must be one of: {', '.join(valid_types)}")
        return v.lower()

class ElementUpdate(BaseModel):
    node_i: Optional[str] = Field(None, description="Start node ID")
    node_j: Optional[str] = Field(None, description="End node ID")
    element_type: Optional[str] = Field(None, description="Element type")
    material_id: Optional[str] = Field(None, description="Material ID")
    section_type: Optional[str] = Field(None, description="Section type")
    width: Optional[float] = Field(None, gt=0, description="Width (m)")
    height: Optional[float] = Field(None, gt=0, description="Height (m)")

class ElementResponse(BaseModel):
    id: int
    project_id: int
    element_id: str
    node_i: str
    node_j: str
    element_type: str
    material_id: Optional[str]
    section_type: Optional[str]
    width: Optional[float]
    height: Optional[float]
    
    class Config:
        from_attributes = True

@router.post("/create", response_model=ElementResponse)
def create_element(element: ElementCreate, db: Session = Depends(get_db)):
    """
    Create a new element with comprehensive validation
    
    Validates:
    - Node existence
    - Element length (no zero-length elements)
    - Node connectivity
    - Duplicate element check
    """
    try:
        # Check if nodes exist
        node_i = db.query(Node).filter(
            Node.project_id == element.project_id,
            Node.node_id == element.node_i
        ).first()
        
        node_j = db.query(Node).filter(
            Node.project_id == element.project_id,
            Node.node_id == element.node_j
        ).first()
        
        if not node_i:
            raise DisconnectedElementError(element.element_id, [element.node_i])
        
        if not node_j:
            raise DisconnectedElementError(element.element_id, [element.node_j])
        
        # Calculate element length
        import math
        length = math.sqrt(
            (node_j.x - node_i.x)**2 +
            (node_j.y - node_i.y)**2 +
            (node_j.z - node_i.z)**2
        )
        
        # Validate element length
        is_valid, error = GeometryValidator.validate_element_length(length)
        if not is_valid:
            raise ZeroLengthElementError(element.element_id, length)
        
        # Check aspect ratio if dimensions provided
        if element.width and element.height:
            min_dim = min(element.width, element.height) * 1000  # Convert to mm
            is_valid, error = GeometryValidator.check_element_aspect_ratio(length, min_dim)
            if not is_valid:
                logger.warning(f"Element {element.element_id}: {error}")
        
        # Create element
        db_element = Element(
            project_id=element.project_id,
            element_id=element.element_id,
            node_i=element.node_i,
            node_j=element.node_j,
            element_type=element.element_type,
            material_id=element.material_id,
            section_type=element.section_type,
            width=element.width,
            height=element.height
        )
        db.add(db_element)
        db.commit()
        db.refresh(db_element)
        
        logger.info(f"Created element {element.element_id} ({element.node_i} -> {element.node_j}), length={length:.2f}mm")
        return db_element
        
    except (InvalidElementError, ZeroLengthElementError, DisconnectedElementError) as e:
        db.rollback()
        response = error_to_http_response(e)
        raise HTTPException(status_code=response['status_code'], detail=response['detail'])
    
    except IntegrityError as e:
        db.rollback()
        if "unique constraint" in str(e).lower():
            raise HTTPException(status_code=409, detail=f"Element with ID '{element.element_id}' already exists")
        elif "foreign key" in str(e).lower():
            raise HTTPException(status_code=404, detail=f"Project {element.project_id} not found")
        raise HTTPException(status_code=400, detail=str(e))
    
    except OperationalError as e:
        db.rollback()
        logger.error(f"Database error creating element: {e}")
        raise HTTPException(status_code=503, detail="Database temporarily unavailable")
    
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error creating element: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/list/{project_id}", response_model=List[ElementResponse])
def list_elements(project_id: int, db: Session = Depends(get_db)):
    """List all elements for a project"""
    elements = db.query(Element).filter(Element.project_id == project_id).all()
    return elements

@router.get("/{element_id}", response_model=ElementResponse)
def get_element(element_id: int, db: Session = Depends(get_db)):
    """Get a specific element"""
    element = db.query(Element).filter(Element.id == element_id).first()
    if not element:
        raise HTTPException(status_code=404, detail="Element not found")
    return element

@router.put("/{element_id}", response_model=ElementResponse)
def update_element(element_id: int, element_update: ElementUpdate, db: Session = Depends(get_db)):
    """Update an element"""
    db_element = db.query(Element).filter(Element.id == element_id).first()
    if not db_element:
        raise HTTPException(status_code=404, detail="Element not found")
    
    update_data = element_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_element, key, value)
    
    db.commit()
    db.refresh(db_element)
    return db_element

@router.delete("/{element_id}")
def delete_element(element_id: int, db: Session = Depends(get_db)):
    """Delete an element"""
    db_element = db.query(Element).filter(Element.id == element_id).first()
    if not db_element:
        raise HTTPException(status_code=404, detail="Element not found")
    
    db.delete(db_element)
    db.commit()
    return {"status": "success", "message": "Element deleted"}
