from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, field_validator, Field
from typing import Dict, List, Optional
import numpy as np
import logging
from app.engine.geometry import GeometryEngine
from app.engine.analysis import StructuralAnalysis
from app.core.validators import NodeValidator, GeometryValidator, AnalysisValidator
from app.core.errors import (
    InvalidNodeError, InvalidElementError, SingularMatrixError,
    ConvergenceError, error_to_http_response
)

router = APIRouter()
logger = logging.getLogger(__name__)

class NodeData(BaseModel):
    id: int
    x: float = Field(..., description="X coordinate (mm)")
    y: float = Field(..., description="Y coordinate (mm)")
    z: float = Field(..., description="Z coordinate (mm)")
    restraints: Optional[List[bool]] = Field(None, description="6 DOF restraints")
    
    @field_validator('x', 'y', 'z')
    @classmethod
    def validate_coordinates(cls, v, info):
        """Validate coordinates"""
        is_valid, error = NodeValidator.validate_coordinates(v, v, v)
        if not is_valid:
            raise ValueError(error)
        return v
    
    @field_validator('restraints')
    @classmethod
    def validate_restraints(cls, v, info):
        """Validate restraints"""
        if v is not None and len(v) != 6:
            raise ValueError("Restraints must have 6 values")
        return v

class ElementData(BaseModel):
    id: int
    node_ids: List[int] = Field(..., min_items=2, description="Node IDs")
    element_type: str = Field(..., description="Element type")
    material_id: Optional[str] = Field("default", description="Material ID")
    section_id: Optional[str] = Field("default", description="Section ID")
    
    @field_validator('element_type')
    @classmethod
    def validate_element_type(cls, v, info):
        """Validate element type"""
        valid_types = ['beam', 'truss', 'frame', 'shell', 'solid']
        if v.lower() not in valid_types:
            raise ValueError(f"Element type must be one of: {', '.join(valid_types)}")
        return v.lower()

class AnalysisRequest(BaseModel):
    model_config = {"protected_namespaces": ()}
    
    model_id: int
    analysis_type: str = Field(..., description="Analysis type: static, modal, pdelta, buckling")
    nodes: List[NodeData] = Field(..., min_items=2)
    elements: List[ElementData] = Field(..., min_items=1)
    loads: List[float] = Field(..., description="Global load vector")
    restraints: Dict[int, List[bool]] = Field(..., description="Boundary conditions")
    material_props: Optional[Dict] = None
    section_props: Optional[Dict] = None
    max_iterations: Optional[int] = Field(50, ge=1, le=1000)
    tolerance: Optional[float] = Field(1e-6, gt=0, lt=1e-3)
    
    @field_validator('analysis_type')
    @classmethod
    def validate_analysis_type(cls, v, info):
        """Validate analysis type"""
        valid_types = ['static', 'modal', 'pdelta', 'buckling', 'time-history']
        if v.lower() not in valid_types:
            raise ValueError(f"Analysis type must be one of: {', '.join(valid_types)}")
        return v.lower()
    
    @field_validator('max_iterations')
    @classmethod
    def validate_iterations(cls, v, info):
        """Validate max iterations"""
        is_valid, error = AnalysisValidator.validate_max_iterations(v)
        if not is_valid:
            raise ValueError(error)
        return v
    
    @field_validator('tolerance')
    @classmethod
    def validate_tolerance(cls, v, info):
        """Validate convergence tolerance"""
        is_valid, error = AnalysisValidator.validate_convergence_tolerance(v)
        if not is_valid:
            raise ValueError(error)
        return v

class AnalysisResponse(BaseModel):
    model_config = {"protected_namespaces": ()}
    
    model_id: int
    analysis_type: str
    results: Dict
    status: str

@router.post("/run", response_model=AnalysisResponse)
def run_analysis(request: AnalysisRequest):
    """
    Run structural analysis with comprehensive validation
    
    Supports:
    - static: Static linear analysis
    - modal: Modal analysis
    - pdelta: P-Delta analysis
    - buckling: Buckling analysis
    """
    try:
        logger.info(f"Starting {request.analysis_type} analysis for model {request.model_id}")
        
        # Validate minimum nodes and elements
        if len(request.nodes) < 2:
            raise InvalidNodeError("At least 2 nodes required")
        if len(request.elements) < 1:
            raise InvalidElementError("At least 1 element required")
        
        # Validate restraints
        n_restraints = sum(sum(r) for r in request.restraints.values())
        is_valid, error = GeometryValidator.check_stability(
            len(request.nodes), n_restraints, dimension=3
        )
        if not is_valid:
            raise InvalidElementError(error)
        
        # Initialize geometry engine
        geom = GeometryEngine()
        
        # Add nodes with validation
        for node_data in request.nodes:
            is_valid, error = NodeValidator.validate_coordinates(
                node_data.x, node_data.y, node_data.z
            )
            if not is_valid:
                raise InvalidNodeError(error)
            
            node = geom.add_node(node_data.id, node_data.x, node_data.y, node_data.z)
            if node_data.restraints:
                node.restraints = node_data.restraints
        
        # Add elements
        for elem_data in request.elements:
            geom.add_element(elem_data.id, elem_data.node_ids, elem_data.element_type)
        
        # Validate geometry
        is_valid, errors = geom.validate_geometry()
        if not is_valid:
            raise InvalidElementError(f"Invalid geometry: {errors}")
        
        # Initialize analysis
        analyzer = StructuralAnalysis(geom)
        
        # Use provided or default material/section properties
        material_props = request.material_props or geom.materials
        section_props = request.section_props or geom.sections
        
        # Assemble stiffness matrix
        try:
            analyzer.assemble_stiffness_matrix(material_props, section_props)
        except np.linalg.LinAlgError:
            raise SingularMatrixError()
        
        # Run analysis based on type
        if request.analysis_type == "static":
            loads = np.array(request.loads)
            results = analyzer.static_analysis(loads, request.restraints)
            
            logger.info(f"Static analysis completed successfully")
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
            modal_results = analyzer.modal_analysis(
                material_props, section_props, request.restraints, n_modes=10
            )
            
            logger.info(f"Modal analysis completed: {len(modal_results['frequencies'])} modes")
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
            
    except (InvalidNodeError, InvalidElementError, SingularMatrixError) as e:
        response = error_to_http_response(e)
        logger.error(f"Analysis validation error: {e}")
        raise HTTPException(status_code=response['status_code'], detail=response['detail'])
    
    except np.linalg.LinAlgError as e:
        logger.error(f"Linear algebra error: {e}")
        raise HTTPException(status_code=500, detail="Singular stiffness matrix. Check model stability.")
    
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
