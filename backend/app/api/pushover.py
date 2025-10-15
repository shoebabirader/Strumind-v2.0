"""
Pushover analysis API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from app.engine.pushover_analysis import run_pushover_analysis
from app.core.security import get_current_active_user, TokenData
from app.core.cache import cached

router = APIRouter()


class PushoverRequest(BaseModel):
    model_data: Dict[Any, Any]
    control_node: str
    load_pattern: Dict[str, float]
    target_displacement: Optional[float] = None
    num_steps: int = 100
    project_id: Optional[int] = None


class PushoverResponse(BaseModel):
    success: bool
    capacity_curve: Dict[str, List[float]]
    performance_point: Dict[str, float]
    performance_level: str
    max_displacement: float
    max_base_shear: float
    ductility: float
    overstrength: float
    steps_completed: int


@router.post("/pushover", response_model=PushoverResponse)
async def run_pushover(
    request: PushoverRequest,
    current_user: TokenData = Depends(get_current_active_user)
):
    """
    Run pushover analysis for seismic performance evaluation
    
    Generates capacity curve and determines performance point
    according to FEMA 356/ASCE 41 guidelines
    
    Performance Levels:
    - IO: Immediate Occupancy
    - LS: Life Safety  
    - CP: Collapse Prevention
    - C: Collapse
    """
    
    try:
        parameters = {
            "control_node": request.control_node,
            "load_pattern": request.load_pattern,
            "target_displacement": request.target_displacement,
            "num_steps": request.num_steps
        }
        
        results = run_pushover_analysis(request.model_data, parameters)
        
        return PushoverResponse(
            success=results["success"],
            capacity_curve=results["capacity_curve"],
            performance_point=results["performance_point"],
            performance_level=results["performance_level"],
            max_displacement=results["max_displacement"],
            max_base_shear=results["max_base_shear"],
            ductility=results["ductility"],
            overstrength=results["overstrength"],
            steps_completed=len(results["steps"])
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Pushover analysis failed: {str(e)}"
        )


@router.post("/pushover/capacity-curve")
async def get_capacity_curve(
    request: PushoverRequest,
    current_user: TokenData = Depends(get_current_active_user)
):
    """Get only the capacity curve without full analysis"""
    
    try:
        parameters = {
            "control_node": request.control_node,
            "load_pattern": request.load_pattern,
            "target_displacement": request.target_displacement,
            "num_steps": request.num_steps
        }
        
        results = run_pushover_analysis(request.model_data, parameters)
        
        return {
            "displacement": results["capacity_curve"]["displacement"],
            "base_shear": results["capacity_curve"]["base_shear"],
            "ductility": results["ductility"],
            "overstrength": results["overstrength"]
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Capacity curve generation failed: {str(e)}"
        )


@router.post("/pushover/performance-point")
async def get_performance_point(
    request: PushoverRequest,
    current_user: TokenData = Depends(get_current_active_user)
):
    """Determine performance point and level"""
    
    try:
        parameters = {
            "control_node": request.control_node,
            "load_pattern": request.load_pattern,
            "target_displacement": request.target_displacement,
            "num_steps": request.num_steps
        }
        
        results = run_pushover_analysis(request.model_data, parameters)
        
        return {
            "performance_point": results["performance_point"],
            "performance_level": results["performance_level"],
            "interpretation": _interpret_performance_level(results["performance_level"])
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Performance point calculation failed: {str(e)}"
        )


def _interpret_performance_level(level: str) -> str:
    """Provide interpretation of performance level"""
    
    interpretations = {
        "IO - Immediate Occupancy": "Structure remains operational with minimal damage. Occupants can remain in building.",
        "LS - Life Safety": "Significant damage but no collapse. Building may need repairs before reoccupancy.",
        "CP - Collapse Prevention": "Severe damage. Building on verge of collapse but has not collapsed.",
        "C - Collapse": "Structure has collapsed or is in imminent danger of collapse."
    }
    
    return interpretations.get(level, "Unknown performance level")
