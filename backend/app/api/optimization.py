from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
from app.engine.optimization import SectionOptimizer

router = APIRouter()

class BeamOptimizationRequest(BaseModel):
    moment: float
    shear: float
    constraints: Dict[str, float]
    optimization_objective: str = "cost"

class ColumnOptimizationRequest(BaseModel):
    axial_load: float
    moment: float
    constraints: Dict[str, float]

class MultiObjectiveRequest(BaseModel):
    design_variables: Dict[str, float]
    objectives: list[str]
    constraints: Dict[str, float]

@router.post("/optimization/beam-section")
def optimize_beam_section(request: BeamOptimizationRequest):
    """Optimize beam section dimensions and reinforcement"""
    try:
        optimizer = SectionOptimizer()
        result = optimizer.optimize_beam_section(
            request.moment,
            request.shear,
            request.constraints
        )
        return {"status": "success", "optimization": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/optimization/column-section")
def optimize_column_section(request: ColumnOptimizationRequest):
    """Optimize column section"""
    try:
        optimizer = SectionOptimizer()
        # Placeholder for column optimization
        result = {
            "optimized": True,
            "section": {"width": 300, "depth": 300},
            "reinforcement": "8-20mm",
            "ties": "8mm @ 150mm"
        }
        return {"status": "success", "optimization": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/optimization/multi-objective")
def multi_objective_optimization(request: MultiObjectiveRequest):
    """Multi-objective optimization"""
    try:
        result = {
            "pareto_front": [],
            "optimal_solutions": [],
            "trade_offs": {}
        }
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/optimization/algorithms")
def list_optimization_algorithms():
    """List available optimization algorithms"""
    return {
        "algorithms": [
            {"name": "SLSQP", "type": "gradient-based", "description": "Sequential Least Squares Programming"},
            {"name": "genetic", "type": "evolutionary", "description": "Genetic Algorithm"},
            {"name": "particle_swarm", "type": "swarm", "description": "Particle Swarm Optimization"},
            {"name": "simulated_annealing", "type": "metaheuristic", "description": "Simulated Annealing"}
        ]
    }
