import numpy as np
from typing import List, Dict, Tuple, Optional

class Node:
    """Structural node with 6 degrees of freedom"""
    
    def __init__(self, id: int, x: float, y: float, z: float):
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.restraints = [False] * 6  # 6 DOF: ux, uy, uz, rx, ry, rz
        self.loads = [0.0] * 6  # Applied loads/moments
    
    def set_restraint(self, dof: int, restrained: bool = True):
        """Set restraint for specific DOF (0-5)"""
        if 0 <= dof < 6:
            self.restraints[dof] = restrained
    
    def set_fixed(self):
        """Fix all DOFs"""
        self.restraints = [True] * 6
    
    def set_pinned(self):
        """Pin support (translations fixed, rotations free)"""
        self.restraints = [True, True, True, False, False, False]
    
    def set_roller(self, direction: str = 'y'):
        """Roller support (one translation free, rotations free)"""
        if direction == 'x':
            # Free in x, restrained in y and z
            self.restraints = [False, True, True, False, False, False]
        elif direction == 'y':
            # Free in y, restrained in x and z
            self.restraints = [True, False, True, False, False, False]
        else:  # z
            # Free in z, restrained in x and y
            self.restraints = [True, True, False, False, False, False]
    
    def apply_load(self, fx: float = 0, fy: float = 0, fz: float = 0,
                   mx: float = 0, my: float = 0, mz: float = 0):
        """Apply loads and moments to node"""
        self.loads = [fx, fy, fz, mx, my, mz]
    
    def distance_to(self, other: 'Node') -> float:
        """Calculate distance to another node"""
        return np.sqrt((other.x - self.x)**2 + 
                      (other.y - self.y)**2 + 
                      (other.z - self.z)**2)

class Element:
    """Structural element (beam, column, truss, etc.)"""
    
    def __init__(self, id: int, nodes: List[Node], element_type: str):
        self.id = id
        self.nodes = nodes
        self.element_type = element_type  # beam, column, slab, shell, truss
        self.material_id = 'default'
        self.section_id = 'default'
        self.distributed_loads = []  # List of distributed loads
        
    def length(self) -> float:
        """Calculate element length"""
        if len(self.nodes) == 2:
            return self.nodes[0].distance_to(self.nodes[1])
        return 0.0
    
    def direction_vector(self) -> np.ndarray:
        """Get unit direction vector"""
        if len(self.nodes) == 2:
            n1, n2 = self.nodes
            dx = n2.x - n1.x
            dy = n2.y - n1.y
            dz = n2.z - n1.z
            L = self.length()
            if L > 1e-6:
                return np.array([dx/L, dy/L, dz/L])
        return np.array([0, 0, 0])
    
    def midpoint(self) -> Tuple[float, float, float]:
        """Get element midpoint coordinates"""
        if len(self.nodes) == 2:
            n1, n2 = self.nodes
            return ((n1.x + n2.x)/2, (n1.y + n2.y)/2, (n1.z + n2.z)/2)
        return (0, 0, 0)
    
    def add_distributed_load(self, w: float, direction: str = 'y', 
                           coordinate_system: str = 'global'):
        """
        Add distributed load to element
        
        Args:
            w: Load intensity (N/mm or kN/m)
            direction: 'x', 'y', or 'z'
            coordinate_system: 'global' or 'local'
        """
        self.distributed_loads.append({
            'intensity': w,
            'direction': direction,
            'coordinate_system': coordinate_system
        })

class GeometryEngine:
    """Manages structural geometry (nodes and elements)"""
    
    def __init__(self):
        self.nodes: Dict[int, Node] = {}
        self.elements: Dict[int, Element] = {}
        self.materials: Dict[str, Dict] = {}
        self.sections: Dict[str, Dict] = {}
        
        # Add default material and section
        self.add_material('default', E=200000, G=76923, density=7850e-9)
        self.add_section('default', A=5000, Iy=1e7, Iz=1e7, J=3e7)
    
    def add_node(self, id: int, x: float, y: float, z: float) -> Node:
        """Add node to model"""
        node = Node(id, x, y, z)
        self.nodes[id] = node
        return node
    
    def add_element(self, id: int, node_ids: List[int], element_type: str) -> Element:
        """Add element to model"""
        nodes = [self.nodes[nid] for nid in node_ids]
        element = Element(id, nodes, element_type)
        self.elements[id] = element
        return element
    
    def add_material(self, id: str, E: float, G: float = None, 
                    density: float = 7850e-9, nu: float = 0.3):
        """Add material properties"""
        if G is None:
            G = E / (2 * (1 + nu))
        
        self.materials[id] = {
            'E': E,  # Young's modulus (MPa)
            'G': G,  # Shear modulus (MPa)
            'density': density,  # kg/mm³
            'nu': nu  # Poisson's ratio
        }
    
    def add_section(self, id: str, A: float, Iy: float, Iz: float, J: float):
        """Add section properties"""
        self.sections[id] = {
            'A': A,    # Area (mm²)
            'Iy': Iy,  # Moment of inertia about y-axis (mm⁴)
            'Iz': Iz,  # Moment of inertia about z-axis (mm⁴)
            'J': J     # Torsion constant (mm⁴)
        }
    
    def get_restraints_dict(self) -> Dict[int, List[bool]]:
        """Get restraints for all nodes"""
        return {node_id: node.restraints for node_id, node in self.nodes.items()}
    
    def get_load_vector(self) -> np.ndarray:
        """Assemble global load vector"""
        n_dof = len(self.nodes) * 6
        F = np.zeros(n_dof)
        
        for node_id, node in self.nodes.items():
            for i, load in enumerate(node.loads):
                F[node_id * 6 + i] = load
        
        return F
    
    def validate_geometry(self) -> Tuple[bool, List[str]]:
        """
        Validate geometry for analysis
        
        Returns:
            (is_valid, list_of_errors)
        """
        errors = []
        
        # Check for nodes
        if len(self.nodes) == 0:
            errors.append("No nodes defined")
        
        # Check for elements
        if len(self.elements) == 0:
            errors.append("No elements defined")
        
        # Check for zero-length elements
        for elem_id, elem in self.elements.items():
            if elem.length() < 1e-6 and elem.element_type in ["beam", "column", "truss"]:
                errors.append(f"Element {elem_id} has zero or near-zero length")
        
        # Check for duplicate nodes
        positions = {}
        for node_id, node in self.nodes.items():
            pos = (round(node.x, 3), round(node.y, 3), round(node.z, 3))
            if pos in positions:
                errors.append(f"Nodes {positions[pos]} and {node_id} have same position")
            positions[pos] = node_id
        
        # Check for disconnected nodes
        connected_nodes = set()
        for elem in self.elements.values():
            for node in elem.nodes:
                connected_nodes.add(node.id)
        
        for node_id in self.nodes:
            if node_id not in connected_nodes:
                errors.append(f"Node {node_id} is not connected to any element")
        
        # Check for boundary conditions
        has_restraint = any(any(node.restraints) for node in self.nodes.values())
        if not has_restraint:
            errors.append("No boundary conditions defined (structure is unstable)")
        
        return (len(errors) == 0, errors)
    
    def get_model_info(self) -> Dict:
        """Get model statistics"""
        return {
            'n_nodes': len(self.nodes),
            'n_elements': len(self.elements),
            'n_dof': len(self.nodes) * 6,
            'element_types': list(set(e.element_type for e in self.elements.values())),
            'materials': list(self.materials.keys()),
            'sections': list(self.sections.keys())
        }
