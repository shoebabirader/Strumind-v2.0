from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.engine.design_codes_extended import (
    Eurocode2, BS8110, AS3600, GB50010, Eurocode3, BS5950
)

router = APIRouter()

class FlexuralDesignRequest(BaseModel):
    code: str  # EC2, BS8110, AS3600, GB50010
    M: float  # kNm
    b: float  # mm
    d: float  # mm
    fc: float  # MPa (fck for EC2, fcu for BS8110, fc for AS3600, fc for GB50010)
    fy: float  # MPa

class SteelDesignRequest(BaseModel):
    code: str  # EC3, BS5950
    N: float  # kN
    M: float  # kNm
    A: float  # mm²
    W_or_Z: float  # mm³ (W for EC3, Z for BS5950)
    fy: float  # MPa

@router.post("/concrete/flexure")
def design_concrete_flexure(request: FlexuralDesignRequest):
    """Design concrete member for flexure using various codes"""
    try:
        if request.code == "EC2":
            designer = Eurocode2()
            result = designer.flexural_design(
                request.M, request.b, request.d, request.fc, request.fy
            )
        elif request.code == "BS8110":
            designer = BS8110()
            result = designer.flexural_design(
                request.M, request.b, request.d, request.fc, request.fy
            )
        elif request.code == "AS3600":
            designer = AS3600()
            result = designer.flexural_design(
                request.M, request.b, request.d, request.fc, request.fy
            )
        elif request.code == "GB50010":
            designer = GB50010()
            result = designer.flexural_design(
                request.M, request.b, request.d, request.fc, request.fy
            )
        else:
            raise HTTPException(status_code=400, detail="Unsupported code")
        
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/steel/member")
def design_steel_member(request: SteelDesignRequest):
    """Design steel member using various codes"""
    try:
        if request.code == "EC3":
            designer = Eurocode3()
            result = designer.member_design(
                request.N, request.M, request.A, request.W_or_Z, request.fy
            )
        elif request.code == "BS5950":
            designer = BS5950()
            result = designer.member_design(
                request.N, request.M, request.A, request.W_or_Z, request.fy
            )
        else:
            raise HTTPException(status_code=400, detail="Unsupported code")
        
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/codes/list")
def list_supported_codes():
    """List all supported design codes"""
    return {
        "concrete_codes": [
            {
                "code": "IS456",
                "name": "IS 456:2000",
                "region": "India",
                "type": "Reinforced Concrete"
            },
            {
                "code": "ACI318",
                "name": "ACI 318",
                "region": "USA",
                "type": "Reinforced Concrete"
            },
            {
                "code": "EC2",
                "name": "Eurocode 2",
                "region": "Europe",
                "type": "Reinforced Concrete"
            },
            {
                "code": "BS8110",
                "name": "BS 8110",
                "region": "UK",
                "type": "Reinforced Concrete"
            },
            {
                "code": "AS3600",
                "name": "AS 3600",
                "region": "Australia",
                "type": "Reinforced Concrete"
            },
            {
                "code": "GB50010",
                "name": "GB 50010",
                "region": "China",
                "type": "Reinforced Concrete"
            }
        ],
        "steel_codes": [
            {
                "code": "IS800",
                "name": "IS 800:2007",
                "region": "India",
                "type": "Steel Structures"
            },
            {
                "code": "AISC360",
                "name": "AISC 360",
                "region": "USA",
                "type": "Steel Structures"
            },
            {
                "code": "EC3",
                "name": "Eurocode 3",
                "region": "Europe",
                "type": "Steel Structures"
            },
            {
                "code": "BS5950",
                "name": "BS 5950",
                "region": "UK",
                "type": "Steel Structures"
            }
        ],
        "seismic_codes": [
            {
                "code": "IS1893",
                "name": "IS 1893:2016",
                "region": "India"
            },
            {
                "code": "ASCE7",
                "name": "ASCE 7",
                "region": "USA"
            },
            {
                "code": "EC8",
                "name": "Eurocode 8",
                "region": "Europe"
            }
        ],
        "wind_codes": [
            {
                "code": "IS875",
                "name": "IS 875 Part 3:2015",
                "region": "India"
            },
            {
                "code": "ASCE7",
                "name": "ASCE 7",
                "region": "USA"
            },
            {
                "code": "AS1170",
                "name": "AS 1170.2",
                "region": "Australia"
            },
            {
                "code": "EC1",
                "name": "Eurocode 1",
                "region": "Europe"
            }
        ],
        "total_codes": 16
    }
