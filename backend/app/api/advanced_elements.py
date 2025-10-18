from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional

router = APIRouter()

class ShellElementRequest(BaseModel):
    element_id: str
    nodes: List[int]
    thickness: float
    material_id: str
    element_type: str = "quad4"  # quad4, quad8, tri3, tri6

class PlateElementRequest(BaseModel):
    element_id: str
    nodes: List[int]
    thickness: float
    material_id: str

class SolidElementRequest(BaseModel):
    element_id: str
    nodes: List[int]
    material_id: str
    element_type: str = "hex8"  # hex8, hex20, tet4, tet10

class LinkElementRequest(BaseModel):
    element_id: str
    nodes: List[int]
    area: float
    material_id: str
    element_type: str = "truss"  # truss, cable, gap

@router.post("/advanced-elements/shell")
def create_shell_element(request: ShellElementRequest):
    """Create shell element"""
    try:
        return {
            "status": "success",
            "element": {
                "id": request.element_id,
                "type": "shell",
                "subtype": request.element_type,
                "nodes": request.nodes,
                "thickness": request.thickness,
                "dofs_per_node": 6
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/advanced-elements/plate")
def create_plate_element(request: PlateElementRequest):
    """Create plate bending element"""
    try:
        return {
            "status": "success",
            "element": {
                "id": request.element_id,
                "type": "plate",
                "nodes": request.nodes,
                "thickness": request.thickness,
                "dofs_per_node": 3
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/advanced-elements/solid")
def create_solid_element(request: SolidElementRequest):
    """Create 3D solid element"""
    try:
        return {
            "status": "success",
            "element": {
                "id": request.element_id,
                "type": "solid",
                "subtype": request.element_type,
                "nodes": request.nodes,
                "dofs_per_node": 3
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/advanced-elements/link")
def create_link_element(request: LinkElementRequest):
    """Create link/truss/cable element"""
    try:
        return {
            "status": "success",
            "element": {
                "id": request.element_id,
                "type": "link",
                "subtype": request.element_type,
                "nodes": request.nodes,
                "area": request.area
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/advanced-elements/types")
def list_element_types():
    """List all available advanced element types"""
    return {
        "element_types": {
            "shell": ["quad4", "quad8", "quad9", "tri3", "tri6"],
            "plate": ["quad4", "quad8", "tri3", "tri6"],
            "solid": ["hex8", "hex20", "hex27", "tet4", "tet10"],
            "link": ["truss", "cable", "gap", "hook"]
        }
    }

@router.get("/advanced-elements/formulations")
def list_element_formulations():
    """List element formulation options"""
    return {
        "formulations": [
            {"name": "displacement", "description": "Standard displacement formulation"},
            {"name": "mixed", "description": "Mixed formulation (u-p)"},
            {"name": "hybrid", "description": "Hybrid stress formulation"},
            {"name": "enhanced", "description": "Enhanced strain formulation"}
        ]
    }
