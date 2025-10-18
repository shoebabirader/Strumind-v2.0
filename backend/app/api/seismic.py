from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator, Field
from typing import List, Dict, Optional
from app.engine.seismic import SeismicAnalysis, SeismicCode, SeismicZone, SoilType
from app.core.validators import EngineeringValidator, SecurityValidator
import numpy as np
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class SeismicParameters(BaseModel):
    code: str = Field(default="IS1893", description="Seismic design code")
    zone: str = Field(default="ZONE_IV", description="Seismic zone")
    importance_factor: float = Field(default=1.0, ge=0.8, le=2.0, description="Importance factor")
    response_reduction_factor: float = Field(default=5.0, ge=1.0, le=10.0, description="Response reduction factor")
    soil_type: str = Field(default="MEDIUM", description="Soil type")
    
    @validator('code')
    def validate_code(cls, v):
        """Validate seismic code"""
        allowed_codes = ['IS1893', 'ASCE7', 'EC8', 'IBC']
        v = SecurityValidator.sanitize_string(v, max_length=20).upper()
        if v not in allowed_codes:
            raise ValueError(f"Invalid seismic code. Allowed: {allowed_codes}")
        return v
    
    @validator('zone')
    def validate_zone(cls, v):
        """Validate seismic zone"""
        allowed_zones = ['ZONE_II', 'ZONE_III', 'ZONE_IV', 'ZONE_V']
        v = SecurityValidator.sanitize_string(v, max_length=20).upper()
        if v not in allowed_zones:
            raise ValueError(f"Invalid zone. Allowed: {allowed_zones}")
        return v
    
    @validator('soil_type')
    def validate_soil_type(cls, v):
        """Validate soil type"""
        allowed_types = ['ROCK', 'MEDIUM', 'SOFT', 'VERY_SOFT']
        v = SecurityValidator.sanitize_string(v, max_length=20).upper()
        if v not in allowed_types:
            raise ValueError(f"Invalid soil type. Allowed: {allowed_types}")
        return v

class BaseShearRequest(BaseModel):
    parameters: SeismicParameters
    total_weight: float = Field(gt=0, le=1e9, description="Total weight in kN")
    building_height: float = Field(gt=0, le=1000, description="Building height in meters")
    building_type: str = Field(default="RC_MRF", description="Building structural system")
    
    @validator('total_weight')
    def validate_weight(cls, v):
        """Validate total weight"""
        return EngineeringValidator.validate_load(v, 'force')
    
    @validator('building_height')
    def validate_height(cls, v):
        """Validate building height"""
        return EngineeringValidator.validate_dimension(v, 'height')
    
    @validator('building_type')
    def validate_building_type(cls, v):
        """Validate building type"""
        allowed_types = ['RC_MRF', 'STEEL_MRF', 'RC_SHEAR_WALL', 'STEEL_BRACED', 'MASONRY']
        v = SecurityValidator.sanitize_string(v, max_length=50).upper()
        if v not in allowed_types:
            raise ValueError(f"Invalid building type. Allowed: {allowed_types}")
        return v

class ResponseSpectrumRequest(BaseModel):
    parameters: SeismicParameters
    mass_matrix: List[List[float]]
    stiffness_matrix: List[List[float]]
    damping_ratio: float = 0.05

class StoryDriftRequest(BaseModel):
    story_displacements: List[float]  # in mm
    story_heights: List[float]  # in mm

class LoadDistributionRequest(BaseModel):
    base_shear: float  # in kN
    story_weights: List[float]  # in kN
    story_heights: List[float]  # in m

@router.post("/base-shear")
def calculate_base_shear(request: BaseShearRequest):
    """Calculate seismic base shear"""
    try:
        # Initialize seismic analysis
        code = SeismicCode[request.parameters.code]
        analyzer = SeismicAnalysis(code)
        
        # Set parameters
        zone = SeismicZone[request.parameters.zone]
        soil = SoilType[request.parameters.soil_type]
        
        analyzer.set_parameters(
            zone=zone,
            importance=request.parameters.importance_factor,
            response_reduction=request.parameters.response_reduction_factor,
            soil=soil
        )
        
        # Calculate time period
        time_period = analyzer.calculate_time_period(
            request.building_height,
            request.building_type
        )
        
        # Calculate base shear
        result = analyzer.calculate_base_shear(
            request.total_weight,
            time_period
        )
        
        return {
            "status": "success",
            "results": result,
            "building_height": request.building_height,
            "total_weight": request.total_weight
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/response-spectrum")
def response_spectrum_analysis(request: ResponseSpectrumRequest):
    """Perform response spectrum analysis"""
    try:
        # Initialize seismic analysis
        code = SeismicCode[request.parameters.code]
        analyzer = SeismicAnalysis(code)
        
        # Set parameters
        zone = SeismicZone[request.parameters.zone]
        soil = SoilType[request.parameters.soil_type]
        
        analyzer.set_parameters(
            zone=zone,
            importance=request.parameters.importance_factor,
            response_reduction=request.parameters.response_reduction_factor,
            soil=soil
        )
        
        # Convert to numpy arrays
        M = np.array(request.mass_matrix)
        K = np.array(request.stiffness_matrix)
        
        # Perform analysis
        result = analyzer.response_spectrum_analysis(M, K, request.damping_ratio)
        
        return {
            "status": "success",
            "results": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/story-drift-check")
def check_story_drift(request: StoryDriftRequest):
    """Check story drift limits"""
    try:
        analyzer = SeismicAnalysis()
        result = analyzer.story_drift_check(
            request.story_displacements,
            request.story_heights
        )
        
        return {
            "status": "success",
            "results": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/load-distribution")
def distribute_seismic_loads(request: LoadDistributionRequest):
    """Distribute base shear to stories"""
    try:
        analyzer = SeismicAnalysis()
        result = analyzer.seismic_load_distribution(
            request.base_shear,
            request.story_weights,
            request.story_heights
        )
        
        return {
            "status": "success",
            "results": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/torsional-irregularity")
def check_torsional_irregularity(max_drift: float, avg_drift: float):
    """Check torsional irregularity"""
    try:
        analyzer = SeismicAnalysis()
        result = analyzer.torsional_irregularity_check(max_drift, avg_drift)
        
        return {
            "status": "success",
            "results": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/soft-story-check")
def check_soft_story(story_stiffnesses: List[float]):
    """Check for soft story"""
    try:
        analyzer = SeismicAnalysis()
        result = analyzer.soft_story_check(story_stiffnesses)
        
        return {
            "status": "success",
            "results": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/codes")
def get_supported_codes():
    """Get list of supported seismic codes"""
    return {
        "codes": [
            {
                "code": "IS1893",
                "name": "IS 1893:2016",
                "country": "India",
                "zones": ["ZONE_II", "ZONE_III", "ZONE_IV", "ZONE_V"]
            },
            {
                "code": "ASCE7",
                "name": "ASCE 7",
                "country": "USA",
                "zones": ["Custom based on location"]
            },
            {
                "code": "EC8",
                "name": "Eurocode 8",
                "country": "Europe",
                "zones": ["Custom based on location"]
            }
        ]
    }

@router.get("/parameters/defaults")
def get_default_parameters():
    """Get default seismic parameters"""
    return {
        "IS1893": {
            "zone": "ZONE_IV",
            "importance_factor": 1.0,
            "response_reduction_factor": 5.0,
            "soil_type": "MEDIUM",
            "damping_ratio": 0.05
        },
        "ASCE7": {
            "importance_factor": 1.0,
            "response_reduction_factor": 8.0,
            "soil_type": "MEDIUM",
            "damping_ratio": 0.05
        }
    }
