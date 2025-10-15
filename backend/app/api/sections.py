from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from app.core.database import get_db
from app.models.project import Section

router = APIRouter()

class SectionCreate(BaseModel):
    project_id: int
    section_id: str
    name: str
    section_type: str  # rectangular, circular, i-section, t-section
    width: Optional[float] = None
    height: Optional[float] = None
    diameter: Optional[float] = None
    flange_width: Optional[float] = None
    flange_thickness: Optional[float] = None
    web_thickness: Optional[float] = None

class SectionUpdate(BaseModel):
    name: Optional[str] = None
    section_type: Optional[str] = None
    width: Optional[float] = None
    height: Optional[float] = None
    diameter: Optional[float] = None
    flange_width: Optional[float] = None
    flange_thickness: Optional[float] = None
    web_thickness: Optional[float] = None

class SectionResponse(BaseModel):
    id: int
    project_id: int
    section_id: str
    name: str
    section_type: str
    width: Optional[float]
    height: Optional[float]
    diameter: Optional[float]
    flange_width: Optional[float]
    flange_thickness: Optional[float]
    web_thickness: Optional[float]
    
    class Config:
        from_attributes = True

# Predefined section library
SECTION_LIBRARY = [
    {
        "id": "rect_300x500",
        "name": "Rectangular 300×500",
        "type": "rectangular",
        "width": 0.3,
        "height": 0.5
    },
    {
        "id": "rect_400x600",
        "name": "Rectangular 400×600",
        "type": "rectangular",
        "width": 0.4,
        "height": 0.6
    },
    {
        "id": "rect_500x700",
        "name": "Rectangular 500×700",
        "type": "rectangular",
        "width": 0.5,
        "height": 0.7
    },
    {
        "id": "circ_300",
        "name": "Circular Ø300",
        "type": "circular",
        "diameter": 0.3
    },
    {
        "id": "circ_400",
        "name": "Circular Ø400",
        "type": "circular",
        "diameter": 0.4
    },
    {
        "id": "i_section_ismb_300",
        "name": "ISMB 300",
        "type": "i-section",
        "height": 0.3,
        "flange_width": 0.15,
        "web_thickness": 0.0075,
        "flange_thickness": 0.0115
    }
]

@router.get("/library")
def get_section_library():
    """Get predefined section library"""
    return {"sections": SECTION_LIBRARY}

@router.post("/create", response_model=SectionResponse)
def create_section(section: SectionCreate, db: Session = Depends(get_db)):
    """Create a new section"""
    try:
        db_section = Section(
            project_id=section.project_id,
            section_id=section.section_id,
            name=section.name,
            section_type=section.section_type,
            width=section.width,
            height=section.height,
            diameter=section.diameter,
            flange_width=section.flange_width,
            flange_thickness=section.flange_thickness,
            web_thickness=section.web_thickness
        )
        db.add(db_section)
        db.commit()
        db.refresh(db_section)
        return db_section
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/list/{project_id}", response_model=List[SectionResponse])
def list_sections(project_id: int, db: Session = Depends(get_db)):
    """List all sections for a project"""
    sections = db.query(Section).filter(Section.project_id == project_id).all()
    return sections

@router.get("/{section_id}", response_model=SectionResponse)
def get_section(section_id: int, db: Session = Depends(get_db)):
    """Get a specific section"""
    section = db.query(Section).filter(Section.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    return section

@router.put("/{section_id}", response_model=SectionResponse)
def update_section(section_id: int, section_update: SectionUpdate, db: Session = Depends(get_db)):
    """Update a section"""
    db_section = db.query(Section).filter(Section.id == section_id).first()
    if not db_section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    update_data = section_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_section, key, value)
    
    db.commit()
    db.refresh(db_section)
    return db_section

@router.delete("/{section_id}")
def delete_section(section_id: int, db: Session = Depends(get_db)):
    """Delete a section"""
    db_section = db.query(Section).filter(Section.id == section_id).first()
    if not db_section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    db.delete(db_section)
    db.commit()
    return {"status": "success", "message": "Section deleted"}
