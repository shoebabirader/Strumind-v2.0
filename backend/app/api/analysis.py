from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from app.engine.geometry import GeometryEngine
from app.engine.analysis import StructuralAnalysis

router = APIRouter()

class AnalysisRequest(BaseModel):
    model_id: int
    analysis_type: str  # static, modal, pushover
    loads: List[float]
    material_props: Dict
    section_props: Dict

class AnalysisResponse(BaseModel):
    model_id: int
    analysis_type: str
    results: Dict

@router.post("/run", response_model=AnalysisResponse)
def run_analysis(request: AnalysisRequest):
    # Initialize geometry and analysis engines
    geom = GeometryEngine()
    analyzer = StructuralAnalysis(geom)
    
    # Assemble stiffness matrix
    analyzer.assemble_stiffness_matrix(request.material_props, request.section_props)
    
    # Run analysis based on type
    if request.analysis_type == "static":
        displacements = analyzer.static_analysis(request.loads)
        results = {"displacements": displacements.tolist()}
    elif request.analysis_type == "modal":
        frequencies, modes = analyzer.modal_analysis()
        results = {"frequencies": frequencies.tolist()}
    else:
        raise HTTPException(status_code=400, detail="Unsupported analysis type")
    
    return AnalysisResponse(
        model_id=request.model_id,
        analysis_type=request.analysis_type,
        results=results
    )
