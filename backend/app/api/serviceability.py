from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.engine.serviceability_checks import ServiceabilityChecks

router = APIRouter()

class DeflectionCheckRequest(BaseModel):
    span: float
    actual_deflection: float
    member_type: str = "beam"
    support_condition: str = "simply_supported"
    loading_type: str = "live"

class CrackWidthCheckRequest(BaseModel):
    stress_steel: float
    cover: float
    bar_diameter: float
    spacing: float
    exposure_condition: str = "moderate"

class VibrationCheckRequest(BaseModel):
    natural_frequency: float
    floor_type: str = "office"
    damping_ratio: float = 0.05

class PunchingShearCheckRequest(BaseModel):
    column_size: float
    slab_thickness: float
    column_load: float
    fck: Optional[float] = None

class FatigueCheckRequest(BaseModel):
    stress_range: float
    n_cycles: float
    material: str = "steel"
    detail_category: str = "C"

class SlendernessCheckRequest(BaseModel):
    length: float
    radius_of_gyration: float
    member_type: str = "column"
    end_conditions: str = "pinned_pinned"

@router.post("/deflection")
def check_deflection(request: DeflectionCheckRequest):
    """Check deflection limits"""
    try:
        checker = ServiceabilityChecks()
        result = checker.deflection_check(
            request.span,
            request.actual_deflection,
            request.member_type,
            request.support_condition,
            request.loading_type
        )
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/crack-width")
def check_crack_width(request: CrackWidthCheckRequest):
    """Check crack width limits"""
    try:
        checker = ServiceabilityChecks()
        result = checker.crack_width_check(
            request.stress_steel,
            request.cover,
            request.bar_diameter,
            request.spacing,
            request.exposure_condition
        )
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/vibration")
def check_vibration(request: VibrationCheckRequest):
    """Check vibration limits"""
    try:
        checker = ServiceabilityChecks()
        result = checker.vibration_check(
            request.natural_frequency,
            request.floor_type,
            request.damping_ratio
        )
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/punching-shear")
def check_punching_shear(request: PunchingShearCheckRequest):
    """Check punching shear"""
    try:
        checker = ServiceabilityChecks()
        result = checker.punching_shear_check(
            request.column_size,
            request.slab_thickness,
            request.column_load,
            request.fck
        )
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/fatigue")
def check_fatigue(request: FatigueCheckRequest):
    """Check fatigue"""
    try:
        checker = ServiceabilityChecks()
        result = checker.fatigue_check(
            request.stress_range,
            request.n_cycles,
            request.material,
            request.detail_category
        )
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/slenderness")
def check_slenderness(request: SlendernessCheckRequest):
    """Check slenderness ratio"""
    try:
        checker = ServiceabilityChecks()
        result = checker.slenderness_check(
            request.length,
            request.radius_of_gyration,
            request.member_type,
            request.end_conditions
        )
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
