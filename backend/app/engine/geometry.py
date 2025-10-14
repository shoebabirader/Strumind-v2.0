import numpy as np
from typing import List, Dict

class Node:
    def __init__(self, id: int, x: float, y: float, z: float):
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.dof = [True] * 6  # 6 DOF: ux, uy, uz, rx, ry, rz

class Element:
    def __init__(self, id: int, nodes: List[Node], element_type: str):
        self.id = id
        self.nodes = nodes
        self.element_type = element_type  # beam, column, slab, shell, truss
        
    def length(self):
        if len(self.nodes) == 2:
            n1, n2 = self.nodes
            return np.sqrt((n2.x - n1.x)**2 + (n2.y - n1.y)**2 + (n2.z - n1.z)**2)
        return 0.0

class GeometryEngine:
    def __init__(self):
        self.nodes: Dict[int, Node] = {}
        self.elements: Dict[int, Element] = {}
    
    def add_node(self, id: int, x: float, y: float, z: float) -> Node:
        node = Node(id, x, y, z)
        self.nodes[id] = node
        return node
    
    def add_element(self, id: int, node_ids: List[int], element_type: str) -> Element:
        nodes = [self.nodes[nid] for nid in node_ids]
        element = Element(id, nodes, element_type)
        self.elements[id] = element
        return element
    
    def validate_geometry(self) -> bool:
        # Check for duplicate nodes, zero-length elements, etc.
        for elem in self.elements.values():
            if elem.length() < 1e-6 and elem.element_type in ["beam", "column", "truss"]:
                return False
        return True
