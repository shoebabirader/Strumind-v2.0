"""
Unit tests for validators
"""
import pytest
import numpy as np
from app.core.validators import (
    NodeValidator, MaterialValidator, SectionValidator,
    LoadValidator, GeometryValidator, AnalysisValidator
)


class TestNodeValidator:
    """Test node validation"""
    
    def test_valid_coordinates(self):
        """Test valid coordinates"""
        is_valid, error = NodeValidator.validate_coordinates(100.0, 200.0, 300.0)
        assert is_valid is True
        assert error is None
    
    def test_nan_coordinates(self):
        """Test NaN coordinates"""
        is_valid, error = NodeValidator.validate_coordinates(np.nan, 200.0, 300.0)
        assert is_valid is False
        assert "finite" in error.lower()
    
    def test_out_of_range_coordinates(self):
        """Test out of range coordinates"""
        is_valid, error = NodeValidator.validate_coordinates(2e6, 200.0, 300.0)
        assert is_valid is False
        assert "range" in error.lower()


class TestMaterialValidator:
    """Test material validation"""
    
    def test_valid_elastic_modulus(self):
        """Test valid E"""
        is_valid, error = MaterialValidator.validate_elastic_modulus(200000)
        assert is_valid is True
    
    def test_negative_elastic_modulus(self):
        """Test negative E"""
        is_valid, error = MaterialValidator.validate_elastic_modulus(-1000)
        assert is_valid is False
    
    def test_valid_poisson_ratio(self):
        """Test valid Poisson's ratio"""
        is_valid, error = MaterialValidator.validate_poisson_ratio(0.3)
        assert is_valid is True
    
    def test_invalid_poisson_ratio(self):
        """Test invalid Poisson's ratio"""
        is_valid, error = MaterialValidator.validate_poisson_ratio(0.6)
        assert is_valid is False
    
    def test_yield_stress_validation(self):
        """Test yield stress validation"""
        is_valid, error = MaterialValidator.validate_yield_stress(250, 410)
        assert is_valid is True
        
        is_valid, error = MaterialValidator.validate_yield_stress(500, 410)
        assert is_valid is False


class TestSectionValidator:
    """Test section validation"""
    
    def test_valid_area(self):
        """Test valid area"""
        is_valid, error = SectionValidator.validate_area(10000)
        assert is_valid is True
    
    def test_zero_area(self):
        """Test zero area"""
        is_valid, error = SectionValidator.validate_area(0)
        assert is_valid is False
    
    def test_valid_section_properties(self):
        """Test valid section properties"""
        is_valid, error = SectionValidator.validate_section_properties(
            A=10000, Iy=1e7, Iz=1e7, J=1e6
        )
        assert is_valid is True


class TestLoadValidator:
    """Test load validation"""
    
    def test_valid_force(self):
        """Test valid force"""
        is_valid, error = LoadValidator.validate_force(10000, "X")
        assert is_valid is True
    
    def test_excessive_force(self):
        """Test excessive force"""
        is_valid, error = LoadValidator.validate_force(1e10, "X")
        assert is_valid is False
    
    def test_valid_moment(self):
        """Test valid moment"""
        is_valid, error = LoadValidator.validate_moment(1e6, "X")
        assert is_valid is True


class TestGeometryValidator:
    """Test geometry validation"""
    
    def test_valid_element_length(self):
        """Test valid element length"""
        is_valid, error = GeometryValidator.validate_element_length(1000)
        assert is_valid is True
    
    def test_zero_length_element(self):
        """Test zero length element"""
        is_valid, error = GeometryValidator.validate_element_length(0.5)
        assert is_valid is False
    
    def test_stability_check(self):
        """Test stability check"""
        is_valid, error = GeometryValidator.check_stability(
            n_nodes=10, n_restraints=6, dimension=3
        )
        assert is_valid is True
        
        is_valid, error = GeometryValidator.check_stability(
            n_nodes=10, n_restraints=3, dimension=3
        )
        assert is_valid is False


class TestAnalysisValidator:
    """Test analysis validation"""
    
    def test_valid_convergence_tolerance(self):
        """Test valid tolerance"""
        is_valid, error = AnalysisValidator.validate_convergence_tolerance(1e-6)
        assert is_valid is True
    
    def test_invalid_convergence_tolerance(self):
        """Test invalid tolerance"""
        is_valid, error = AnalysisValidator.validate_convergence_tolerance(1e-15)
        assert is_valid is False
    
    def test_valid_max_iterations(self):
        """Test valid max iterations"""
        is_valid, error = AnalysisValidator.validate_max_iterations(50)
        assert is_valid is True
    
    def test_invalid_max_iterations(self):
        """Test invalid max iterations"""
        is_valid, error = AnalysisValidator.validate_max_iterations(0)
        assert is_valid is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
