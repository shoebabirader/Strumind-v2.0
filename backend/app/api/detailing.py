from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, List

router = APIRouter()

class DetailingRequest(BaseModel):
    model_config = {"protected_namespaces": ()}
    model_id: int
    design_id: int
    output_format: str  # DXF, IFC, PDF

class DetailingResponse(BaseModel):
    model_config = {"protected_namespaces": ()}
    model_id: int
    bbs: List[Dict]  # Bar Bending Schedule
    boq: Dict  # Bill of Quantities
    drawing_url: str

@router.post("/generate", response_model=DetailingResponse)
def generate_detailing(request: DetailingRequest):
    # Placeholder for detailing logic
    bbs = [
        {"bar_mark": "B1", "diameter": 20, "length": 6000, "quantity": 4},
        {"bar_mark": "S1", "diameter": 8, "length": 400, "quantity": 20}
    ]
    
    boq = {
        "concrete": {"grade": "M25", "volume": 2.5, "unit": "m3"},
        "steel": {"total_weight": 150, "unit": "kg"}
    }
    
    return DetailingResponse(
        model_id=request.model_id,
        bbs=bbs,
        boq=boq,
        drawing_url="/exports/drawing_123.pdf"
    )
