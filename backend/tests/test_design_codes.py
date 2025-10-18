"""
Unit tests for design codes
"""
import pytest
from app.engine.design_codes.is456_concrete import IS456ConcreteDesign
from app.engine.design_codes.is800_steel import IS800SteelDesign
from app.engine.design_codes.is1893_seismic import IS1893SeismicDesign, SeismicZone, SoilType


class TestIS456ConcreteDesign:
    """Test IS 456 concrete design"""
    
    def test_flexural_design_singly_reinforced(self):
        """Test singly reinforced beam design"""
        designer = IS456ConcreteDesign(fck=25, fy=415)
        result = designer.flexural_design_singly_reinforced(M=150, b=300, d=500)
        
        assert result['status'] in ['design_ok', 'minimum_steel_governs']
        assert result['Ast_required'] > 0
        assert result['design_ok'] is True
    
    def test_flexural_design_doubly_required(self):
        """Test when doubly reinforced is required"""
        designer = IS456ConcreteDesign(fck=25, fy=415)
        result = designer.flexural_design_singly_reinforced(M=500, b=300, d=500)
        
        assert result['status'] == 'doubly_reinforced_required'
    
    def test_shear_design(self):
        """Test shear design"""
        designer = IS456ConcreteDesign(fck=25, fy=415)
        result = designer.shear_design(V=100, b=300, d=500, Ast=1200)
        
        assert 'tau_v' in result
        assert 'tau_c' in result
        assert result['design_ok'] is not None
    
    def test_development_length(self):
        """Test development length calculation"""
        designer = IS456ConcreteDesign(fck=25, fy=415)
        Ld = designer.development_length(dia=16, stress_type='tension')
        
        assert Ld > 0
        assert isinstance(Ld, float)


class TestIS800SteelDesign:
    """Test IS 800 steel design"""
    
    def test_tension_member_design(self):
        """Test tension member design"""
        designer = IS800SteelDesign(fy=250, fu=410)
        result = designer.tension_member_design(T=500, Ag=2400, An=2160)
        
        assert 'Tdg_yielding' in result
        assert 'Tdn_rupture' in result
        assert result['design_ok'] is not None
    
    def test_compression_member_design(self):
        """Test compression member design"""
        designer = IS800SteelDesign(fy=250, fu=410)
        section = {'A': 2400, 'rx': 50, 'ry': 30, 'Iz': 6000000, 'Iy': 2160000}
        result = designer.compression_member_design(P=300, L=4000, section=section)
        
        assert 'lambda_max' in result
        assert 'Pd_capacity' in result
        assert result['design_ok'] is not None
    
    def test_beam_design(self):
        """Test beam design"""
        designer = IS800SteelDesign(fy=250, fu=410)
        section = {'Zp': 500000, 'Ze': 450000, 'd': 300, 'tw': 8}
        result = designer.beam_design(M=100, V=50, section=section)
        
        assert 'Md_capacity' in result
        assert 'Vd_capacity' in result
        assert result['design_ok'] is not None


class TestIS1893SeismicDesign:
    """Test IS 1893 seismic design"""
    
    def test_base_shear_calculation(self):
        """Test base shear calculation"""
        designer = IS1893SeismicDesign(
            zone=SeismicZone.ZONE_III,
            soil_type=SoilType.TYPE_II
        )
        result = designer.base_shear(W=10000, T=1.0, R=5.0)
        
        assert 'V_B' in result
        assert 'Ah' in result
        assert result['V_B'] > 0
    
    def test_fundamental_period(self):
        """Test fundamental period calculation"""
        designer = IS1893SeismicDesign(
            zone=SeismicZone.ZONE_III,
            soil_type=SoilType.TYPE_II
        )
        T = designer.fundamental_period(h=30, building_type='RC_MRF')
        
        assert T > 0
        assert T < 5.0  # Reasonable range
    
    def test_story_drift_check(self):
        """Test story drift check"""
        designer = IS1893SeismicDesign(
            zone=SeismicZone.ZONE_III,
            soil_type=SoilType.TYPE_II
        )
        result = designer.story_drift_check(delta_i=0.010, h_i=3.0, building_type='RC')
        
        assert 'drift_ok' in result
        assert 'drift_ratio' in result
    
    def test_design_spectrum(self):
        """Test design spectrum generation"""
        designer = IS1893SeismicDesign(
            zone=SeismicZone.ZONE_III,
            soil_type=SoilType.TYPE_II
        )
        T, Sa_g = designer.design_spectrum()
        
        assert len(T) == len(Sa_g)
        assert all(sa >= 0 for sa in Sa_g)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
