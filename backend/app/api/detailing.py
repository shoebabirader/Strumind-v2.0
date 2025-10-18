from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import logging
import math

router = APIRouter()
logger = logging.getLogger(__name__)

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
    """
    Generate Bar Bending Schedule (BBS) and detailing drawings
    
    Creates:
    - Bar bending schedule with cutting lengths
    - Bill of quantities
    - DXF/IFC export ready data
    """
    try:
        logger.info(f"Generating detailing for design {request.design_id}")
        
        # Generate BBS based on design results
        bbs = []
        
        # Main reinforcement bars
        main_bars = {
            "bar_mark": "M1",
            "diameter": 20,
            "length": _calculate_main_bar_length(request.design_id),
            "quantity": _calculate_main_bar_quantity(request.design_id),
            "shape": "straight",
            "hooks": "standard",
            "cutting_length": _calculate_cutting_length(20, "straight", hooks="standard")
        }
        bbs.append(main_bars)
        
        # Distribution bars
        dist_bars = {
            "bar_mark": "D1",
            "diameter": 12,
            "length": _calculate_distribution_length(request.design_id),
            "quantity": _calculate_distribution_quantity(request.design_id),
            "shape": "straight",
            "hooks": "none",
            "cutting_length": _calculate_cutting_length(12, "straight")
        }
        bbs.append(dist_bars)
        
        # Stirrups/Links
        stirrups = {
            "bar_mark": "S1",
            "diameter": 8,
            "length": _calculate_stirrup_length(request.design_id),
            "quantity": _calculate_stirrup_quantity(request.design_id),
            "shape": "rectangular",
            "hooks": "135_degree",
            "cutting_length": _calculate_cutting_length(8, "rectangular", hooks="135_degree")
        }
        bbs.append(stirrups)
        
        # Calculate total steel weight (kg)
        total_steel_weight = sum(
            (math.pi * (bar["diameter"]/2)**2 * bar["cutting_length"] * bar["quantity"] * 7.85e-6)
            for bar in bbs
        )
        
        # Calculate concrete volume (m³)
        concrete_volume = _calculate_concrete_volume(request.design_id)
        
        # Generate BOQ
        boq = {
            "concrete": {
                "grade": "M25",
                "volume": round(concrete_volume, 3),
                "unit": "m³"
            },
            "steel": {
                "total_weight": round(total_steel_weight, 2),
                "unit": "kg",
                "breakdown": {
                    "main_bars": round(total_steel_weight * 0.6, 2),
                    "distribution": round(total_steel_weight * 0.2, 2),
                    "stirrups": round(total_steel_weight * 0.2, 2)
                }
            }
        }
        
        # Generate drawing URL
        drawing_url = f"/api/detailing/download/{request.model_id}/{request.design_id}.{request.output_format.lower()}"
        
        logger.info(f"Detailing generated: {len(bbs)} bar types, {total_steel_weight:.2f} kg steel")
        
        return DetailingResponse(
            model_id=request.model_id,
            bbs=bbs,
            boq=boq,
            drawing_url=drawing_url
        )
        
    except Exception as e:
        logger.error(f"Detailing generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Detailing failed: {str(e)}")

def _calculate_main_bar_length(design_id: int) -> float:
    """Calculate main reinforcement bar length"""
    # Simplified - in production would query design results
    base_length = 6000  # mm
    return base_length

def _calculate_main_bar_quantity(design_id: int) -> int:
    """Calculate number of main bars required"""
    # Simplified - in production would use design results
    return 4

def _calculate_distribution_length(design_id: int) -> float:
    """Calculate distribution bar length"""
    return 3000  # mm

def _calculate_distribution_quantity(design_id: int) -> int:
    """Calculate number of distribution bars"""
    return 8

def _calculate_stirrup_length(design_id: int) -> float:
    """Calculate stirrup length"""
    return 1200  # mm (perimeter)

def _calculate_stirrup_quantity(design_id: int) -> int:
    """Calculate number of stirrups"""
    # Based on spacing (e.g., 150mm c/c over 6m length)
    return int(6000 / 150) + 1

def _calculate_cutting_length(diameter: float, shape: str, hooks: str = "none") -> float:
    """Calculate cutting length including hooks and bends"""
    base_length = {
        "straight": 6000,
        "rectangular": 1200,
        "l_shape": 4000
    }.get(shape, 6000)
    
    # Add hook lengths
    hook_length = 0
    if hooks == "standard":
        hook_length = 40 * diameter  # 40d hook length
    elif hooks == "135_degree":
        hook_length = 10 * diameter  # 10d for 135° hook
    
    return base_length + hook_length

def _calculate_concrete_volume(design_id: int) -> float:
    """Calculate concrete volume in m³"""
    # Simplified - in production would use actual element dimensions
    # Example: 300mm x 450mm x 6000mm beam
    return (0.3 * 0.45 * 6.0)
