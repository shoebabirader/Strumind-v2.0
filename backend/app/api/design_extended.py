from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict
import logging
from app.engine.design_codes.is456_concrete import IS456ConcreteDesign, quick_flexural_design, quick_shear_design
from app.engine.design_codes.is800_steel import IS800SteelDesign, quick_tension_design, quick_compression_design
from app.core.errors import UnsupportedDesignCodeError, error_to_http_response

router = APIRouter()
logger = logging.getLogger(__name__)

# IS 456 Concrete Design Models
class IS456FlexuralDesignRequest(BaseModel):
    M: float = Field(..., description="Design moment (kN·m)")
    b: float = Field(..., description="Width of beam (mm)")
    d: float = Field(..., description="Effective depth (mm)")
    fck: float = Field(25, description="Characteristic strength of concrete (MPa)")
    fy: float = Field(415, description="Characteristic strength of steel (MPa)")
    d_prime: Optional[float] = Field(None, description="Cover to compression steel (mm)")

class IS456ShearDesignRequest(BaseModel):
    V: float = Field(..., description="Design shear force (kN)")
    b: float = Field(..., description="Width of beam (mm)")
    d: float = Field(..., description="Effective depth (mm)")
    Ast: float = Field(..., description="Area of tension steel (mm²)")
    fck: float = Field(25, description="Characteristic strength of concrete (MPa)")
    fy: float = Field(415, description="Characteristic strength of steel (MPa)")

class IS456TorsionDesignRequest(BaseModel):
    T: float = Field(..., description="Design torsional moment (kN·m)")
    b: float = Field(..., description="Width of beam (mm)")
    D: float = Field(..., description="Overall depth (mm)")
    Ast: float = Field(..., description="Area of tension steel (mm²)")
    Asc: float = Field(0, description="Area of compression steel (mm²)")
    fck: float = Field(25, description="Characteristic strength of concrete (MPa)")
    fy: float = Field(415, description="Characteristic strength of steel (MPa)")

# IS 800 Steel Design Models
class IS800TensionDesignRequest(BaseModel):
    T: float = Field(..., description="Design tension force (kN)")
    Ag: float = Field(..., description="Gross area (mm²)")
    An: float = Field(..., description="Net area (mm²)")
    Anc: Optional[float] = Field(None, description="Net area for block shear (mm²)")
    Avg: Optional[float] = Field(None, description="Gross shear area (mm²)")
    fy: float = Field(250, description="Yield strength (MPa)")
    fu: float = Field(410, description="Ultimate strength (MPa)")

class IS800CompressionDesignRequest(BaseModel):
    P: float = Field(..., description="Design compression force (kN)")
    L: float = Field(..., description="Unsupported length (mm)")
    section: Dict = Field(..., description="Section properties (A, rx, ry, Iz, Iy)")
    buckling_class: str = Field("b", description="Buckling class (a, b, c, d)")
    Kx: float = Field(1.0, description="Effective length factor x-axis")
    Ky: float = Field(1.0, description="Effective length factor y-axis")
    fy: float = Field(250, description="Yield strength (MPa)")
    fu: float = Field(410, description="Ultimate strength (MPa)")

class IS800BeamDesignRequest(BaseModel):
    M: float = Field(..., description="Design moment (kN·m)")
    V: float = Field(..., description="Design shear (kN)")
    section: Dict = Field(..., description="Section properties")
    Lb: Optional[float] = Field(None, description="Laterally unsupported length (mm)")
    lateral_support: str = Field("full", description="Lateral support type")
    fy: float = Field(250, description="Yield strength (MPa)")
    fu: float = Field(410, description="Ultimate strength (MPa)")

# Legacy models for compatibility
class FlexuralDesignRequest(BaseModel):
    code: str  # IS456, EC2, BS8110, AS3600, GB50010
    M: float  # kNm
    b: float  # mm
    d: float  # mm
    fc: float  # MPa (fck for IS456/EC2, fcu for BS8110, fc for AS3600/GB50010)
    fy: float  # MPa

class SteelDesignRequest(BaseModel):
    code: str  # IS800, EC3, BS5950
    N: float  # kN
    M: float  # kNm
    A: float  # mm²
    W_or_Z: float  # mm³
    fy: float  # MPa

# IS 456:2000 Concrete Design Endpoints
@router.post("/is456/flexural")
def is456_flexural_design(request: IS456FlexuralDesignRequest):
    """
    Design concrete beam for flexure per IS 456:2000
    
    Implements:
    - Singly reinforced design (Clause 38)
    - Doubly reinforced design (Clause 38.1)
    - Minimum and maximum steel checks
    - Bar arrangement suggestions
    """
    try:
        designer = IS456ConcreteDesign(request.fck, request.fy)
        
        # Try singly reinforced first
        result = designer.flexural_design_singly_reinforced(
            request.M, request.b, request.d
        )
        
        # If doubly reinforced required
        if result.get('status') == 'doubly_reinforced_required':
            result = designer.flexural_design_doubly_reinforced(
                request.M, request.b, request.d, request.d_prime
            )
        
        logger.info(f"IS 456 flexural design: M={request.M} kN·m, status={result['status']}")
        return {"status": "success", "code": "IS456", "results": result}
        
    except Exception as e:
        logger.error(f"IS 456 flexural design error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/is456/shear")
def is456_shear_design(request: IS456ShearDesignRequest):
    """
    Design concrete beam for shear per IS 456:2000 Clause 40
    
    Implements:
    - Nominal shear stress calculation
    - Permissible shear stress (Table 19)
    - Shear reinforcement design
    - Stirrup spacing calculation
    """
    try:
        designer = IS456ConcreteDesign(request.fck, request.fy)
        result = designer.shear_design(request.V, request.b, request.d, request.Ast)
        
        logger.info(f"IS 456 shear design: V={request.V} kN, status={result['status']}")
        return {"status": "success", "code": "IS456", "results": result}
        
    except Exception as e:
        logger.error(f"IS 456 shear design error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/is456/torsion")
def is456_torsion_design(request: IS456TorsionDesignRequest):
    """
    Design concrete beam for torsion per IS 456:2000 Clause 41
    
    Implements:
    - Torsional shear stress calculation
    - Check if torsion can be ignored
    - Longitudinal and transverse steel for torsion
    """
    try:
        designer = IS456ConcreteDesign(request.fck, request.fy)
        result = designer.torsion_design(
            request.T, request.b, request.D, request.Ast, request.Asc
        )
        
        logger.info(f"IS 456 torsion design: T={request.T} kN·m, status={result['status']}")
        return {"status": "success", "code": "IS456", "results": result}
        
    except Exception as e:
        logger.error(f"IS 456 torsion design error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# IS 800:2007 Steel Design Endpoints
@router.post("/is800/tension")
def is800_tension_design(request: IS800TensionDesignRequest):
    """
    Design steel tension member per IS 800:2007 Clause 6
    
    Implements:
    - Yielding check (Clause 6.2)
    - Rupture check (Clause 6.3)
    - Block shear check (Clause 6.4)
    """
    try:
        designer = IS800SteelDesign(request.fy, request.fu)
        result = designer.tension_member_design(
            request.T, request.Ag, request.An, request.Anc, request.Avg
        )
        
        logger.info(f"IS 800 tension design: T={request.T} kN, status={result['status']}")
        return {"status": "success", "code": "IS800", "results": result}
        
    except Exception as e:
        logger.error(f"IS 800 tension design error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/is800/compression")
def is800_compression_design(request: IS800CompressionDesignRequest):
    """
    Design steel compression member per IS 800:2007 Clause 7
    
    Implements:
    - Slenderness ratio calculation
    - Buckling curve selection (Table 10)
    - Design compressive strength
    - Effective length factors
    """
    try:
        from app.engine.design_codes.is800_steel import BucklingClass
        
        designer = IS800SteelDesign(request.fy, request.fu)
        
        # Convert buckling class string to enum
        buckling_class = BucklingClass(request.buckling_class)
        
        result = designer.compression_member_design(
            request.P, request.L, request.section, buckling_class,
            request.Kx, request.Ky
        )
        
        logger.info(f"IS 800 compression design: P={request.P} kN, status={result['status']}")
        return {"status": "success", "code": "IS800", "results": result}
        
    except Exception as e:
        logger.error(f"IS 800 compression design error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/is800/beam")
def is800_beam_design(request: IS800BeamDesignRequest):
    """
    Design steel beam per IS 800:2007 Clause 8
    
    Implements:
    - Bending strength (Clause 8.2)
    - Shear strength (Clause 8.4)
    - Lateral-torsional buckling (Clause 8.2.2)
    - Interaction check for high shear
    """
    try:
        designer = IS800SteelDesign(request.fy, request.fu)
        result = designer.beam_design(
            request.M, request.V, request.section,
            request.Lb, request.lateral_support
        )
        
        logger.info(f"IS 800 beam design: M={request.M} kN·m, V={request.V} kN, status={result['status']}")
        return {"status": "success", "code": "IS800", "results": result}
        
    except Exception as e:
        logger.error(f"IS 800 beam design error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# Legacy endpoint for backward compatibility
@router.post("/concrete/flexure")
def design_concrete_flexure(request: FlexuralDesignRequest):
    """Design concrete member for flexure using various codes (legacy endpoint)"""
    try:
        if request.code == "IS456":
            designer = IS456ConcreteDesign(request.fc, request.fy)
            result = designer.flexural_design_singly_reinforced(
                request.M, request.b, request.d
            )
        else:
            raise UnsupportedDesignCodeError(request.code)
        
        return {"status": "success", "results": result}
    except UnsupportedDesignCodeError as e:
        response = error_to_http_response(e)
        raise HTTPException(status_code=response['status_code'], detail=response['detail'])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/steel/member")
def design_steel_member(request: SteelDesignRequest):
    """Design steel member using various codes (legacy endpoint)"""
    try:
        if request.code == "IS800":
            designer = IS800SteelDesign(request.fy, 410)  # Assume fu
            # Simplified - assume tension if N > 0
            result = designer.tension_member_design(request.N, request.A, request.A * 0.9)
        else:
            raise UnsupportedDesignCodeError(request.code)
        
        return {"status": "success", "results": result}
    except UnsupportedDesignCodeError as e:
        response = error_to_http_response(e)
        raise HTTPException(status_code=response['status_code'], detail=response['detail'])
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
