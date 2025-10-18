from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError
from pydantic import BaseModel, field_validator, Field
from typing import List, Optional
import logging
import math
from app.core.database import get_db
from app.models.project import Section
from app.core.validators import SectionValidator
from app.core.errors import InvalidSectionPropertyError, error_to_http_response

router = APIRouter()
logger = logging.getLogger(__name__)

class SectionCreate(BaseModel):
    project_id: int
    section_id: str = Field(..., description="Unique section identifier")
    name: str = Field(..., description="Section name")
    section_type: str = Field(..., description="Section type")
    width: Optional[float] = Field(None, gt=0, description="Width (m)")
    height: Optional[float] = Field(None, gt=0, description="Height (m)")
    diameter: Optional[float] = Field(None, gt=0, description="Diameter (m)")
    flange_width: Optional[float] = Field(None, gt=0, description="Flange width (m)")
    flange_thickness: Optional[float] = Field(None, gt=0, description="Flange thickness (m)")
    web_thickness: Optional[float] = Field(None, gt=0, description="Web thickness (m)")
    
    @field_validator('section_type')
    @classmethod
    def validate_section_type(cls, v, info):
        """Validate section type"""
        valid_types = ['rectangular', 'circular', 'i-section', 't-section', 'box', 'channel']
        if v.lower() not in valid_types:
            raise ValueError(f"Section type must be one of: {', '.join(valid_types)}")
        return v.lower()
    
    def calculate_properties(self):
        """Calculate section properties (A, Iy, Iz, J)"""
        if self.section_type == 'rectangular' and self.width and self.height:
            b, h = self.width * 1000, self.height * 1000  # Convert to mm
            A = b * h
            Iy = (b * h**3) / 12
            Iz = (h * b**3) / 12
            J = (b * h**3) * (1/3 - 0.21 * (h/b) * (1 - h**4/(12*b**4)))
            return {'A': A, 'Iy': Iy, 'Iz': Iz, 'J': J}
        elif self.section_type == 'circular' and self.diameter:
            d = self.diameter * 1000  # Convert to mm
            A = math.pi * d**2 / 4
            I = math.pi * d**4 / 64
            J = math.pi * d**4 / 32
            return {'A': A, 'Iy': I, 'Iz': I, 'J': J}
        return None

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
    """
    Create a new section with validation
    
    Validates section properties and calculates A, Iy, Iz, J
    """
    try:
        # Calculate section properties
        props = section.calculate_properties()
        if props:
            # Validate calculated properties
            is_valid, error = SectionValidator.validate_section_properties(
                props['A'], props['Iy'], props['Iz'], props['J']
            )
            if not is_valid:
                raise InvalidSectionPropertyError(error)
        
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
        
        logger.info(f"Created section {section.section_id}: {section.name}")
        return db_section
        
    except InvalidSectionPropertyError as e:
        db.rollback()
        response = error_to_http_response(e)
        raise HTTPException(status_code=response['status_code'], detail=response['detail'])
    
    except IntegrityError as e:
        db.rollback()
        if "unique constraint" in str(e).lower():
            raise HTTPException(status_code=409, detail=f"Section with ID '{section.section_id}' already exists")
        raise HTTPException(status_code=400, detail=str(e))
    
    except OperationalError as e:
        db.rollback()
        logger.error(f"Database error creating section: {e}")
        raise HTTPException(status_code=503, detail="Database temporarily unavailable")
    
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error creating section: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

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
