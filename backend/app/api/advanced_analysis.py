from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import numpy as np
from app.engine.advanced_analysis import TimeHistoryAnalysis, BucklingAnalysis, LoadCombinations, EnvelopeResults
from app.engine.results_processor import ResultsProcessor
from app.database.steel_sections import SteelSectionDatabase
from app.engine.slab_design import SlabDesign

router = APIRouter()

class TimeHistoryRequest(BaseModel):
    mass_matrix: List[List[float]]
    stiffness_matrix: List[List[float]]
    damping_matrix: List[List[float]]
    force_history: List[List[float]]
    time_step: float
    damping_ratio: float = 0.05

class BucklingRequest(BaseModel):
    stiffness_matrix: List[List[float]]
    geometric_stiffness_matrix: List[List[float]]
    n_modes: int = 10

class LoadCombinationRequest(BaseModel):
    load_cases: Dict[str, float]
    code: str = "IS875"

class EnvelopeRequest(BaseModel):
    combination_results: Dict[str, List[float]]

class SlabDesignRequest(BaseModel):
    slab_type: str
    span_x: float
    span_y: Optional[float] = None
    thickness: float
    loads: Dict
    support_condition: str = "simply_supported"
    column_size: Optional[float] = None

class ResultsVisualizationRequest(BaseModel):
    element_id: str
    result_type: str
    stations: List[float]
    values: List[float]
    span: Optional[float] = None

@router.post("/time-history")
def time_history_analysis(request: TimeHistoryRequest):
    """Perform time-history analysis"""
    try:
        analyzer = TimeHistoryAnalysis()
        
        M = np.array(request.mass_matrix)
        K = np.array(request.stiffness_matrix)
        C = np.array(request.damping_matrix)
        F_t = np.array(request.force_history)
        
        result = analyzer.newmark_beta(M, C, K, F_t, request.time_step, request.damping_ratio)
        
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/buckling")
def buckling_analysis(request: BucklingRequest):
    """Perform linear buckling analysis"""
    try:
        analyzer = BucklingAnalysis()
        
        K = np.array(request.stiffness_matrix)
        Kg = np.array(request.geometric_stiffness_matrix)
        
        result = analyzer.linear_buckling(K, Kg, request.n_modes)
        
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/load-combinations")
def generate_load_combinations(request: LoadCombinationRequest):
    """Generate load combinations per code"""
    try:
        generator = LoadCombinations(request.code)
        result = generator.generate_combinations(request.load_cases)
        
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/envelope")
def calculate_envelope(request: EnvelopeRequest):
    """Calculate envelope results"""
    try:
        processor = EnvelopeResults()
        results = {combo: np.array(values) for combo, values in request.combination_results.items()}
        result = processor.calculate_envelope(results)
        
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/steel-sections/{standard}")
def get_steel_sections(standard: str, section_type: Optional[str] = None):
    """Get steel sections from database"""
    try:
        db = SteelSectionDatabase()
        
        if section_type:
            sections = [s for s in db.sections[standard] if s.type == section_type]
        else:
            sections = db.sections[standard]
        
        return {
            "status": "success",
            "sections": [s.to_dict() for s in sections]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/steel-sections/standards")
def get_steel_standards():
    """Get available steel section standards"""
    db = SteelSectionDatabase()
    return {
        "standards": db.get_all_standards(),
        "total_sections": sum(len(sections) for sections in db.sections.values())
    }

@router.post("/slab-design")
def design_slab(request: SlabDesignRequest):
    """Design concrete slab"""
    try:
        designer = SlabDesign()
        
        if request.slab_type == "one_way":
            result = designer.one_way_slab_design(
                request.span_x,
                request.thickness,
                request.loads,
                request.support_condition
            )
        elif request.slab_type == "two_way":
            result = designer.two_way_slab_design(
                request.span_x,
                request.span_y,
                request.thickness,
                request.loads,
                request.support_condition
            )
        elif request.slab_type == "flat_slab":
            result = designer.flat_slab_design(
                request.span_x,
                request.column_size,
                request.thickness,
                request.loads
            )
        else:
            raise ValueError(f"Unknown slab type: {request.slab_type}")
        
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/results/moment-diagram")
def generate_moment_diagram(request: ResultsVisualizationRequest):
    """Generate moment diagram data"""
    try:
        processor = ResultsProcessor()
        result = processor.generate_moment_diagram(
            request.element_id,
            request.values,
            request.stations
        )
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/results/shear-diagram")
def generate_shear_diagram(request: ResultsVisualizationRequest):
    """Generate shear diagram data"""
    try:
        processor = ResultsProcessor()
        result = processor.generate_shear_diagram(
            request.element_id,
            request.values,
            request.stations
        )
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/results/deflection-curve")
def generate_deflection_curve(request: ResultsVisualizationRequest):
    """Generate deflection curve data"""
    try:
        processor = ResultsProcessor()
        result = processor.generate_deflection_curve(
            request.element_id,
            request.values,
            request.stations,
            request.span
        )
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
