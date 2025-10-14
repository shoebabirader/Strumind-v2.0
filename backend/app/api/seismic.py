from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from app.engine.seismic import SeismicAnalysis, SeismicCode, SeismicZone, SoilType
import numpy as np

router = APIRouter()

class SeismicParameters(BaseModel):
    code: str = "IS1893"  # IS1893, ASCE7, EC8
    zone: str = "ZONE_IV"  # ZONE_II, ZONE_III, ZONE_IV, ZONE_V
    importance_factor: float = 1.0
    response_reduction_factor: float = 5.0
    soil_type: str = "MEDIUM"  # ROCK, MEDIUM, SOFT

class BaseShearRequest(BaseModel):
    parameters: SeismicParameters
    total_weight: float  # in kN
    building_height: float  # in meters
    building_type: str = "RC_MRF"  # RC_MRF, STEEL_MRF, RC_SHEAR_WALL

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
