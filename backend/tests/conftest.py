"""
Pytest configuration and fixtures
"""
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


@pytest.fixture
def sample_node_data():
    """Sample node data for testing"""
    return {
        'project_id': 1,
        'node_id': 'N1',
        'x': 0.0,
        'y': 0.0,
        'z': 0.0,
        'restraints': [True, True, True, False, False, False]
    }


@pytest.fixture
def sample_element_data():
    """Sample element data for testing"""
    return {
        'project_id': 1,
        'element_id': 'E1',
        'node_i': 'N1',
        'node_j': 'N2',
        'element_type': 'beam',
        'material_id': 'M1',
        'section_type': 'rectangular',
        'width': 0.3,
        'height': 0.5
    }


@pytest.fixture
def sample_material_data():
    """Sample material data for testing"""
    return {
        'project_id': 1,
        'material_id': 'M1',
        'name': 'Concrete M25',
        'E': 25000,
        'nu': 0.2,
        'density': 2500,
        'fy': 25,
        'material_type': 'concrete'
    }


@pytest.fixture
def sample_section_properties():
    """Sample section properties for testing"""
    return {
        'A': 150000,  # mm²
        'Iy': 3.125e9,  # mm⁴
        'Iz': 1.125e9,  # mm⁴
        'J': 1.0e8,  # mm⁴
        'd': 500,  # mm
        'b': 300,  # mm
    }


@pytest.fixture
def sample_steel_section():
    """Sample steel section for testing"""
    return {
        'A': 2400,  # mm²
        'rx': 50,  # mm
        'ry': 30,  # mm
        'Iz': 6000000,  # mm⁴
        'Iy': 2160000,  # mm⁴
        'Zp': 500000,  # mm³
        'Ze': 450000,  # mm³
        'd': 300,  # mm
        'tw': 8,  # mm
    }
