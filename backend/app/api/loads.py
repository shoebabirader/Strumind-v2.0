from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from app.core.database import get_db
from app.models.project import Load

router = APIRouter()

class LoadCreate(BaseModel):
    project_id: int
    load_id: str
    load_type: str  # nodal, element
    load_case: str  # DL, LL, WL, EQ, SL
    target_id: str  # node_id or element_id
    fx: Optional[float] = 0
    fy: Optional[float] = 0
    fz: Optional[float] = 0
    mx: Optional[float] = 0
    my: Optional[float] = 0
    mz: Optional[float] = 0
    magnitude: Optional[float] = 0
    direction: Optional[str] = "global-y"
    distribution: Optional[str] = "uniform"

class LoadUpdate(BaseModel):
    load_case: Optional[str] = None
    fx: Optional[float] = None
    fy: Optional[float] = None
    fz: Optional[float] = None
    mx: Optional[float] = None
    my: Optional[float] = None
    mz: Optional[float] = None
    magnitude: Optional[float] = None
    direction: Optional[str] = None
    distribution: Optional[str] = None

class LoadResponse(BaseModel):
    id: int
    project_id: int
    load_id: str
    load_type: str
    load_case: str
    target_id: str
    fx: Optional[float]
    fy: Optional[float]
    fz: Optional[float]
    mx: Optional[float]
    my: Optional[float]
    mz: Optional[float]
    magnitude: Optional[float]
    direction: Optional[str]
    distribution: Optional[str]
    
    class Config:
        from_attributes = True

@router.post("/create", response_model=LoadResponse)
def create_load(load: LoadCreate, db: Session = Depends(get_db)):
    """Create a new load"""
    try:
        db_load = Load(
            project_id=load.project_id,
            load_id=load.load_id,
            load_type=load.load_type,
            load_case=load.load_case,
            target_id=load.target_id,
            fx=load.fx,
            fy=load.fy,
            fz=load.fz,
            mx=load.mx,
            my=load.my,
            mz=load.mz,
            magnitude=load.magnitude,
            direction=load.direction,
            distribution=load.distribution
        )
        db.add(db_load)
        db.commit()
        db.refresh(db_load)
        return db_load
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/nodal", response_model=LoadResponse)
def create_nodal_load(load: LoadCreate, db: Session = Depends(get_db)):
    """Create a nodal load"""
    load.load_type = "nodal"
    return create_load(load, db)

@router.post("/element", response_model=LoadResponse)
def create_element_load(load: LoadCreate, db: Session = Depends(get_db)):
    """Create an element load"""
    load.load_type = "element"
    return create_load(load, db)

@router.get("/list/{project_id}", response_model=List[LoadResponse])
def list_loads(project_id: int, db: Session = Depends(get_db)):
    """List all loads for a project"""
    loads = db.query(Load).filter(Load.project_id == project_id).all()
    return loads

@router.get("/{load_id}", response_model=LoadResponse)
def get_load(load_id: int, db: Session = Depends(get_db)):
    """Get a specific load"""
    load = db.query(Load).filter(Load.id == load_id).first()
    if not load:
        raise HTTPException(status_code=404, detail="Load not found")
    return load

@router.put("/{load_id}", response_model=LoadResponse)
def update_load(load_id: int, load_update: LoadUpdate, db: Session = Depends(get_db)):
    """Update a load"""
    db_load = db.query(Load).filter(Load.id == load_id).first()
    if not db_load:
        raise HTTPException(status_code=404, detail="Load not found")
    
    update_data = load_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_load, key, value)
    
    db.commit()
    db.refresh(db_load)
    return db_load

@router.delete("/{load_id}")
def delete_load(load_id: int, db: Session = Depends(get_db)):
    """Delete a load"""
    db_load = db.query(Load).filter(Load.id == load_id).first()
    if not db_load:
        raise HTTPException(status_code=404, detail="Load not found")
    
    db.delete(db_load)
    db.commit()
    return {"status": "success", "message": "Load deleted"}
