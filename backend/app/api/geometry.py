from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from app.engine.geometry import GeometryEngine, Node, Element

router = APIRouter()

class NodeCreate(BaseModel):
    id: int
    x: float
    y: float
    z: float
    restraints: Optional[List[bool]] = None

class ElementCreate(BaseModel):
    id: int
    node_ids: List[int]
    element_type: str
    material_id: Optional[str] = "default"
    section_id: Optional[str] = "default"

class RestraintUpdate(BaseModel):
    node_id: int
    restraint_type: str  # 'fixed', 'pinned', 'roller'
    direction: Optional[str] = None

class DistributedLoadRequest(BaseModel):
    element_id: int
    intensity: float
    direction: str = "y"
    coordinate_system: str = "global"

@router.post("/geometry/create-engine")
def create_geometry_engine():
    """Create a new geometry engine instance"""
    try:
        engine = GeometryEngine()
        return {"status": "success", "engine_id": id(engine)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/geometry/nodes/create")
def create_node(node: NodeCreate):
    """Create a new node"""
    try:
        new_node = Node(node.id, node.x, node.y, node.z)
        if node.restraints:
            new_node.restraints = node.restraints
        return {
            "status": "success",
            "node": {
                "id": new_node.id,
                "coordinates": [new_node.x, new_node.y, new_node.z],
                "restraints": new_node.restraints
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/geometry/nodes/set-restraint")
def set_node_restraint(request: RestraintUpdate):
    """Set node restraint (fixed, pinned, roller)"""
    try:
        node = Node(request.node_id, 0, 0, 0)
        
        if request.restraint_type == "fixed":
            node.set_fixed()
        elif request.restraint_type == "pinned":
            node.set_pinned()
        elif request.restraint_type == "roller":
            node.set_roller(request.direction or "y")
        
        return {
            "status": "success",
            "node_id": node.id,
            "restraints": node.restraints
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/geometry/elements/create")
def create_element(element: ElementCreate):
    """Create a new element"""
    try:
        nodes = [Node(nid, 0, 0, 0) for nid in element.node_ids]
        new_element = Element(element.id, nodes, element.element_type)
        new_element.material_id = element.material_id
        new_element.section_id = element.section_id
        
        return {
            "status": "success",
            "element": {
                "id": new_element.id,
                "type": new_element.element_type,
                "nodes": element.node_ids,
                "length": new_element.length()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/geometry/elements/add-distributed-load")
def add_distributed_load(request: DistributedLoadRequest):
    """Add distributed load to element"""
    try:
        return {
            "status": "success",
            "element_id": request.element_id,
            "load": {
                "intensity": request.intensity,
                "direction": request.direction,
                "coordinate_system": request.coordinate_system
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/geometry/validate")
def validate_geometry(node_count: int, element_count: int):
    """Validate geometry"""
    try:
        is_valid = node_count > 0 and element_count > 0
        warnings = []
        
        if node_count < 2:
            warnings.append("Minimum 2 nodes required")
        if element_count < 1:
            warnings.append("At least 1 element required")
        
        return {
            "valid": is_valid,
            "warnings": warnings,
            "node_count": node_count,
            "element_count": element_count
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
