from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from app.core.database import get_db
from app.models.project import Material

router = APIRouter()

class MaterialCreate(BaseModel):
    project_id: int
    material_id: str
    name: str
    E: float  # Young's modulus (MPa)
    nu: float  # Poisson's ratio
    density: float  # kg/m³
    fy: Optional[float] = None  # Yield strength (MPa)
    material_type: Optional[str] = "concrete"

class MaterialUpdate(BaseModel):
    name: Optional[str] = None
    E: Optional[float] = None
    nu: Optional[float] = None
    density: Optional[float] = None
    fy: Optional[float] = None
    material_type: Optional[str] = None

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
    """Create a new material"""
    try:
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
        return db_material
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

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
