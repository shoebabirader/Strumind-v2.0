"""
Foundation design API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from app.engine.foundation_design import design_foundation
from app.core.security import get_current_active_user, TokenData

router = APIRouter()


class FoundationDesignRequest(BaseModel):
    foundation_type: str  # 'isolated', 'combined', 'mat', 'pile'
    loads: Dict[str, float]
    soil_properties: Dict[str, float]
    parameters: Dict[str, Any]


@router.post("/design")
async def design_foundation_endpoint(
    request: FoundationDesignRequest,
    current_user: TokenData = Depends(get_current_active_user)
):
    """
    Design foundation based on type and loads
    
    Foundation Types:
    - isolated: Isolated spread footing
    - combined: Combined footing
    - mat: Mat (raft) foundation
    - pile: Pile foundation
    """
    
    try:
        result = design_foundation(
            foundation_type=request.foundation_type,
            loads=request.loads,
            soil_properties=request.soil_properties,
            parameters=request.parameters
        )
        
        return {
            "success": True,
            "foundation_type": request.foundation_type,
            "design_results": result
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Foundation design failed: {str(e)}"
        )


@router.post("/isolated-footing")
async def design_isolated_footing(
    loads: Dict[str, float],
    soil_properties: Dict[str, float],
    column_size: Dict[str, float],
    parameters: Dict[str, Any],
    current_user: TokenData = Depends(get_current_active_user)
):
    """Design isolated spread footing"""
    
    params = {**parameters, "column_size": column_size}
    
    result = design_foundation("isolated", loads, soil_properties, params)
    
    return result


@router.post("/mat-foundation")
async def design_mat_foundation(
    loads: Dict[str, float],
    soil_properties: Dict[str, float],
    parameters: Dict[str, Any],
    current_user: TokenData = Depends(get_current_active_user)
):
    """Design mat (raft) foundation"""
    
    result = design_foundation("mat", loads, soil_properties, parameters)
    
    return result


@router.post("/pile-foundation")
async def design_pile_foundation(
    loads: Dict[str, float],
    soil_properties: Dict[str, float],
    parameters: Dict[str, Any],
    current_user: TokenData = Depends(get_current_active_user)
):
    """Design pile foundation"""
    
    result = design_foundation("pile", loads, soil_properties, parameters)
    
    return result
