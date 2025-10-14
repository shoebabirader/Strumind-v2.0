import pytest
import numpy as np
from app.engine.seismic import SeismicAnalysis, SeismicCode, SeismicZone, SoilType

def test_base_shear_is1893():
    """Test base shear calculation per IS 1893"""
    analyzer = SeismicAnalysis(SeismicCode.IS1893)
    analyzer.set_parameters(
        zone=SeismicZone.ZONE_IV,
        importance=1.0,
        response_reduction=5.0,
        soil=SoilType.MEDIUM
    )
    
    # Test case: 10-story building
    total_weight = 10000  # kN
    time_period = 1.0  # seconds
    
    result = analyzer.calculate_base_shear(total_weight, time_period)
    
    assert result["base_shear"] > 0
    assert result["zone_factor"] == 0.24
    assert result["code"] == "IS 1893:2016"
    assert "seismic_coefficient" in result

def test_time_period_calculation():
    """Test fundamental time period calculation"""
    analyzer = SeismicAnalysis()
    
    # RC moment frame, 30m height
    T = analyzer.calculate_time_period(30.0, "RC_MRF")
    
    assert T > 0
    assert T < 5.0  # Reasonable range
    
    # Steel frame should have higher period
    T_steel = analyzer.calculate_time_period(30.0, "STEEL_MRF")
    assert T_steel > T

def test_story_drift_check():
    """Test story drift limits"""
    analyzer = SeismicAnalysis()
    
    # Story displacements in mm
    displacements = [0, 10, 22, 36, 52]
    heights = [0, 3000, 6000, 9000, 12000]
    
    result = analyzer.story_drift_check(displacements, heights)
    
    assert "checks" in result
    assert "overall_status" in result
    assert len(result["checks"]) == 4  # 4 stories above ground

def test_torsional_irregularity():
    """Test torsional irregularity check"""
    analyzer = SeismicAnalysis()
    
    # Regular building
    result1 = analyzer.torsional_irregularity_check(10.0, 9.0)
    assert result1["is_irregular"] == False
    
    # Irregular building
    result2 = analyzer.torsional_irregularity_check(15.0, 10.0)
    assert result2["is_irregular"] == True

def test_soft_story_check():
    """Test soft story detection"""
    analyzer = SeismicAnalysis()
    
    # Normal stiffness distribution
    stiffnesses1 = [1000, 950, 900, 850]
    result1 = analyzer.soft_story_check(stiffnesses1)
    assert result1["has_soft_story"] == False
    
    # Soft story at level 2
    stiffnesses2 = [1000, 600, 900, 850]
    result2 = analyzer.soft_story_check(stiffnesses2)
    assert result2["has_soft_story"] == True

def test_load_distribution():
    """Test seismic load distribution"""
    analyzer = SeismicAnalysis()
    
    base_shear = 1000  # kN
    story_weights = [500, 500, 500, 500]  # kN
    story_heights = [3, 6, 9, 12]  # m
    
    result = analyzer.seismic_load_distribution(
        base_shear, story_weights, story_heights
    )
    
    assert len(result["story_forces"]) == 4
    assert sum(result["story_forces"]) == pytest.approx(base_shear, rel=0.01)
    assert result["cumulative_shear"][0] == pytest.approx(base_shear, rel=0.01)

def test_response_spectrum_analysis():
    """Test response spectrum analysis"""
    analyzer = SeismicAnalysis(SeismicCode.IS1893)
    analyzer.set_parameters(
        zone=SeismicZone.ZONE_IV,
        importance=1.0,
        response_reduction=5.0,
        soil=SoilType.MEDIUM
    )
    
    # Simple 2-DOF system
    M = np.array([[1000, 0], [0, 1000]])
    K = np.array([[2000, -1000], [-1000, 1000]])
    
    result = analyzer.response_spectrum_analysis(M, K)
    
    assert len(result["frequencies"]) == 2
    assert len(result["periods"]) == 2
    assert result["total_base_shear_srss"] > 0

def test_spectral_acceleration():
    """Test spectral acceleration calculation"""
    analyzer = SeismicAnalysis()
    analyzer.soil_type = SoilType.MEDIUM
    
    # Test different periods
    Sa_short = analyzer._spectral_acceleration_is1893(0.3)
    Sa_medium = analyzer._spectral_acceleration_is1893(1.0)
    Sa_long = analyzer._spectral_acceleration_is1893(3.0)
    
    assert Sa_short > 0
    assert Sa_medium > 0
    assert Sa_long > 0
    assert Sa_short >= Sa_medium  # Generally true for medium soil

def test_asce7_base_shear():
    """Test ASCE 7 base shear calculation"""
    analyzer = SeismicAnalysis(SeismicCode.ASCE7)
    analyzer.set_parameters(
        zone=SeismicZone.ZONE_IV,  # Not used in ASCE 7 but required
        importance=1.0,
        response_reduction=8.0,
        soil=SoilType.MEDIUM
    )
    
    total_weight = 10000  # kN
    time_period = 1.0  # seconds
    
    result = analyzer.calculate_base_shear(total_weight, time_period)
    
    assert result["base_shear"] > 0
    assert result["code"] == "ASCE 7"
    assert "Sds" in result
    assert "Sd1" in result
