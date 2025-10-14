from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict
from app.core.database import get_db
from app.models.project import Project, StructuralModel

router = APIRouter()

class ModelCreate(BaseModel):
    project_id: int
    geometry_data: Dict
    materials: Dict
    sections: Dict

class ModelResponse(BaseModel):
    id: int
    project_id: int
    geometry_data: Dict
    
    class Config:
        from_attributes = True

@router.post("/create", response_model=ModelResponse)
def create_model(model: ModelCreate, db: Session = Depends(get_db)):
    db_model = StructuralModel(**model.dict())
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model

@router.get("/{model_id}", response_model=ModelResponse)
def get_model(model_id: int, db: Session = Depends(get_db)):
    model = db.query(StructuralModel).filter(StructuralModel.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model
