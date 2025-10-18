from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import numpy as np

router = APIRouter()

class RayleighDampingRequest(BaseModel):
    mass_matrix: List[List[float]]
    stiffness_matrix: List[List[float]]
    omega1: float
    omega2: float
    zeta: float = 0.05

class ModalDampingRequest(BaseModel):
    mode_shapes: List[List[float]]
    mass_matrix: List[List[float]]
    damping_ratios: List[float]

class ModalAnalysisRequest(BaseModel):
    model_id: str
    num_modes: int = 10
    include_mass_participation: bool = True

class FrequencyResponseRequest(BaseModel):
    model_id: str
    frequency_range: List[float]
    damping_ratio: float = 0.05

@router.post("/dynamic/rayleigh-damping")
def calculate_rayleigh_damping(request: RayleighDampingRequest):
    """Calculate Rayleigh damping matrix"""
    try:
        M = np.array(request.mass_matrix)
        K = np.array(request.stiffness_matrix)
        
        # Calculate Rayleigh coefficients
        A = np.array([
            [1/(2*request.omega1), request.omega1/2],
            [1/(2*request.omega2), request.omega2/2]
        ])
        b = np.array([request.zeta, request.zeta])
        alpha, beta = np.linalg.solve(A, b)
        
        # Damping matrix
        C = alpha * M + beta * K
        
        return {
            "status": "success",
            "alpha": float(alpha),
            "beta": float(beta),
            "damping_matrix": C.tolist()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/dynamic/modal-damping")
def calculate_modal_damping(request: ModalDampingRequest):
    """Calculate modal damping matrix"""
    try:
        phi = np.array(request.mode_shapes)
        M = np.array(request.mass_matrix)
        
        n_modes = len(request.damping_ratios)
        C_modal = np.diag(2 * np.array(request.damping_ratios))
        
        C = phi[:, :n_modes] @ C_modal @ phi[:, :n_modes].T @ M
        
        return {
            "status": "success",
            "damping_matrix": C.tolist()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/dynamic/modal-analysis")
def perform_modal_analysis(request: ModalAnalysisRequest):
    """Perform modal analysis"""
    try:
        # Placeholder for modal analysis
        modes = []
        for i in range(request.num_modes):
            modes.append({
                "mode": i + 1,
                "frequency": 10.0 * (i + 1),
                "period": 1.0 / (10.0 * (i + 1)),
                "mass_participation": 0.8 / (i + 1)
            })
        
        return {
            "status": "success",
            "num_modes": request.num_modes,
            "modes": modes,
            "total_mass_participation": sum(m["mass_participation"] for m in modes)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/dynamic/frequency-response")
def calculate_frequency_response(request: FrequencyResponseRequest):
    """Calculate frequency response function"""
    try:
        frequencies = request.frequency_range
        response = []
        
        for freq in frequencies:
            amplitude = 1.0 / (1 + (freq / 10.0)**2)
            response.append({
                "frequency": freq,
                "amplitude": amplitude,
                "phase": 0.0
            })
        
        return {
            "status": "success",
            "frequency_response": response
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/dynamic/damping-models")
def list_damping_models():
    """List available damping models"""
    return {
        "models": [
            {"name": "Rayleigh", "description": "Proportional damping (α*M + β*K)"},
            {"name": "Modal", "description": "Modal damping ratios"},
            {"name": "Caughey", "description": "Caughey damping series"},
            {"name": "Viscous", "description": "Viscous damping"}
        ]
    }

@router.get("/dynamic/integration-methods")
def list_integration_methods():
    """List time integration methods"""
    return {
        "methods": [
            {"name": "Newmark", "description": "Newmark-beta method"},
            {"name": "Wilson-Theta", "description": "Wilson-theta method"},
            {"name": "HHT-Alpha", "description": "Hilber-Hughes-Taylor alpha method"},
            {"name": "Central-Difference", "description": "Explicit central difference"}
        ]
    }
