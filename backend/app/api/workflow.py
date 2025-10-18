from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from app.engine.workflow import StructuralWorkflow, LoadCase, LoadCombination

router = APIRouter()

class GeometryRequest(BaseModel):
    nodes: List[Dict[str, Any]]
    elements: List[Dict[str, Any]]

class MaterialRequest(BaseModel):
    materials: Dict[str, Dict[str, float]]

class LoadCaseRequest(BaseModel):
    name: str
    type: str
    loads: List[Dict[str, Any]]
    factor: float = 1.0
    description: str = ""

class LoadCombinationRequest(BaseModel):
    name: str
    description: str
    load_cases: Dict[str, float]

class WorkflowAnalysisRequest(BaseModel):
    geometry: GeometryRequest
    materials: MaterialRequest
    load_cases: List[LoadCaseRequest]
    combinations: Optional[List[LoadCombinationRequest]] = None
    analysis_type: str = "linear"

@router.post("/workflow/create")
def create_workflow():
    """Create a new structural workflow"""
    try:
        workflow = StructuralWorkflow()
        return {"status": "success", "workflow_id": id(workflow)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/workflow/run-complete")
def run_complete_workflow(request: WorkflowAnalysisRequest):
    """Run complete structural analysis workflow"""
    try:
        workflow = StructuralWorkflow()
        
        # Create geometry
        for node in request.geometry.nodes:
            workflow.geometry.add_node(
                node['id'], node['x'], node['y'], node['z']
            )
        
        for element in request.geometry.elements:
            workflow.geometry.add_element(
                element['id'], element['nodes'], element['type']
            )
        
        # Define materials
        for mat_id, props in request.materials.materials.items():
            workflow.define_material(mat_id, props)
        
        # Apply load cases
        for lc in request.load_cases:
            load_case = LoadCase(
                name=lc.name,
                type=lc.type,
                factor=lc.factor,
                description=lc.description
            )
            workflow.add_load_case(load_case)
        
        # Add combinations
        if request.combinations:
            for comb in request.combinations:
                combination = LoadCombination(
                    name=comb.name,
                    description=comb.description,
                    load_cases=comb.load_cases
                )
                workflow.add_combination(combination)
        
        # Run analysis
        results = workflow.run_analysis(request.analysis_type)
        
        return {
            "status": "success",
            "results": {
                "max_displacement": float(results.max_displacement),
                "total_reaction": float(results.total_reaction),
                "warnings": results.warnings,
                "summary": results.summary()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/workflow/status/{workflow_id}")
def get_workflow_status(workflow_id: str):
    """Get workflow execution status"""
    return {
        "workflow_id": workflow_id,
        "status": "ready",
        "geometry_ready": True,
        "materials_ready": True,
        "loads_ready": True
    }
