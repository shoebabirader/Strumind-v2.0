"""
Advanced Analysis API Endpoints
P-Delta, Buckling, and Result Post-Processing
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import logging
import numpy as np
from app.engine.advanced_analysis import PDeltaAnalysis, BucklingAnalysis, ResultsPostProcessor
from app.engine.analysis import StructuralAnalysis
from app.engine.geometry import GeometryEngine

router = APIRouter()
logger = logging.getLogger(__name__)


class PDeltaAnalysisRequest(BaseModel):
    """Request model for P-Delta analysis"""
    project_id: int
    load_case: str = Field(..., description="Load case name")
    loads: Dict = Field(..., description="Load vector")
    restraints: Dict = Field(..., description="Boundary conditions")
    material_props: Dict = Field(..., description="Material properties")
    section_props: Dict = Field(..., description="Section properties")
    max_iterations: int = Field(50, description="Maximum iterations")
    tolerance: float = Field(1e-4, description="Convergence tolerance")


class BucklingAnalysisRequest(BaseModel):
    """Request model for buckling analysis"""
    project_id: int
    reference_loads: Dict = Field(..., description="Reference load pattern")
    restraints: Dict = Field(..., description="Boundary conditions")
    material_props: Dict = Field(..., description="Material properties")
    section_props: Dict = Field(..., description="Section properties")
    n_modes: int = Field(10, description="Number of buckling modes")


class StressCalculationRequest(BaseModel):
    """Request model for stress calculation"""
    element_forces: Dict = Field(..., description="Element forces from analysis")
    section_props: Dict = Field(..., description="Section properties")


class UtilizationRatioRequest(BaseModel):
    """Request model for utilization ratio calculation"""
    element_stresses: Dict = Field(..., description="Element stresses")
    material_props: Dict = Field(..., description="Material properties")
    threshold: float = Field(0.95, description="Critical member threshold")


@router.post("/pdelta")
def run_pdelta_analysis(request: PDeltaAnalysisRequest):
    """
    Perform P-Delta (second-order) analysis
    
    P-Delta analysis accounts for geometric nonlinearity due to axial forces.
    It iteratively updates the stiffness matrix to include geometric stiffness
    effects until convergence is achieved.
    
    Returns:
    - Displacements including P-Delta effects
    - Element forces
    - Stability indices
    - Convergence information
    """
    try:
        logger.info(f"Starting P-Delta analysis for project {request.project_id}")
        
        # Initialize geometry and analysis engines
        # Note: In production, load from database
        geom = GeometryEngine()
        analysis = StructuralAnalysis(geom)
        
        # Initialize P-Delta analysis
        pdelta = PDeltaAnalysis(geom, analysis)
        pdelta.max_iterations = request.max_iterations
        pdelta.tolerance = request.tolerance
        
        # Convert loads dict to numpy array
        # Note: Proper conversion needed based on your data structure
        loads = np.array(list(request.loads.values()))
        
        # Run P-Delta analysis
        results = pdelta.pdelta_analysis(
            loads,
            request.restraints,
            request.material_props,
            request.section_props
        )
        
        logger.info(f"P-Delta analysis completed. Converged: {results['converged']}, Iterations: {results['iterations']}")
        
        return {
            "status": "success",
            "analysis_type": "P-Delta",
            "converged": results['converged'],
            "iterations": results['iterations'],
            "displacements": results['displacements'].tolist(),
            "reactions": results['reactions'].tolist(),
            "element_forces": results['element_forces'],
            "stability_indices": results['stability_indices']
        }
        
    except Exception as e:
        logger.error(f"P-Delta analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"P-Delta analysis failed: {str(e)}")


@router.post("/buckling")
def run_buckling_analysis(request: BucklingAnalysisRequest):
    """
    Perform eigenvalue buckling analysis
    
    Buckling analysis determines the critical load factors at which the
    structure becomes unstable. It solves the eigenvalue problem:
    (K + λ * Kg) * φ = 0
    
    Returns:
    - Critical load factors (eigenvalues)
    - Buckling mode shapes (eigenvectors)
    - Stability assessment
    """
    try:
        logger.info(f"Starting buckling analysis for project {request.project_id}")
        
        # Initialize engines
        geom = GeometryEngine()
        analysis = StructuralAnalysis(geom)
        
        # Initialize buckling analysis
        buckling = BucklingAnalysis(geom, analysis)
        
        # Convert reference loads
        reference_loads = np.array(list(request.reference_loads.values()))
        
        # Run buckling analysis
        results = buckling.buckling_analysis(
            request.material_props,
            request.section_props,
            request.restraints,
            reference_loads,
            request.n_modes
        )
        
        if results.get('status') == 'error':
            raise HTTPException(status_code=500, detail=results['message'])
        
        logger.info(f"Buckling analysis completed. Critical load factor: {results['critical_load_factor']:.3f}")
        
        return {
            "status": "success",
            "analysis_type": "Buckling",
            "critical_load_factor": results['critical_load_factor'],
            "load_factors": results['load_factors'],
            "n_modes": results['n_modes'],
            "stability_status": results['status'],
            "message": results['message'],
            "mode_shapes": [mode.tolist() for mode in results['mode_shapes']]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Buckling analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Buckling analysis failed: {str(e)}")


@router.post("/calculate-stresses")
def calculate_stresses(request: StressCalculationRequest):
    """
    Calculate stresses from element forces
    
    Computes:
    - Axial stress (σ = N/A)
    - Bending stress (σ = M*y/I)
    - Shear stress (τ = V/A)
    - Torsional stress (τ = T*r/J)
    - Von Mises stress
    
    Returns stress components for each element
    """
    try:
        logger.info("Calculating element stresses")
        
        stresses = ResultsPostProcessor.calculate_stresses(
            request.element_forces,
            request.section_props
        )
        
        return {
            "status": "success",
            "element_stresses": stresses
        }
        
    except Exception as e:
        logger.error(f"Stress calculation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Stress calculation failed: {str(e)}")


@router.post("/utilization-ratios")
def calculate_utilization_ratios(request: UtilizationRatioRequest):
    """
    Calculate utilization ratios (demand/capacity)
    
    Computes:
    - Utilization ratio = σ_actual / σ_allowable
    - Status (OK, OVERSTRESSED)
    - Safety margin
    - Critical members (UR > threshold)
    
    Returns utilization ratios for all elements
    """
    try:
        logger.info("Calculating utilization ratios")
        
        # Calculate URs
        utilization_ratios = ResultsPostProcessor.calculate_utilization_ratios(
            request.element_stresses,
            request.material_props
        )
        
        # Identify critical members
        critical_members = ResultsPostProcessor.identify_critical_members(
            utilization_ratios,
            request.threshold
        )
        
        # Summary statistics
        all_urs = [data['utilization_ratio'] for data in utilization_ratios.values()]
        max_ur = max(all_urs) if all_urs else 0.0
        avg_ur = sum(all_urs) / len(all_urs) if all_urs else 0.0
        overstressed_count = sum(1 for ur in all_urs if ur > 1.0)
        
        return {
            "status": "success",
            "utilization_ratios": utilization_ratios,
            "critical_members": critical_members,
            "summary": {
                "max_utilization_ratio": round(max_ur, 3),
                "avg_utilization_ratio": round(avg_ur, 3),
                "overstressed_count": overstressed_count,
                "total_members": len(utilization_ratios),
                "critical_members_count": len(critical_members)
            }
        }
        
    except Exception as e:
        logger.error(f"Utilization ratio calculation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Utilization ratio calculation failed: {str(e)}")


@router.get("/analysis-types")
def get_analysis_types():
    """
    Get list of available advanced analysis types
    """
    return {
        "analysis_types": [
            {
                "type": "pdelta",
                "name": "P-Delta Analysis",
                "description": "Second-order analysis accounting for geometric nonlinearity",
                "features": [
                    "Geometric stiffness matrix",
                    "Iterative solution",
                    "Stability indices",
                    "Convergence monitoring"
                ]
            },
            {
                "type": "buckling",
                "name": "Buckling Analysis",
                "description": "Eigenvalue analysis for critical buckling loads",
                "features": [
                    "Critical load factors",
                    "Buckling mode shapes",
                    "Stability assessment",
                    "Multiple modes"
                ]
            },
            {
                "type": "stress_calculation",
                "name": "Stress Calculation",
                "description": "Calculate stresses from element forces",
                "features": [
                    "Axial stress",
                    "Bending stress",
                    "Shear stress",
                    "Von Mises stress"
                ]
            },
            {
                "type": "utilization_ratios",
                "name": "Utilization Ratios",
                "description": "Calculate demand/capacity ratios",
                "features": [
                    "Utilization ratios",
                    "Critical members",
                    "Safety margins",
                    "Summary statistics"
                ]
            }
        ]
    }


@router.get("/stability-criteria")
def get_stability_criteria():
    """
    Get stability criteria and limits
    """
    return {
        "stability_index": {
            "description": "Story stability index θ = (P*Δ)/(V*h)",
            "limits": {
                "stable": "θ < 0.1",
                "significant_pdelta": "0.1 ≤ θ < 0.2",
                "potentially_unstable": "θ ≥ 0.2"
            }
        },
        "buckling_load_factor": {
            "description": "Critical load factor from eigenvalue analysis",
            "limits": {
                "unstable": "λ < 1.0",
                "marginal": "1.0 ≤ λ < 2.0",
                "stable": "λ ≥ 2.0",
                "recommended": "λ ≥ 3.0"
            }
        },
        "utilization_ratio": {
            "description": "Demand/capacity ratio",
            "limits": {
                "ok": "UR ≤ 1.0",
                "critical": "0.95 ≤ UR ≤ 1.0",
                "overstressed": "UR > 1.0"
            }
        }
    }
