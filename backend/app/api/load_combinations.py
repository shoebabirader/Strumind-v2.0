from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from app.engine.load_combinations import LoadCombinationGenerator, EnvelopeGenerator

router = APIRouter()

class LoadCombinationRequest(BaseModel):
    code: str
    load_cases: Dict[str, float]
    limit_state: str = "ultimate"

class EnvelopeRequest(BaseModel):
    results: List[Dict[str, float]]
    result_type: str  # 'moment', 'shear', 'axial', 'displacement'

@router.post("/load-combinations/generate")
def generate_load_combinations(request: LoadCombinationRequest):
    """Generate load combinations per design code"""
    try:
        generator = LoadCombinationGenerator(request.code)
        combinations = generator.generate_combinations(
            request.load_cases,
            request.limit_state
        )
        return {"status": "success", "combinations": combinations}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/load-combinations/envelope")
def generate_envelope(request: EnvelopeRequest):
    """Generate result envelope from multiple combinations"""
    try:
        envelope_gen = EnvelopeGenerator()
        envelope = envelope_gen.generate_envelope(
            request.results,
            request.result_type
        )
        return {"status": "success", "envelope": envelope}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/load-combinations/codes")
def get_supported_codes():
    """Get supported design codes"""
    return {
        "codes": [
            {"code": "IS456", "description": "Indian Standard - Concrete"},
            {"code": "IS800", "description": "Indian Standard - Steel"},
            {"code": "ASCE7", "description": "American Standard"},
            {"code": "Eurocode", "description": "European Standard"},
            {"code": "BS8110", "description": "British Standard"}
        ]
    }

@router.get("/load-combinations/factors/{code}")
def get_load_factors(code: str, limit_state: str = "ultimate"):
    """Get load factors for specific code"""
    try:
        factors = {
            "IS456": {
                "dead": 1.5,
                "live": 1.5,
                "wind": 1.5,
                "seismic": 1.5
            },
            "ASCE7": {
                "dead": 1.2,
                "live": 1.6,
                "wind": 1.0,
                "seismic": 1.0
            }
        }
        return {
            "code": code,
            "limit_state": limit_state,
            "factors": factors.get(code, {})
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
