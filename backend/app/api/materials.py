from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError
from pydantic import BaseModel, field_validator, Field
from typing import List, Optional
import logging
from app.core.database import get_db
from app.models.project import Material
from app.core.validators import MaterialValidator
from app.core.errors import (
    InvalidMaterialPropertyError, MaterialNotFoundError,
    error_to_http_response
)

router = APIRouter()
logger = logging.getLogger(__name__)

class MaterialCreate(BaseModel):
    project_id: int
    material_id: str = Field(..., description="Unique material identifier")
    name: str = Field(..., description="Material name")
    E: float = Field(..., gt=0, description="Young's modulus (MPa)")
    nu: float = Field(..., ge=-1, le=0.5, description="Poisson's ratio")
    density: float = Field(..., gt=0, description="Density (kg/m³)")
    fy: Optional[float] = Field(None, gt=0, description="Yield strength (MPa)")
    fu: Optional[float] = Field(None, gt=0, description="Ultimate strength (MPa)")
    material_type: Optional[str] = Field("concrete", description="Material type")
    
    @field_validator('E')
    @classmethod
    def validate_E(cls, v, info):
        """Validate Young's modulus"""
        is_valid, error = MaterialValidator.validate_elastic_modulus(v)
        if not is_valid:
            raise ValueError(error)
        return v
    
    @field_validator('nu')
    @classmethod
    def validate_nu(cls, v, info):
        """Validate Poisson's ratio"""
        is_valid, error = MaterialValidator.validate_poisson_ratio(v)
        if not is_valid:
            raise ValueError(error)
        return v
    
    @field_validator('density')
    @classmethod
    def validate_density(cls, v, info):
        """Validate density"""
        is_valid, error = MaterialValidator.validate_density(v)
        if not is_valid:
            raise ValueError(error)
        return v
    
    @field_validator('fu')
    @classmethod
    def validate_fu(cls, v, info):
        """Validate ultimate strength"""
        if v is not None and 'fy' in values and info.data.get('fy') is not None:
            is_valid, error = MaterialValidator.validate_yield_stress(info.data.get('fy'), v)
            if not is_valid:
                raise ValueError(error)
        return v

class MaterialUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Material name")
    E: Optional[float] = Field(None, gt=0, description="Young's modulus (MPa)")
    nu: Optional[float] = Field(None, ge=-1, le=0.5, description="Poisson's ratio")
    density: Optional[float] = Field(None, gt=0, description="Density (kg/m³)")
    fy: Optional[float] = Field(None, gt=0, description="Yield strength (MPa)")
    fu: Optional[float] = Field(None, gt=0, description="Ultimate strength (MPa)")
    material_type: Optional[str] = Field(None, description="Material type")

class MaterialResponse(BaseModel):
    id: int
    project_id: int
    material_id: str
    name: str
    E: float
    nu: float
    density: float
    fy: Optional[float]
    material_type: Optional[str]
    
    class Config:
        from_attributes = True

# Predefined material library
MATERIAL_LIBRARY = [
    {
        "id": "concrete_m20",
        "name": "Concrete M20",
        "E": 22000,
        "nu": 0.2,
        "density": 2500,
        "fy": 20,
        "type": "concrete"
    },
    {
        "id": "concrete_m25",
        "name": "Concrete M25",
        "E": 25000,
        "nu": 0.2,
        "density": 2500,
        "fy": 25,
        "type": "concrete"
    },
    {
        "id": "concrete_m30",
        "name": "Concrete M30",
        "E": 27000,
        "nu": 0.2,
        "density": 2500,
        "fy": 30,
        "type": "concrete"
    },
    {
        "id": "steel_fe415",
        "name": "Steel Fe415",
        "E": 200000,
        "nu": 0.3,
        "density": 7850,
        "fy": 415,
        "type": "steel"
    },
    {
        "id": "steel_fe500",
        "name": "Steel Fe500",
        "E": 200000,
        "nu": 0.3,
        "density": 7850,
        "fy": 500,
        "type": "steel"
    },
    {
        "id": "steel_a36",
        "name": "Steel A36",
        "E": 200000,
        "nu": 0.3,
        "density": 7850,
        "fy": 250,
        "type": "steel"
    },
    {
        "id": "aluminum_6061",
        "name": "Aluminum 6061",
        "E": 70000,
        "nu": 0.33,
        "density": 2700,
        "fy": 276,
        "type": "aluminum"
    }
]

@router.get("/library")
def get_material_library():
    """Get predefined material library"""
    return {"materials": MATERIAL_LIBRARY}

@router.post("/create", response_model=MaterialResponse)
def create_material(material: MaterialCreate, db: Session = Depends(get_db)):
    """
    Create a new material with comprehensive validation
    
    Validates:
    - Young's modulus (1,000 - 500,000 MPa)
    - Poisson's ratio (-1.0 to 0.5)
    - Density (100 - 20,000 kg/m³)
    - Yield vs ultimate strength relationship
    """
    try:
        # Additional validation
        is_valid, error = MaterialValidator.validate_elastic_modulus(material.E)
        if not is_valid:
            raise InvalidMaterialPropertyError(error)
        
        is_valid, error = MaterialValidator.validate_poisson_ratio(material.nu)
        if not is_valid:
            raise InvalidMaterialPropertyError(error)
        
        is_valid, error = MaterialValidator.validate_density(material.density)
        if not is_valid:
            raise InvalidMaterialPropertyError(error)
        
        if material.fy and material.fu:
            is_valid, error = MaterialValidator.validate_yield_stress(material.fy, material.fu)
            if not is_valid:
                raise InvalidMaterialPropertyError(error)
        
        # Create material
        db_material = Material(
            project_id=material.project_id,
            material_id=material.material_id,
            name=material.name,
            E=material.E,
            nu=material.nu,
            density=material.density,
            fy=material.fy,
            material_type=material.material_type
        )
        db.add(db_material)
        db.commit()
        db.refresh(db_material)
        
        logger.info(f"Created material {material.material_id}: {material.name} (E={material.E} MPa)")
        return db_material
        
    except InvalidMaterialPropertyError as e:
        db.rollback()
        response = error_to_http_response(e)
        raise HTTPException(status_code=response['status_code'], detail=response['detail'])
    
    except IntegrityError as e:
        db.rollback()
        if "unique constraint" in str(e).lower():
            raise HTTPException(status_code=409, detail=f"Material with ID '{material.material_id}' already exists")
        elif "foreign key" in str(e).lower():
            raise HTTPException(status_code=404, detail=f"Project {material.project_id} not found")
        raise HTTPException(status_code=400, detail=str(e))
    
    except OperationalError as e:
        db.rollback()
        logger.error(f"Database error creating material: {e}")
        raise HTTPException(status_code=503, detail="Database temporarily unavailable")
    
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error creating material: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/list/{project_id}", response_model=List[MaterialResponse])
def list_materials(project_id: int, db: Session = Depends(get_db)):
    """List all materials for a project"""
    materials = db.query(Material).filter(Material.project_id == project_id).all()
    return materials

@router.get("/{material_id}", response_model=MaterialResponse)
def get_material(material_id: int, db: Session = Depends(get_db)):
    """Get a specific material"""
    material = db.query(Material).filter(Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material

@router.put("/{material_id}", response_model=MaterialResponse)
def update_material(material_id: int, material_update: MaterialUpdate, db: Session = Depends(get_db)):
    """Update a material"""
    db_material = db.query(Material).filter(Material.id == material_id).first()
    if not db_material:
        raise HTTPException(status_code=404, detail="Material not found")
    
    update_data = material_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_material, key, value)
    
    db.commit()
    db.refresh(db_material)
    return db_material

@router.delete("/{material_id}")
def delete_material(material_id: int, db: Session = Depends(get_db)):
    """Delete a material"""
    db_material = db.query(Material).filter(Material.id == material_id).first()
    if not db_material:
        raise HTTPException(status_code=404, detail="Material not found")
    
    db.delete(db_material)
    db.commit()
    return {"status": "success", "message": "Material deleted"}
