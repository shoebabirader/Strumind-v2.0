from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
from app.engine.slab_design import SlabDesign

router = APIRouter()

class OneWaySlabRequest(BaseModel):
    span: float
    thickness: float
    loads: Dict[str, float]
    support_condition: str = "simply_supported"
    code: str = "IS456"

class TwoWaySlabRequest(BaseModel):
    lx: float
    ly: float
    thickness: float
    loads: Dict[str, float]
    support_condition: str = "all_edges_supported"
    code: str = "IS456"

class FlatSlabRequest(BaseModel):
    panel_size: float
    column_size: float
    thickness: float
    loads: Dict[str, float]
    code: str = "IS456"

@router.post("/slab-design/one-way")
def design_one_way_slab(request: OneWaySlabRequest):
    """Design one-way slab"""
    try:
        designer = SlabDesign(code=request.code)
        result = designer.one_way_slab_design(
            request.span,
            request.thickness,
            request.loads,
            request.support_condition
        )
        return {"status": "success", "design": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/slab-design/two-way")
def design_two_way_slab(request: TwoWaySlabRequest):
    """Design two-way slab"""
    try:
        designer = SlabDesign(code=request.code)
        result = designer.two_way_slab_design(
            request.lx,
            request.ly,
            request.thickness,
            request.loads,
            request.support_condition
        )
        return {"status": "success", "design": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/slab-design/flat-slab")
def design_flat_slab(request: FlatSlabRequest):
    """Design flat slab with punching shear check"""
    try:
        designer = SlabDesign(code=request.code)
        result = designer.flat_slab_design(
            request.panel_size,
            request.column_size,
            request.thickness,
            request.loads
        )
        return {"status": "success", "design": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/slab-design/codes")
def get_supported_slab_codes():
    """Get supported design codes for slabs"""
    return {
        "codes": [
            {"code": "IS456", "description": "Indian Standard for Concrete"},
            {"code": "ACI318", "description": "American Concrete Institute"},
            {"code": "BS8110", "description": "British Standard"},
            {"code": "Eurocode2", "description": "European Standard"}
        ]
    }
