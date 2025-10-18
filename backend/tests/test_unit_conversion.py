"""
Unit tests for unit conversion system
"""
import pytest
import numpy as np
from app.engine.units_system import UnitConverter, STANDARD_MATERIALS


class TestUnitConverter:
    """Test unit conversion utilities"""
    
    def test_length_conversions(self):
        """Test length unit conversions"""
        # mm to m
        assert UnitConverter.MM_TO_M == 1e-3
        assert 1000 * UnitConverter.MM_TO_M == 1.0
        
        # m to mm
        assert UnitConverter.M_TO_MM == 1e3
        assert 1.0 * UnitConverter.M_TO_MM == 1000
    
    def test_force_conversions(self):
        """Test force unit conversions"""
        # kN to N
        assert UnitConverter.KN_TO_N == 1e3
        assert 10 * UnitConverter.KN_TO_N == 10000
        
        # N to kN
        assert UnitConverter.N_TO_KN == 1e-3
        assert 10000 * UnitConverter.N_TO_KN == 10
    
    def test_stress_conversions(self):
        """Test stress unit conversions"""
        # MPa to Pa
        assert UnitConverter.MPA_TO_PA == 1e6
        assert 200 * UnitConverter.MPA_TO_PA == 200e6
        
        # Pa to MPa
        assert UnitConverter.PA_TO_MPA == 1e-6
        assert 200e6 * UnitConverter.PA_TO_MPA == 200
    
    def test_area_conversions(self):
        """Test area unit conversions"""
        # mm² to m²
        assert UnitConverter.MM2_TO_M2 == 1e-6
        assert 1e6 * UnitConverter.MM2_TO_M2 == 1.0
    
    def test_moment_of_inertia_conversions(self):
        """Test moment of inertia conversions"""
        # mm⁴ to m⁴
        assert UnitConverter.MM4_TO_M4 == 1e-12
        assert 1e12 * UnitConverter.MM4_TO_M4 == 1.0
    
    def test_standardize_material(self):
        """Test material property standardization"""
        result = UnitConverter.standardize_material(
            E_MPa=200000,
            nu=0.3,
            density_kg_m3=7850,
            fy_MPa=415
        )
        
        assert result['E'] == 200000e6  # Pa
        assert result['nu'] == 0.3
        assert result['density'] == 7850
        assert result['fy'] == 415e6  # Pa
    
    def test_standardize_section(self):
        """Test section property standardization"""
        result = UnitConverter.standardize_section(
            A_mm2=5000,
            Iy_mm4=1e8,
            Iz_mm4=5e7,
            J_mm4=2e7
        )
        
        assert result['A'] == 5000e-6  # m²
        assert result['Iy'] == 1e8 * 1e-12  # m⁴
        assert result['Iz'] == 5e7 * 1e-12  # m⁴
        assert result['J'] == 2e7 * 1e-12  # m⁴
    
    def test_standardize_coordinates(self):
        """Test coordinate standardization"""
        x_m, y_m, z_m = UnitConverter.standardize_coordinates(
            x_mm=1000,
            y_mm=2000,
            z_mm=3000
        )
        
        assert x_m == 1.0
        assert y_m == 2.0
        assert z_m == 3.0
    
    def test_standardize_forces(self):
        """Test force and moment standardization"""
        result = UnitConverter.standardize_forces(
            fx_kN=10,
            fy_kN=20,
            fz_kN=30,
            mx_kNm=5,
            my_kNm=10,
            mz_kNm=15
        )
        
        assert result['fx'] == 10000  # N
        assert result['fy'] == 20000  # N
        assert result['fz'] == 30000  # N
        assert result['mx'] == 5000  # N·m
        assert result['my'] == 10000  # N·m
        assert result['mz'] == 15000  # N·m
    
    def test_to_engineering_units(self):
        """Test conversion to engineering units"""
        result = UnitConverter.to_engineering_units(
            displacement_m=0.01,
            force_N=10000,
            stress_Pa=200e6,
            moment_Nm=5000
        )
        
        assert result['displacement_mm'] == 10
        assert result['force_kN'] == 10
        assert result['stress_MPa'] == 200
        assert result['moment_kNm'] == 5
    
    def test_standard_materials(self):
        """Test standard material properties"""
        # Test concrete M25
        concrete = STANDARD_MATERIALS['concrete_M25']
        assert concrete['E'] == 25000e6  # Pa
        assert concrete['nu'] == 0.2
        assert concrete['density'] == 2500  # kg/m³
        
        # Test steel Fe415
        steel = STANDARD_MATERIALS['steel_Fe415']
        assert steel['E'] == 200000e6  # Pa
        assert steel['nu'] == 0.3
        assert steel['density'] == 7850  # kg/m³
        assert steel['fy'] == 415e6  # Pa
    
    def test_dimensional_consistency(self):
        """Test dimensional consistency of conversions"""
        # EA/L should have units of N/m
        E_Pa = 200000 * UnitConverter.MPA_TO_PA
        A_m2 = 5000 * UnitConverter.MM2_TO_M2
        L_m = 6000 * UnitConverter.MM_TO_M
        
        stiffness = E_Pa * A_m2 / L_m  # N/m
        
        # Should be a reasonable stiffness value
        assert stiffness > 0
        assert stiffness < 1e12  # Reasonable upper bound


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
