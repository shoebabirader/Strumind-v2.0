from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from typing import Dict
from app.reporting.pdf_generator import PDFReportGenerator

router = APIRouter()

class ReportRequest(BaseModel):
    project_data: Dict
    analysis_results: Dict

class CalculationSheetRequest(BaseModel):
    member_id: str
    design_data: Dict

@router.post("/analysis-report")
def generate_analysis_report(request: ReportRequest):
    """Generate comprehensive analysis report"""
    try:
        generator = PDFReportGenerator()
        pdf_content = generator.generate_analysis_report(
            request.project_data,
            request.analysis_results
        )
        
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=analysis_report.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/calculation-sheet")
def generate_calculation_sheet(request: CalculationSheetRequest):
    """Generate detailed calculation sheet"""
    try:
        generator = PDFReportGenerator()
        pdf_content = generator.generate_calculation_sheet(
            request.member_id,
            request.design_data
        )
        
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=calc_{request.member_id}.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
