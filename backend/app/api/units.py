from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from app.engine.units_system import UnitConverter

router = APIRouter()

class ConversionRequest(BaseModel):
    value: float
    from_unit: str
    to_unit: str
    quantity_type: str  # 'length', 'force', 'stress', 'moment'

class BatchConversionRequest(BaseModel):
    values: Dict[str, float]
    from_system: str  # 'SI', 'Imperial', 'US'
    to_system: str

@router.post("/units/convert")
def convert_units(request: ConversionRequest):
    """Convert between units"""
    try:
        converter = UnitConverter()
        converted_value = converter.convert(
            request.value,
            request.from_unit,
            request.to_unit,
            request.quantity_type
        )
        return {
            "status": "success",
            "original": {"value": request.value, "unit": request.from_unit},
            "converted": {"value": converted_value, "unit": request.to_unit}
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/units/batch-convert")
def batch_convert_units(request: BatchConversionRequest):
    """Convert multiple values between unit systems"""
    try:
        converter = UnitConverter()
        converted = {}
        for key, value in request.values.items():
            converted[key] = value  # Placeholder conversion
        
        return {
            "status": "success",
            "from_system": request.from_system,
            "to_system": request.to_system,
            "converted_values": converted
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/units/supported")
def get_supported_units():
    """Get all supported units"""
    return {
        "length": ["mm", "m", "cm", "in", "ft"],
        "force": ["N", "kN", "MN", "lbf", "kip"],
        "stress": ["Pa", "kPa", "MPa", "GPa", "psi", "ksi"],
        "moment": ["Nm", "kNm", "MNm", "lbf-in", "kip-ft"],
        "area": ["mm2", "m2", "in2", "ft2"],
        "volume": ["mm3", "m3", "in3", "ft3"]
    }

@router.get("/units/systems")
def get_unit_systems():
    """Get available unit systems"""
    return {
        "systems": [
            {
                "name": "SI",
                "description": "International System",
                "base_units": {
                    "length": "m",
                    "force": "N",
                    "stress": "Pa",
                    "moment": "Nm"
                }
            },
            {
                "name": "Imperial",
                "description": "Imperial System",
                "base_units": {
                    "length": "ft",
                    "force": "lbf",
                    "stress": "psi",
                    "moment": "lbf-ft"
                }
            }
        ]
    }
