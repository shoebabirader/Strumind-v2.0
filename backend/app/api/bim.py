from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Dict
import os
from app.bim.ifc_handler import IFCHandler
from app.bim.visualization import VisualizationEngine

router = APIRouter()

ifc_handler = IFCHandler()
viz_engine = VisualizationEngine()

class IFCExportRequest(BaseModel):
    model_config = {"protected_namespaces": ()}
    model_id: int
    model_data: Dict

class IFCExportResponse(BaseModel):
    model_config = {"protected_namespaces": ()}
    model_id: int
    ifc_content: str
    download_url: str

class VisualizationRequest(BaseModel):
    model_config = {"protected_namespaces": ()}
    model_id: int
    model_data: Dict
    analysis_results: Dict = None

@router.post("/export/ifc", response_model=IFCExportResponse)
def export_to_ifc(request: IFCExportRequest):
    """Export structural model to IFC format"""
    ifc_content = ifc_handler.export_to_ifc(request.model_data)
    
    # Save to file (simplified)
    filename = f"model_{request.model_id}.ifc"
    download_url = f"/exports/{filename}"
    
    return IFCExportResponse(
        model_id=request.model_id,
        ifc_content=ifc_content,
        download_url=download_url
    )

@router.post("/import/ifc")
async def import_from_ifc(file: UploadFile = File(...)):
    """Import IFC file and extract structural data"""
    # SECURITY FIX: Validate file type and size
    ALLOWED_EXTENSIONS = {'.ifc', '.IFC'}
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    
    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Only IFC files are allowed. Got: {file_ext}"
        )
    
    # Read and validate file size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE / (1024*1024)}MB"
        )
    
    # Validate content is text-based (IFC files are text)
    try:
        ifc_content = content.decode('utf-8')
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Invalid IFC file format. File must be valid UTF-8 text."
        )
    
    # Validate IFC header
    if not ifc_content.strip().startswith('ISO-10303-21'):
        raise HTTPException(
            status_code=400,
            detail="Invalid IFC file. Missing ISO-10303-21 header."
        )
    
    try:
        model_data = ifc_handler.import_from_ifc(ifc_content)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to parse IFC file: {str(e)}"
        )
    
    return {
        "status": "success",
        "model_data": model_data,
        "filename": file.filename
    }

@router.post("/visualization/scene")
def generate_scene(request: VisualizationRequest):
    """Generate Three.js scene data"""
    scene = viz_engine.generate_threejs_scene(request.model_data)
    return {"scene": scene}

@router.post("/visualization/stress")
def generate_stress_viz(request: VisualizationRequest):
    """Generate stress visualization"""
    if not request.analysis_results:
        raise HTTPException(status_code=400, detail="Analysis results required")
    
    viz_data = viz_engine.generate_stress_visualization(request.analysis_results)
    return {"visualization": viz_data}

@router.post("/visualization/deformation")
def generate_deformation_viz(request: VisualizationRequest):
    """Generate deformation visualization"""
    if not request.analysis_results:
        raise HTTPException(status_code=400, detail="Analysis results required")
    
    viz_data = viz_engine.generate_deformation_visualization(request.analysis_results)
    return {"visualization": viz_data}
