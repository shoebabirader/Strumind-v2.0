from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Dict
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
    content = await file.read()
    ifc_content = content.decode('utf-8')
    
    model_data = ifc_handler.import_from_ifc(ifc_content)
    
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
