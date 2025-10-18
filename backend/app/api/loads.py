from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError
from pydantic import BaseModel, field_validator, Field
from typing import List, Optional
import logging
from app.core.database import get_db
from app.models.project import Load
from app.core.validators import LoadValidator
from app.core.errors import InvalidLoadError, error_to_http_response

router = APIRouter()
logger = logging.getLogger(__name__)

class LoadCreate(BaseModel):
    project_id: int
    load_id: str = Field(..., description="Unique load identifier")
    load_type: str = Field(..., description="Load type: nodal or element")
    load_case: str = Field(..., description="Load case: DL, LL, WL, EQ, SL")
    target_id: str = Field(..., description="Target node_id or element_id")
    fx: Optional[float] = Field(0, description="Force in X direction (N)")
    fy: Optional[float] = Field(0, description="Force in Y direction (N)")
    fz: Optional[float] = Field(0, description="Force in Z direction (N)")
    mx: Optional[float] = Field(0, description="Moment about X axis (N·mm)")
    my: Optional[float] = Field(0, description="Moment about Y axis (N·mm)")
    mz: Optional[float] = Field(0, description="Moment about Z axis (N·mm)")
    magnitude: Optional[float] = Field(0, description="Load magnitude")
    direction: Optional[str] = Field("global-y", description="Load direction")
    distribution: Optional[str] = Field("uniform", description="Load distribution")
    
    @field_validator('load_type')
    @classmethod
    def validate_load_type(cls, v, info):
        """Validate load type"""
        valid_types = ['nodal', 'element', 'distributed', 'point']
        if v.lower() not in valid_types:
            raise ValueError(f"Load type must be one of: {', '.join(valid_types)}")
        return v.lower()
    
    @field_validator('load_case')
    @classmethod
    def validate_load_case(cls, v, info):
        """Validate load case"""
        valid_cases = ['DL', 'LL', 'WL', 'EQ', 'SL', 'TL', 'DEAD', 'LIVE', 'WIND', 'EARTHQUAKE', 'SNOW', 'TEMPERATURE']
        if v.upper() not in valid_cases:
            raise ValueError(f"Load case must be one of: {', '.join(valid_cases)}")
        return v.upper()
    
    @field_validator('fx', 'fy', 'fz')
    @classmethod
    def validate_forces(cls, v, info):
        """Validate force magnitudes"""
        is_valid, error = LoadValidator.validate_force(v, info.field_name)
        if not is_valid:
            raise ValueError(error)
        return v
    
    @field_validator('mx', 'my', 'mz')
    @classmethod
    def validate_moments(cls, v, info):
        """Validate moment magnitudes"""
        is_valid, error = LoadValidator.validate_moment(v, info.field_name)
        if not is_valid:
            raise ValueError(error)
        return v

class LoadUpdate(BaseModel):
    load_case: Optional[str] = Field(None, description="Load case")
    fx: Optional[float] = Field(None, description="Force in X (N)")
    fy: Optional[float] = Field(None, description="Force in Y (N)")
    fz: Optional[float] = Field(None, description="Force in Z (N)")
    mx: Optional[float] = Field(None, description="Moment about X (N·mm)")
    my: Optional[float] = Field(None, description="Moment about Y (N·mm)")
    mz: Optional[float] = Field(None, description="Moment about Z (N·mm)")
    magnitude: Optional[float] = Field(None, description="Load magnitude")
    direction: Optional[str] = Field(None, description="Load direction")
    distribution: Optional[str] = Field(None, description="Load distribution")

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
    """
    Create a new load with comprehensive validation
    
    Validates:
    - Load type (nodal, element, distributed, point)
    - Load case (DL, LL, WL, EQ, SL, etc.)
    - Force magnitudes (max 100,000 kN)
    - Moment magnitudes (max 10,000 kN·m)
    - Target existence (node or element)
    """
    try:
        # Validate forces
        for force, direction in [(load.fx, 'X'), (load.fy, 'Y'), (load.fz, 'Z')]:
            is_valid, error = LoadValidator.validate_force(force, direction)
            if not is_valid:
                raise InvalidLoadError(error)
        
        # Validate moments
        for moment, axis in [(load.mx, 'X'), (load.my, 'Y'), (load.mz, 'Z')]:
            is_valid, error = LoadValidator.validate_moment(moment, axis)
            if not is_valid:
                raise InvalidLoadError(error)
        
        # Create load
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
        
        logger.info(f"Created load {load.load_id}: {load.load_case} on {load.target_id}")
        return db_load
        
    except InvalidLoadError as e:
        db.rollback()
        response = error_to_http_response(e)
        raise HTTPException(status_code=response['status_code'], detail=response['detail'])
    
    except IntegrityError as e:
        db.rollback()
        if "unique constraint" in str(e).lower():
            raise HTTPException(status_code=409, detail=f"Load with ID '{load.load_id}' already exists")
        elif "foreign key" in str(e).lower():
            raise HTTPException(status_code=404, detail=f"Project {load.project_id} not found")
        raise HTTPException(status_code=400, detail=str(e))
    
    except OperationalError as e:
        db.rollback()
        logger.error(f"Database error creating load: {e}")
        raise HTTPException(status_code=503, detail="Database temporarily unavailable")
    
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error creating load: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

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
