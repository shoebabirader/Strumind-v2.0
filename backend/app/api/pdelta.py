from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import numpy as np
from app.engine.pdelta import PDeltaAnalysis

router = APIRouter()

class PDeltaRequest(BaseModel):
    stiffness_matrix: List[List[float]]
    mass_matrix: List[List[float]]
    loads: List[float]
    axial_forces: List[float]
    element_lengths: List[float]

class StabilityIndexRequest(BaseModel):
    story_shear: float
    story_weight: float
    story_drift: float
    story_height: float

@router.post("/analysis")
def pdelta_analysis(request: PDeltaRequest):
    """Perform P-Delta analysis"""
    try:
        analyzer = PDeltaAnalysis()
        
        K = np.array(request.stiffness_matrix)
        M = np.array(request.mass_matrix)
        P = np.array(request.loads)
        axial = np.array(request.axial_forces)
        lengths = np.array(request.element_lengths)
        
        result = analyzer.pdelta_analysis(K, M, P, axial, lengths)
        
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/stability-index")
def calculate_stability_index(request: StabilityIndexRequest):
    """Calculate stability index (theta)"""
    try:
        analyzer = PDeltaAnalysis()
        result = analyzer.stability_index(
            request.story_shear,
            request.story_weight,
            request.story_drift,
            request.story_height
        )
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/moment-amplification")
def moment_amplification(Pu: float, Pc: float, Cm: float = 1.0):
    """Calculate moment amplification factor"""
    try:
        analyzer = PDeltaAnalysis()
        result = analyzer.moment_amplification_factor(Pu, Pc, Cm)
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
