"""
Wind Load Analysis Module
Supports: IS 875 Part 3, ASCE 7, AS 1170.2, Eurocode 1
"""
import numpy as np
from typing import Dict, List, Tuple
from enum import Enum

class WindCode(Enum):
    IS875 = "IS875"
    ASCE7 = "ASCE7"
    AS1170 = "AS1170"
    EUROCODE1 = "EC1"

class TerrainCategory(Enum):
    # IS 875 Terrain Categories
    CATEGORY_1 = 1  # Exposed open terrain
    CATEGORY_2 = 2  # Open terrain with scattered obstructions
    CATEGORY_3 = 3  # Terrain with numerous obstructions
    CATEGORY_4 = 4  # Terrain with large and closely spaced obstructions

class BuildingClass(Enum):
    # IS 875 Building Classes
    CLASS_A = "A"  # Temporary structures
    CLASS_B = "B"  # Normal buildings
    CLASS_C = "C"  # Important buildings

class WindAnalysis:
    """Comprehensive wind load analysis engine"""
    
    def __init__(self, code: WindCode = WindCode.IS875):
        self.code = code
        self.basic_wind_speed = 44.0  # m/s (default for IS 875)
        self.terrain_category = TerrainCategory.CATEGORY_2
        self.building_class = BuildingClass.CLASS_B
        self.risk_coefficient = 1.0
        self.topography_factor = 1.0
        
    def set_parameters(self, basic_wind_speed: float, terrain: TerrainCategory,
                       building_class: BuildingClass, risk_coeff: float = 1.0,
                       topography: float = 1.0):
        """Set wind analysis parameters"""
        self.basic_wind_speed = basic_wind_speed
        self.terrain_category = terrain
        self.building_class = building_class
        self.risk_coefficient = risk_coeff
        self.topography_factor = topography
    
    def calculate_design_wind_pressure(self, height: float, 
                                       building_dimensions: Dict) -> Dict:
        """Calculate design wind pressure per IS 875"""
        if self.code == WindCode.IS875:
            return self._wind_pressure_is875(height, building_dimensions)
        elif self.code == WindCode.ASCE7:
            return self._wind_pressure_asce7(height, building_dimensions)
        else:
            raise NotImplementedError(f"Code {self.code} not implemented")
    
    def _wind_pressure_is875(self, height: float, dimensions: Dict) -> Dict:
        """IS 875 Part 3:2015 Wind Pressure Calculation"""
        Vb = self.basic_wind_speed
        k1 = self.risk_coefficient
        k2 = self._terrain_height_factor_is875(height)
        k3 = self.topography_factor
        k4 = 1.0  # Importance factor (simplified)
        
        # Design wind speed
        Vz = Vb * k1 * k2 * k3 * k4
        
        # Design wind pressure
        pz = 0.6 * (Vz ** 2)  # N/m² (0.6 is air density factor)
        
        # External pressure coefficients (simplified)
        width = dimensions.get('width', 20)
        depth = dimensions.get('depth', 20)
        height_total = dimensions.get('height', 30)
        
        # Calculate pressure coefficients
        Cpe = self._external_pressure_coefficient_is875(
            width, depth, height_total, height
        )
        
        # Internal pressure coefficient
        Cpi = 0.2  # Assuming normal permeability
        
        # Net pressure coefficient
        Cp_net = Cpe - Cpi
        
        # Design pressure
        pd = pz * Cp_net
        
        return {
            "design_pressure": pd,
            "design_wind_speed": Vz,
            "basic_wind_speed": Vb,
            "risk_coefficient": k1,
            "terrain_height_factor": k2,
            "topography_factor": k3,
            "external_pressure_coeff": Cpe,
            "internal_pressure_coeff": Cpi,
            "net_pressure_coeff": Cp_net,
            "height": height,
            "code": "IS 875 Part 3:2015"
        }
    
    def _terrain_height_factor_is875(self, height: float) -> float:
        """Calculate terrain and height factor k2 per IS 875"""
        cat = self.terrain_category.value
        h = height  # in meters
        
        # IS 875 Table 33 - Terrain and height factor
        if cat == 1:  # Category 1
            k2 = 1.05 if h <= 10 else 1.05 * (h/10)**0.12
        elif cat == 2:  # Category 2
            k2 = 1.00 if h <= 10 else 1.00 * (h/10)**0.14
        elif cat == 3:  # Category 3
            k2 = 0.91 if h <= 10 else 0.91 * (h/10)**0.17
        else:  # Category 4
            k2 = 0.80 if h <= 10 else 0.80 * (h/10)**0.20
        
        return k2
    
    def _external_pressure_coefficient_is875(self, width: float, depth: float,
                                            height: float, z: float) -> float:
        """Calculate external pressure coefficient per IS 875"""
        # Simplified - windward wall
        # For detailed analysis, need to consider all faces
        
        # Aspect ratio
        h_w = height / width
        
        # Windward wall (positive pressure)
        if h_w <= 1:
            Cpe = 0.7
        elif h_w <= 2:
            Cpe = 0.75
        elif h_w <= 4:
            Cpe = 0.8
        else:
            Cpe = 0.85
        
        return Cpe
    
    def _wind_pressure_asce7(self, height: float, dimensions: Dict) -> Dict:
        """ASCE 7 Wind Pressure Calculation"""
        # Simplified ASCE 7 method
        V = self.basic_wind_speed  # mph
        
        # Velocity pressure exposure coefficient
        Kz = self._velocity_pressure_coefficient_asce7(height)
        
        # Topographic factor
        Kzt = self.topography_factor
        
        # Directionality factor
        Kd = 0.85  # For buildings
        
        # Velocity pressure
        qz = 0.613 * Kz * Kzt * Kd * (V ** 2)  # N/m²
        
        # External pressure coefficient (simplified)
        Cp = 0.8  # Windward wall
        
        # Internal pressure coefficient
        GCpi = 0.18  # Enclosed building
        
        # Design pressure
        p = qz * (Cp - GCpi)
        
        return {
            "design_pressure": p,
            "velocity_pressure": qz,
            "basic_wind_speed": V,
            "exposure_coefficient": Kz,
            "topographic_factor": Kzt,
            "directionality_factor": Kd,
            "external_pressure_coeff": Cp,
            "internal_pressure_coeff": GCpi,
            "height": height,
            "code": "ASCE 7"
        }
    
    def _velocity_pressure_coefficient_asce7(self, height: float) -> float:
        """Calculate velocity pressure exposure coefficient per ASCE 7"""
        # Exposure B (suburban terrain)
        z = height  # in meters
        zg = 365.76  # gradient height in meters
        alpha = 7.0  # power law exponent
        
        if z < 9.14:  # Below 30 ft
            z = 9.14
        
        Kz = 2.01 * ((z / zg) ** (2 / alpha))
        
        return Kz
    
    def calculate_wind_forces(self, pressures: List[float], 
                             areas: List[float],
                             heights: List[float]) -> Dict:
        """Calculate wind forces on building"""
        forces = []
        moments = []
        
        for p, A, h in zip(pressures, areas, heights):
            F = p * A / 1000  # Convert to kN
            M = F * h  # Moment about base
            forces.append(F)
            moments.append(M)
        
        total_force = sum(forces)
        total_moment = sum(moments)
        
        return {
            "story_forces": forces,
            "story_moments": moments,
            "total_force": total_force,
            "total_moment": total_moment,
            "base_shear": total_force
        }
    
    def gust_factor_analysis(self, height: float, width: float, 
                            natural_frequency: float = None) -> Dict:
        """Calculate gust effect factor per IS 875"""
        h = height
        b = width
        
        # Estimate natural frequency if not provided
        if natural_frequency is None:
            # Empirical formula
            f1 = 46 / h  # Hz
        else:
            f1 = natural_frequency
        
        # Background factor
        B = 1 / (1 + 0.9 * ((b + h) / 100) ** 0.63)
        
        # Size reduction factor
        S = 1 / (1 + 3.5 * f1 * ((b + h) / 100))
        
        # Energy ratio
        E = 1 / (1 + 2 * f1)
        
        # Gust factor
        G = 0.5 + np.sqrt(B**2 + (S * E)**2)
        
        return {
            "gust_factor": G,
            "natural_frequency": f1,
            "background_factor": B,
            "size_reduction_factor": S,
            "energy_ratio": E,
            "height": h,
            "width": b
        }
    
    def along_wind_response(self, height: float, width: float, depth: float,
                           mass_per_floor: float, damping_ratio: float = 0.01) -> Dict:
        """Calculate along-wind dynamic response"""
        h = height
        b = width
        d = depth
        
        # Natural frequency (empirical)
        f1 = 46 / h  # Hz
        
        # Mode shape factor
        Cf = 1.0  # First mode
        
        # Gust factor
        gust = self.gust_factor_analysis(h, b, f1)
        G = gust["gust_factor"]
        
        # Mean wind load
        Vz = self.basic_wind_speed * self._terrain_height_factor_is875(h)
        pz = 0.6 * (Vz ** 2)
        Fmean = pz * b * h * 0.8  # Simplified
        
        # Peak wind load
        Fpeak = G * Fmean
        
        # Dynamic displacement
        omega = 2 * np.pi * f1
        k = (mass_per_floor * h) * (omega ** 2)  # Stiffness
        displacement = Fpeak / k
        
        return {
            "peak_force": Fpeak / 1000,  # kN
            "mean_force": Fmean / 1000,  # kN
            "gust_factor": G,
            "natural_frequency": f1,
            "displacement": displacement * 1000,  # mm
            "damping_ratio": damping_ratio
        }
    
    def across_wind_response(self, height: float, width: float, depth: float,
                            mass_per_floor: float, damping_ratio: float = 0.01) -> Dict:
        """Calculate across-wind (vortex shedding) response"""
        h = height
        b = width
        d = depth
        
        # Natural frequency
        f1 = 46 / h  # Hz
        
        # Strouhal number
        St = 0.2  # For rectangular buildings
        
        # Critical wind speed for vortex shedding
        Vcrit = (f1 * b) / St
        
        # Check if critical speed is within design range
        Vdesign = self.basic_wind_speed * 1.5  # Peak gust
        
        is_critical = abs(Vcrit - Vdesign) / Vdesign < 0.2
        
        # Across-wind force coefficient
        Cy = 0.1  # Typical for rectangular buildings
        
        # RMS across-wind force
        rho = 1.2  # Air density kg/m³
        Fy_rms = 0.5 * rho * (Vdesign ** 2) * h * d * Cy
        
        # Peak factor
        gp = 3.5  # For 10-minute mean
        
        # Peak across-wind force
        Fy_peak = gp * Fy_rms
        
        # Displacement
        omega = 2 * np.pi * f1
        k = (mass_per_floor * h) * (omega ** 2)
        displacement = Fy_peak / k
        
        return {
            "peak_force": Fy_peak / 1000,  # kN
            "rms_force": Fy_rms / 1000,  # kN
            "critical_wind_speed": Vcrit,
            "design_wind_speed": Vdesign,
            "is_critical": is_critical,
            "strouhal_number": St,
            "displacement": displacement * 1000,  # mm
            "recommendation": "Consider wind tunnel test" if is_critical else "OK"
        }
    
    def wind_load_combinations(self, wind_force: float, dead_load: float,
                              live_load: float, code: str = "IS875") -> Dict:
        """Generate wind load combinations"""
        if code == "IS875":
            # IS 875 load combinations
            combinations = {
                "DL + WL": dead_load + wind_force,
                "DL + 0.8LL + WL": dead_load + 0.8 * live_load + wind_force,
                "0.9DL + WL": 0.9 * dead_load + wind_force
            }
        else:  # ASCE 7
            combinations = {
                "1.2D + 1.0W + 0.5L": 1.2 * dead_load + 1.0 * wind_force + 0.5 * live_load,
                "0.9D + 1.0W": 0.9 * dead_load + 1.0 * wind_force
            }
        
        return {
            "combinations": combinations,
            "governing": max(combinations.items(), key=lambda x: x[1]),
            "code": code
        }
    
    def cladding_pressure(self, height: float, zone: str = "interior") -> Dict:
        """Calculate cladding and component pressures"""
        # Design wind pressure at height
        result = self.calculate_design_wind_pressure(height, {
            'width': 20, 'depth': 20, 'height': height
        })
        
        pz = result["design_pressure"]
        
        # Cladding pressure coefficients (IS 875)
        if zone == "corner":
            Cpe_pos = 0.8
            Cpe_neg = -1.5
        elif zone == "edge":
            Cpe_pos = 0.7
            Cpe_neg = -1.2
        else:  # interior
            Cpe_pos = 0.7
            Cpe_neg = -0.8
        
        Cpi = 0.2  # Internal pressure
        
        # Positive and negative pressures
        p_pos = pz * (Cpe_pos - Cpi)
        p_neg = pz * (Cpe_neg - Cpi)
        
        # Design pressure (maximum absolute)
        p_design = max(abs(p_pos), abs(p_neg))
        
        return {
            "positive_pressure": p_pos,
            "negative_pressure": p_neg,
            "design_pressure": p_design,
            "zone": zone,
            "height": height,
            "external_coeff_pos": Cpe_pos,
            "external_coeff_neg": Cpe_neg
        }
