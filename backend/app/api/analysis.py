from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import numpy as np
from app.engine.geometry import GeometryEngine
from app.engine.analysis import StructuralAnalysis

router = APIRouter()

class NodeData(BaseModel):
    id: int
    x: float
    y: float
    z: float
    restraints: Optional[List[bool]] = None

class ElementData(BaseModel):
    id: int
    node_ids: List[int]
    element_type: str
    material_id: Optional[str] = "default"
    section_id: Optional[str] = "default"

class AnalysisRequest(BaseModel):
    model_config = {"protected_namespaces": ()}
    
    model_id: int
    analysis_type: str  # static, modal
    nodes: List[NodeData]
    elements: List[ElementData]
    loads: List[float]  # Global load vector
    restraints: Dict[int, List[bool]]  # {node_id: [ux, uy, uz, rx, ry, rz]}
    material_props: Optional[Dict] = None
    section_props: Optional[Dict] = None

class AnalysisResponse(BaseModel):
    model_config = {"protected_namespaces": ()}
    
    model_id: int
    analysis_type: str
    results: Dict
    status: str

@router.post("/run", response_model=AnalysisResponse)
def run_analysis(request: AnalysisRequest):
    """
    Run structural analysis
    
    Supports:
    - static: Static linear analysis
    - modal: Modal analysis (natural frequencies and mode shapes)
    """
    try:
        # Initialize geometry engine
        geom = GeometryEngine()
        
        # Add nodes
        for node_data in request.nodes:
            node = geom.add_node(node_data.id, node_data.x, node_data.y, node_data.z)
            if node_data.restraints:
                node.restraints = node_data.restraints
        
        # Add elements
        for elem_data in request.elements:
            geom.add_element(elem_data.id, elem_data.node_ids, elem_data.element_type)
        
        # Validate geometry
        is_valid, errors = geom.validate_geometry()
        if not is_valid:
            raise HTTPException(status_code=400, detail=f"Invalid geometry: {errors}")
        
        # Initialize analysis
        analyzer = StructuralAnalysis(geom)
        
        # Use provided or default material/section properties
        material_props = request.material_props or geom.materials
        section_props = request.section_props or geom.sections
        
        # Assemble stiffness matrix
        analyzer.assemble_stiffness_matrix(material_props, section_props)
        
        # Run analysis based on type
        if request.analysis_type == "static":
            # Convert loads list to numpy array
            loads = np.array(request.loads)
            
            # Run static analysis
            results = analyzer.static_analysis(loads, request.restraints)
            
            return AnalysisResponse(
                model_id=request.model_id,
                analysis_type=request.analysis_type,
                status="success",
                results={
                    "displacements": results['displacements'].tolist(),
                    "reactions": results['reactions'].tolist(),
                    "element_forces": results['element_forces']
                }
            )
            
        elif request.analysis_type == "modal":
            # Run modal analysis
            modal_results = analyzer.modal_analysis(
                material_props, 
                section_props, 
                request.restraints, 
                n_modes=10
            )
            
            return AnalysisResponse(
                model_id=request.model_id,
                analysis_type=request.analysis_type,
                status="success",
                results={
                    "frequencies": modal_results['frequencies'],
                    "periods": modal_results['periods'],
                    "participation_factors": modal_results['participation_factors']
                }
            )
        else:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported analysis type: {request.analysis_type}"
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
