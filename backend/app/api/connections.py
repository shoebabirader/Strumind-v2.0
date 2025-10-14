from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.engine.steel_connections import SteelConnectionDesign

router = APIRouter()

class MomentConnectionRequest(BaseModel):
    M: float  # kNm
    V: float  # kN
    beam_depth: float  # mm
    connection_type: str  # "bolted" or "welded"
    bolt_diameter: float = 20  # mm
    n_bolts: int = 6
    flange_width: float = 200  # mm
    weld_size: float = 8  # mm

class ShearConnectionRequest(BaseModel):
    V: float  # kN
    bolt_diameter: float  # mm
    n_bolts: int
    edge_distance: float  # mm

class BasePlateRequest(BaseModel):
    P: float  # kN
    M: float  # kNm
    column_size: float  # mm
    concrete_grade: float  # MPa

@router.post("/moment-connection")
def design_moment_connection(request: MomentConnectionRequest):
    """Design moment connection"""
    try:
        designer = SteelConnectionDesign()
        
        if request.connection_type == "bolted":
            result = designer.moment_connection_bolted(
                request.M, request.V, request.beam_depth,
                request.bolt_diameter, request.n_bolts
            )
        else:  # welded
            result = designer.moment_connection_welded(
                request.M, request.V, request.beam_depth,
                request.flange_width, request.weld_size
            )
        
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/shear-connection")
def design_shear_connection(request: ShearConnectionRequest):
    """Design simple shear connection"""
    try:
        designer = SteelConnectionDesign()
        result = designer.shear_connection_simple(
            request.V, request.bolt_diameter,
            request.n_bolts, request.edge_distance
        )
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/base-plate")
def design_base_plate(request: BasePlateRequest):
    """Design column base plate"""
    try:
        designer = SteelConnectionDesign()
        result = designer.base_plate_design(
            request.P, request.M,
            request.column_size, request.concrete_grade
        )
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
