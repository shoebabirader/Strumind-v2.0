import pytest
import numpy as np
from app.engine.geometry import GeometryEngine, Node, Element
from app.engine.analysis import StructuralAnalysis

def test_node_creation():
    node = Node(1, 0, 0, 0)
    assert node.id == 1
    assert node.x == 0
    assert len(node.dof) == 6

def test_element_length():
    n1 = Node(1, 0, 0, 0)
    n2 = Node(2, 5, 0, 0)
    elem = Element(1, [n1, n2], "beam")
    assert elem.length() == 5.0

def test_geometry_validation():
    geom = GeometryEngine()
    geom.add_node(1, 0, 0, 0)
    geom.add_node(2, 5, 0, 0)
    geom.add_element(1, [1, 2], "beam")
    assert geom.validate_geometry() == True

def test_static_analysis():
    geom = GeometryEngine()
    geom.add_node(1, 0, 0, 0)
    geom.add_node(2, 5, 0, 0)
    geom.add_element(1, [1, 2], "truss")
    
    analyzer = StructuralAnalysis(geom)
    material_props = {'E': 2e11}
    section_props = {'A': 0.01}
    
    K = analyzer.assemble_stiffness_matrix(material_props, section_props)
    assert K is not None
