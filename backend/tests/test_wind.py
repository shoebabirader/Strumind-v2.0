import pytest
import numpy as np
from app.engine.wind import WindAnalysis, WindCode, TerrainCategory, BuildingClass

def test_wind_pressure_is875():
    """Test wind pressure calculation per IS 875"""
    analyzer = WindAnalysis(WindCode.IS875)
    analyzer.set_parameters(
        basic_wind_speed=44.0,
        terrain=TerrainCategory.CATEGORY_2,
        building_class=BuildingClass.CLASS_B,
        risk_coeff=1.0,
        topography=1.0
    )
    
    # Test at 30m height
    dimensions = {'width': 20, 'depth': 20, 'height': 30}
    result = analyzer.calculate_design_wind_pressure(30, dimensions)
    
    assert result["design_pressure"] > 0
    assert result["basic_wind_speed"] == 44.0
    assert result["code"] == "IS 875 Part 3:2015"
    assert "design_wind_speed" in result

def test_terrain_height_factor():
    """Test terrain and height factor calculation"""
    analyzer = WindAnalysis()
    
    # Category 2, 10m height
    analyzer.terrain_category = TerrainCategory.CATEGORY_2
    k2_10 = analyzer._terrain_height_factor_is875(10)
    assert k2_10 == pytest.approx(1.0, rel=0.01)
    
    # Category 2, 30m height
    k2_30 = analyzer._terrain_height_factor_is875(30)
    assert k2_30 > k2_10  # Should increase with height
    
    # Category 1 should have higher factor than Category 4
    analyzer.terrain_category = TerrainCategory.CATEGORY_1
    k2_cat1 = analyzer._terrain_height_factor_is875(30)
    
    analyzer.terrain_category = TerrainCategory.CATEGORY_4
    k2_cat4 = analyzer._terrain_height_factor_is875(30)
    
    assert k2_cat1 > k2_cat4

def test_wind_forces():
    """Test wind force calculation"""
    analyzer = WindAnalysis()
    
    pressures = [1000, 1200, 1400, 1600]  # N/m²
    areas = [100, 100, 100, 100]  # m²
    heights = [3, 6, 9, 12]  # m
    
    result = analyzer.calculate_wind_forces(pressures, areas, heights)
    
    assert len(result["story_forces"]) == 4
    assert result["total_force"] > 0
    assert result["total_moment"] > 0
    assert result["base_shear"] == result["total_force"]

def test_gust_factor():
    """Test gust effect factor calculation"""
    analyzer = WindAnalysis()
    
    result = analyzer.gust_factor_analysis(
        height=30,
        width=20,
        natural_frequency=1.5
    )
    
    assert result["gust_factor"] > 1.0  # Gust factor should be > 1
    assert result["gust_factor"] < 3.0  # Reasonable upper limit
    assert result["natural_frequency"] == 1.5
    assert "background_factor" in result

def test_along_wind_response():
    """Test along-wind dynamic response"""
    analyzer = WindAnalysis()
    analyzer.basic_wind_speed = 44.0
    
    result = analyzer.along_wind_response(
        height=30,
        width=20,
        depth=20,
        mass_per_floor=100000,  # kg
        damping_ratio=0.01
    )
    
    assert result["peak_force"] > result["mean_force"]
    assert result["gust_factor"] > 1.0
    assert result["displacement"] > 0
    assert "natural_frequency" in result

def test_across_wind_response():
    """Test across-wind (vortex shedding) response"""
    analyzer = WindAnalysis()
    analyzer.basic_wind_speed = 44.0
    
    result = analyzer.across_wind_response(
        height=30,
        width=20,
        depth=20,
        mass_per_floor=100000,
        damping_ratio=0.01
    )
    
    assert result["peak_force"] > 0
    assert result["critical_wind_speed"] > 0
    assert "is_critical" in result
    assert "recommendation" in result

def test_wind_load_combinations():
    """Test wind load combinations"""
    analyzer = WindAnalysis()
    
    result = analyzer.wind_load_combinations(
        wind_force=500,  # kN
        dead_load=2000,  # kN
        live_load=500,  # kN
        code="IS875"
    )
    
    assert "combinations" in result
    assert "governing" in result
    assert len(result["combinations"]) >= 3
    
    # Check that combinations are calculated correctly
    assert result["combinations"]["DL + WL"] == 2500

def test_cladding_pressure():
    """Test cladding pressure calculation"""
    analyzer = WindAnalysis()
    analyzer.basic_wind_speed = 44.0
    
    # Test corner zone (highest pressure)
    result_corner = analyzer.cladding_pressure(30, "corner")
    
    # Test interior zone (lowest pressure)
    result_interior = analyzer.cladding_pressure(30, "interior")
    
    assert result_corner["design_pressure"] > result_interior["design_pressure"]
    assert "positive_pressure" in result_corner
    assert "negative_pressure" in result_corner

def test_asce7_wind_pressure():
    """Test ASCE 7 wind pressure calculation"""
    analyzer = WindAnalysis(WindCode.ASCE7)
    analyzer.set_parameters(
        basic_wind_speed=115.0,  # mph
        terrain=TerrainCategory.CATEGORY_2,
        building_class=BuildingClass.CLASS_B,
        risk_coeff=1.0,
        topography=1.0
    )
    
    dimensions = {'width': 20, 'depth': 20, 'height': 30}
    result = analyzer.calculate_design_wind_pressure(30, dimensions)
    
    assert result["design_pressure"] > 0
    assert result["code"] == "ASCE 7"
    assert "velocity_pressure" in result
    assert "exposure_coefficient" in result

def test_external_pressure_coefficient():
    """Test external pressure coefficient calculation"""
    analyzer = WindAnalysis()
    
    # Low-rise building
    Cpe_low = analyzer._external_pressure_coefficient_is875(20, 20, 15, 10)
    
    # High-rise building
    Cpe_high = analyzer._external_pressure_coefficient_is875(20, 20, 60, 30)
    
    assert Cpe_high > Cpe_low  # Higher buildings have higher coefficients

def test_velocity_pressure_coefficient():
    """Test velocity pressure coefficient for ASCE 7"""
    analyzer = WindAnalysis(WindCode.ASCE7)
    
    # Test at different heights
    Kz_10 = analyzer._velocity_pressure_coefficient_asce7(10)
    Kz_30 = analyzer._velocity_pressure_coefficient_asce7(30)
    Kz_50 = analyzer._velocity_pressure_coefficient_asce7(50)
    
    assert Kz_30 > Kz_10  # Should increase with height
    assert Kz_50 > Kz_30

def test_wind_speed_variation():
    """Test wind pressure variation with wind speed"""
    analyzer = WindAnalysis()
    
    # Test with different wind speeds
    analyzer.basic_wind_speed = 33.0
    dimensions = {'width': 20, 'depth': 20, 'height': 30}
    result1 = analyzer.calculate_design_wind_pressure(30, dimensions)
    
    analyzer.basic_wind_speed = 50.0
    result2 = analyzer.calculate_design_wind_pressure(30, dimensions)
    
    # Pressure should increase with wind speed (quadratically)
    ratio = result2["design_pressure"] / result1["design_pressure"]
    expected_ratio = (50.0 / 33.0) ** 2
    assert ratio == pytest.approx(expected_ratio, rel=0.1)
