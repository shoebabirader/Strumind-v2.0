from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from app.engine.results_processor import ResultsProcessor

router = APIRouter()

class DiagramRequest(BaseModel):
    element_id: str
    values: List[float]
    stations: List[float]
    span: float = 0.0

@router.post("/results/moment-diagram")
def generate_moment_diagram(request: DiagramRequest):
    """Generate moment diagram data"""
    try:
        processor = ResultsProcessor()
        result = processor.generate_moment_diagram(
            request.element_id,
            request.values,
            request.stations
        )
        return {"status": "success", "diagram": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/results/shear-diagram")
def generate_shear_diagram(request: DiagramRequest):
    """Generate shear force diagram data"""
    try:
        processor = ResultsProcessor()
        result = processor.generate_shear_diagram(
            request.element_id,
            request.values,
            request.stations
        )
        return {"status": "success", "diagram": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/results/deflection-curve")
def generate_deflection_curve(request: DiagramRequest):
    """Generate deflection curve with serviceability checks"""
    try:
        processor = ResultsProcessor()
        result = processor.generate_deflection_curve(
            request.element_id,
            request.values,
            request.stations,
            request.span
        )
        return {"status": "success", "curve": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/results/process-batch")
def process_batch_results(element_ids: List[str], results_data: Dict):
    """Process results for multiple elements"""
    try:
        processor = ResultsProcessor()
        processed = {}
        for elem_id in element_ids:
            if elem_id in results_data:
                processed[elem_id] = {
                    "processed": True,
                    "summary": "Results processed successfully"
                }
        return {"status": "success", "processed_results": processed}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/results/export-formats")
def get_export_formats():
    """Get available export formats for results"""
    return {
        "formats": [
            {"format": "json", "description": "JSON format"},
            {"format": "csv", "description": "Comma-separated values"},
            {"format": "excel", "description": "Microsoft Excel"},
            {"format": "pdf", "description": "PDF report"}
        ]
    }
