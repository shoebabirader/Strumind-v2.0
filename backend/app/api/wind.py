from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from app.engine.wind import WindAnalysis, WindCode, TerrainCategory, BuildingClass

router = APIRouter()

class WindParameters(BaseModel):
    code: str = "IS875"  # IS875, ASCE7, AS1170, EC1
    basic_wind_speed: float = 44.0  # m/s for IS875, mph for ASCE7
    terrain_category: int = 2  # 1, 2, 3, 4
    building_class: str = "B"  # A, B, C
    risk_coefficient: float = 1.0
    topography_factor: float = 1.0

class WindPressureRequest(BaseModel):
    parameters: WindParameters
    height: float  # in meters
    building_dimensions: Dict  # width, depth, height

class WindForceRequest(BaseModel):
    pressures: List[float]  # N/m²
    areas: List[float]  # m²
    heights: List[float]  # m

class GustFactorRequest(BaseModel):
    height: float  # m
    width: float  # m
    natural_frequency: Optional[float] = None  # Hz

class DynamicResponseRequest(BaseModel):
    parameters: WindParameters
    height: float  # m
    width: float  # m
    depth: float  # m
    mass_per_floor: float  # kg
    damping_ratio: float = 0.01

class LoadCombinationRequest(BaseModel):
    wind_force: float  # kN
    dead_load: float  # kN
    live_load: float  # kN
    code: str = "IS875"

class CladdingPressureRequest(BaseModel):
    parameters: WindParameters
    height: float  # m
    zone: str = "interior"  # corner, edge, interior

@router.post("/design-pressure")
def calculate_design_pressure(request: WindPressureRequest):
    """Calculate design wind pressure"""
    try:
        # Initialize wind analysis
        code = WindCode[request.parameters.code]
        analyzer = WindAnalysis(code)
        
        # Set parameters
        terrain = TerrainCategory(request.parameters.terrain_category)
        building_class = BuildingClass[request.parameters.building_class]
        
        analyzer.set_parameters(
            basic_wind_speed=request.parameters.basic_wind_speed,
            terrain=terrain,
            building_class=building_class,
            risk_coeff=request.parameters.risk_coefficient,
            topography=request.parameters.topography_factor
        )
        
        # Calculate pressure
        result = analyzer.calculate_design_wind_pressure(
            request.height,
            request.building_dimensions
        )
        
        return {
            "status": "success",
            "results": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/wind-forces")
def calculate_wind_forces(request: WindForceRequest):
    """Calculate wind forces on building"""
    try:
        analyzer = WindAnalysis()
        result = analyzer.calculate_wind_forces(
            request.pressures,
            request.areas,
            request.heights
        )
        
        return {
            "status": "success",
            "results": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/gust-factor")
def calculate_gust_factor(request: GustFactorRequest):
    """Calculate gust effect factor"""
    try:
        analyzer = WindAnalysis()
        result = analyzer.gust_factor_analysis(
            request.height,
            request.width,
            request.natural_frequency
        )
        
        return {
            "status": "success",
            "results": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/along-wind-response")
def calculate_along_wind(request: DynamicResponseRequest):
    """Calculate along-wind dynamic response"""
    try:
        # Initialize wind analysis
        code = WindCode[request.parameters.code]
        analyzer = WindAnalysis(code)
        
        # Set parameters
        terrain = TerrainCategory(request.parameters.terrain_category)
        building_class = BuildingClass[request.parameters.building_class]
        
        analyzer.set_parameters(
            basic_wind_speed=request.parameters.basic_wind_speed,
            terrain=terrain,
            building_class=building_class,
            risk_coeff=request.parameters.risk_coefficient,
            topography=request.parameters.topography_factor
        )
        
        # Calculate response
        result = analyzer.along_wind_response(
            request.height,
            request.width,
            request.depth,
            request.mass_per_floor,
            request.damping_ratio
        )
        
        return {
            "status": "success",
            "results": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/across-wind-response")
def calculate_across_wind(request: DynamicResponseRequest):
    """Calculate across-wind (vortex shedding) response"""
    try:
        # Initialize wind analysis
        code = WindCode[request.parameters.code]
        analyzer = WindAnalysis(code)
        
        # Set parameters
        terrain = TerrainCategory(request.parameters.terrain_category)
        building_class = BuildingClass[request.parameters.building_class]
        
        analyzer.set_parameters(
            basic_wind_speed=request.parameters.basic_wind_speed,
            terrain=terrain,
            building_class=building_class,
            risk_coeff=request.parameters.risk_coefficient,
            topography=request.parameters.topography_factor
        )
        
        # Calculate response
        result = analyzer.across_wind_response(
            request.height,
            request.width,
            request.depth,
            request.mass_per_floor,
            request.damping_ratio
        )
        
        return {
            "status": "success",
            "results": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/load-combinations")
def generate_load_combinations(request: LoadCombinationRequest):
    """Generate wind load combinations"""
    try:
        analyzer = WindAnalysis()
        result = analyzer.wind_load_combinations(
            request.wind_force,
            request.dead_load,
            request.live_load,
            request.code
        )
        
        return {
            "status": "success",
            "results": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/cladding-pressure")
def calculate_cladding_pressure(request: CladdingPressureRequest):
    """Calculate cladding and component pressures"""
    try:
        # Initialize wind analysis
        code = WindCode[request.parameters.code]
        analyzer = WindAnalysis(code)
        
        # Set parameters
        terrain = TerrainCategory(request.parameters.terrain_category)
        building_class = BuildingClass[request.parameters.building_class]
        
        analyzer.set_parameters(
            basic_wind_speed=request.parameters.basic_wind_speed,
            terrain=terrain,
            building_class=building_class,
            risk_coeff=request.parameters.risk_coefficient,
            topography=request.parameters.topography_factor
        )
        
        # Calculate pressure
        result = analyzer.cladding_pressure(
            request.height,
            request.zone
        )
        
        return {
            "status": "success",
            "results": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/codes")
def get_supported_codes():
    """Get list of supported wind codes"""
    return {
        "codes": [
            {
                "code": "IS875",
                "name": "IS 875 Part 3:2015",
                "country": "India",
                "unit": "m/s",
                "terrain_categories": [1, 2, 3, 4]
            },
            {
                "code": "ASCE7",
                "name": "ASCE 7",
                "country": "USA",
                "unit": "mph",
                "exposure_categories": ["B", "C", "D"]
            },
            {
                "code": "AS1170",
                "name": "AS 1170.2",
                "country": "Australia",
                "unit": "m/s",
                "terrain_categories": [1, 2, 3, 4]
            },
            {
                "code": "EC1",
                "name": "Eurocode 1",
                "country": "Europe",
                "unit": "m/s",
                "terrain_categories": [0, 1, 2, 3, 4]
            }
        ]
    }

@router.get("/parameters/defaults")
def get_default_parameters():
    """Get default wind parameters"""
    return {
        "IS875": {
            "basic_wind_speed": 44.0,
            "terrain_category": 2,
            "building_class": "B",
            "risk_coefficient": 1.0,
            "topography_factor": 1.0
        },
        "ASCE7": {
            "basic_wind_speed": 115.0,  # mph
            "exposure": "B",
            "importance_factor": 1.0,
            "topography_factor": 1.0
        }
    }

@router.get("/wind-zones/india")
def get_india_wind_zones():
    """Get basic wind speeds for Indian cities"""
    return {
        "zones": {
            "Mumbai": 44,
            "Chennai": 50,
            "Kolkata": 50,
            "Delhi": 47,
            "Bangalore": 33,
            "Hyderabad": 44,
            "Ahmedabad": 47,
            "Pune": 39,
            "Visakhapatnam": 55,
            "Coastal_Areas": 50
        },
        "unit": "m/s",
        "note": "Basic wind speeds at 10m height in terrain category 2"
    }
