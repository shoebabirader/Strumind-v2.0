from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, List

router = APIRouter()

class TemplateResponse(BaseModel):
    name: str
    description: str
    nodes: List[Dict]
    elements: List[Dict]
    materials: Dict
    sections: Dict

@router.get("/list")
def list_templates():
    """Get list of available model templates"""
    return {
        "templates": [
            {"name": "Simple Frame", "description": "2D portal frame with 2 columns and 1 beam"},
            {"name": "Building Frame", "description": "3D multi-story building frame"},
            {"name": "Truss", "description": "2D truss structure"},
            {"name": "Grid Floor", "description": "Grid of beams and slabs"},
            {"name": "Bridge", "description": "Simple bridge structure"},
        ]
    }

@router.get("/{template_name}", response_model=TemplateResponse)
def get_template(template_name: str):
    """Get specific template with geometry"""
    templates = {
        "Simple Frame": generate_simple_frame(),
        "Building Frame": generate_building_frame(),
        "Truss": generate_truss(),
        "Grid Floor": generate_grid_floor(),
        "Bridge": generate_bridge(),
    }
    
    return templates.get(template_name, generate_simple_frame())

def generate_simple_frame() -> Dict:
    """Generate a simple 2D portal frame"""
    return {
        "name": "Simple Frame",
        "description": "2D portal frame",
        "nodes": [
            {"id": 1, "x": 0, "y": 0, "z": 0, "restraints": [True, True, True, True, True, True]},
            {"id": 2, "x": 0, "y": 3000, "z": 0, "restraints": [False] * 6},
            {"id": 3, "x": 5000, "y": 3000, "z": 0, "restraints": [False] * 6},
            {"id": 4, "x": 5000, "y": 0, "z": 0, "restraints": [True, True, True, True, True, True]},
        ],
        "elements": [
            {"id": 1, "type": "column", "nodes": [1, 2], "material": "Concrete M25", "section": "300x300"},
            {"id": 2, "type": "beam", "nodes": [2, 3], "material": "Concrete M25", "section": "300x450"},
            {"id": 3, "type": "column", "nodes": [3, 4], "material": "Concrete M25", "section": "300x300"},
        ],
        "materials": {
            "Concrete M25": {"E": 25e9, "poisson": 0.2, "density": 2500, "grade": "M25"}
        },
        "sections": {
            "300x300": {"type": "rectangular", "width": 300, "depth": 300},
            "300x450": {"type": "rectangular", "width": 300, "depth": 450}
        }
    }

def generate_building_frame() -> Dict:
    """Generate a 3D multi-story building frame"""
    nodes = []
    elements = []
    node_id = 1
    elem_id = 1
    
    # 3 stories, 2x2 bays
    for floor in range(4):  # 0 to 3 (4 levels)
        y = floor * 3000
        for i in range(3):  # 3 columns in X
            for j in range(3):  # 3 columns in Z
                x = i * 5000
                z = j * 5000
                restraints = [True] * 6 if floor == 0 else [False] * 6
                nodes.append({"id": node_id, "x": x, "y": y, "z": z, "restraints": restraints})
                
                # Add column to next floor
                if floor < 3:
                    elements.append({
                        "id": elem_id,
                        "type": "column",
                        "nodes": [node_id, node_id + 9],
                        "material": "Concrete M25",
                        "section": "300x300"
                    })
                    elem_id += 1
                
                node_id += 1
    
    return {
        "name": "Building Frame",
        "description": "3D multi-story building",
        "nodes": nodes,
        "elements": elements,
        "materials": {
            "Concrete M25": {"E": 25e9, "poisson": 0.2, "density": 2500, "grade": "M25"}
        },
        "sections": {
            "300x300": {"type": "rectangular", "width": 300, "depth": 300},
            "300x450": {"type": "rectangular", "width": 300, "depth": 450}
        }
    }

def generate_truss() -> Dict:
    """Generate a 2D truss"""
    return {
        "name": "Truss",
        "description": "2D truss structure",
        "nodes": [
            {"id": 1, "x": 0, "y": 0, "z": 0, "restraints": [True, True, True, True, True, True]},
            {"id": 2, "x": 2000, "y": 1500, "z": 0, "restraints": [False] * 6},
            {"id": 3, "x": 4000, "y": 0, "z": 0, "restraints": [True, True, True, True, True, True]},
        ],
        "elements": [
            {"id": 1, "type": "truss", "nodes": [1, 2], "material": "Steel Fe415", "section": "ISA 75x75x6"},
            {"id": 2, "type": "truss", "nodes": [2, 3], "material": "Steel Fe415", "section": "ISA 75x75x6"},
        ],
        "materials": {
            "Steel Fe415": {"E": 200e9, "poisson": 0.3, "density": 7850, "grade": "Fe415"}
        },
        "sections": {
            "ISA 75x75x6": {"type": "angle", "width": 75, "thickness": 6}
        }
    }

def generate_grid_floor() -> Dict:
    """Generate a grid floor system"""
    nodes = []
    elements = []
    node_id = 1
    elem_id = 1
    
    # 4x4 grid
    for i in range(4):
        for j in range(4):
            nodes.append({
                "id": node_id,
                "x": i * 5000,
                "y": 3000,
                "z": j * 5000,
                "restraints": [False] * 6
            })
            node_id += 1
    
    # Add beams in X direction
    for j in range(4):
        for i in range(3):
            elements.append({
                "id": elem_id,
                "type": "beam",
                "nodes": [j * 4 + i + 1, j * 4 + i + 2],
                "material": "Concrete M25",
                "section": "300x450"
            })
            elem_id += 1
    
    # Add beams in Z direction
    for i in range(4):
        for j in range(3):
            elements.append({
                "id": elem_id,
                "type": "beam",
                "nodes": [j * 4 + i + 1, (j + 1) * 4 + i + 1],
                "material": "Concrete M25",
                "section": "300x450"
            })
            elem_id += 1
    
    return {
        "name": "Grid Floor",
        "description": "Grid floor system",
        "nodes": nodes,
        "elements": elements,
        "materials": {
            "Concrete M25": {"E": 25e9, "poisson": 0.2, "density": 2500, "grade": "M25"}
        },
        "sections": {
            "300x450": {"type": "rectangular", "width": 300, "depth": 450}
        }
    }

def generate_bridge() -> Dict:
    """Generate a simple bridge"""
    return {
        "name": "Bridge",
        "description": "Simple bridge structure",
        "nodes": [
            {"id": 1, "x": 0, "y": 0, "z": 0, "restraints": [True, True, True, True, True, True]},
            {"id": 2, "x": 10000, "y": 0, "z": 0, "restraints": [False] * 6},
            {"id": 3, "x": 20000, "y": 0, "z": 0, "restraints": [True, True, True, True, True, True]},
        ],
        "elements": [
            {"id": 1, "type": "beam", "nodes": [1, 2], "material": "Concrete M30", "section": "1000x600"},
            {"id": 2, "type": "beam", "nodes": [2, 3], "material": "Concrete M30", "section": "1000x600"},
        ],
        "materials": {
            "Concrete M30": {"E": 27e9, "poisson": 0.2, "density": 2500, "grade": "M30"}
        },
        "sections": {
            "1000x600": {"type": "rectangular", "width": 1000, "depth": 600}
        }
    }
