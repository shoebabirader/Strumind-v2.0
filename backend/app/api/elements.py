from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from app.core.database import get_db
from app.models.project import Element

router = APIRouter()

class ElementCreate(BaseModel):
    project_id: int
    element_id: str
    node_i: str
    node_j: str
    element_type: str
    material_id: Optional[str] = None
    section_type: Optional[str] = "rectangular"
    width: Optional[float] = 0.3
    height: Optional[float] = 0.5

class ElementUpdate(BaseModel):
    node_i: Optional[str] = None
    node_j: Optional[str] = None
    element_type: Optional[str] = None
    material_id: Optional[str] = None
    section_type: Optional[str] = None
    width: Optional[float] = None
    height: Optional[float] = None

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
    """Create a new element"""
    try:
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
        return db_element
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

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
