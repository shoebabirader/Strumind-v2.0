"""
Seismic Analysis Module
Supports: IS 1893, ASCE 7, Eurocode 8, UBC
"""
import numpy as np
from typing import Dict, List, Tuple
from enum import Enum

class SeismicCode(Enum):
    IS1893 = "IS1893"
    ASCE7 = "ASCE7"
    EUROCODE8 = "EC8"
    UBC = "UBC"

class SeismicZone(Enum):
    # IS 1893 Zones
    ZONE_II = 0.10
    ZONE_III = 0.16
    ZONE_IV = 0.24
    ZONE_V = 0.36

class SoilType(Enum):
    # IS 1893 Soil Types
    ROCK = "I"
    MEDIUM = "II"
    SOFT = "III"

class SeismicAnalysis:
    """Comprehensive seismic analysis engine"""
    
    def __init__(self, code: SeismicCode = SeismicCode.IS1893):
        self.code = code
        self.zone_factor = None
        self.importance_factor = 1.0
        self.response_reduction_factor = 5.0
        self.soil_type = SoilType.MEDIUM
        
    def set_parameters(self, zone: SeismicZone, importance: float, 
                       response_reduction: float, soil: SoilType):
        """Set seismic parameters"""
        self.zone_factor = zone.value
        self.importance_factor = importance
        self.response_reduction_factor = response_reduction
        self.soil_type = soil
    
    def calculate_base_shear(self, total_weight: float, time_period: float) -> Dict:
        """Calculate seismic base shear per IS 1893"""
        if self.code == SeismicCode.IS1893:
            return self._base_shear_is1893(total_weight, time_period)
        elif self.code == SeismicCode.ASCE7:
            return self._base_shear_asce7(total_weight, time_period)
        else:
            raise NotImplementedError(f"Code {self.code} not implemented")
    
    def _base_shear_is1893(self, W: float, T: float) -> Dict:
        """IS 1893:2016 Base Shear Calculation"""
        Z = self.zone_factor
        I = self.importance_factor
        R = self.response_reduction_factor
        
        # Spectral acceleration coefficient
        Sa_g = self._spectral_acceleration_is1893(T)
        
        # Design horizontal seismic coefficient
        Ah = (Z * I * Sa_g) / (2 * R)
        
        # Base shear
        Vb = Ah * W
        
        return {
            "base_shear": Vb,
            "seismic_coefficient": Ah,
            "zone_factor": Z,
            "importance_factor": I,
            "response_reduction": R,
            "spectral_acceleration": Sa_g,
            "time_period": T,
            "code": "IS 1893:2016"
        }
    
    def _spectral_acceleration_is1893(self, T: float) -> float:
        """Calculate spectral acceleration coefficient per IS 1893"""
        # Soil type factors
        if self.soil_type == SoilType.ROCK:
            Sa_g = 1.0 if T <= 0.10 else (1.0/T if T <= 0.40 else 1.0/(T**2))
        elif self.soil_type == SoilType.MEDIUM:
            Sa_g = 1.0 if T <= 0.55 else (1.36/T if T <= 4.0 else 1.0)
        else:  # SOFT
            Sa_g = 1.0 if T <= 0.67 else (1.67/T if T <= 4.0 else 1.0)
        
        return min(Sa_g, 2.5)
    
    def _base_shear_asce7(self, W: float, T: float) -> Dict:
        """ASCE 7 Base Shear Calculation"""
        # Simplified for demonstration
        Ss = 1.5  # Short period spectral acceleration
        S1 = 0.6  # 1-second spectral acceleration
        
        Sds = (2/3) * Ss
        Sd1 = (2/3) * S1
        
        Cs = Sds / (self.response_reduction_factor / self.importance_factor)
        Cs = min(Cs, Sd1 / (T * (self.response_reduction_factor / self.importance_factor)))
        Cs = max(Cs, 0.044 * Sds * self.importance_factor)
        
        Vb = Cs * W
        
        return {
            "base_shear": Vb,
            "seismic_coefficient": Cs,
            "Sds": Sds,
            "Sd1": Sd1,
            "time_period": T,
            "code": "ASCE 7"
        }
    
    def response_spectrum_analysis(self, mass_matrix: np.ndarray, 
                                   stiffness_matrix: np.ndarray,
                                   damping_ratio: float = 0.05) -> Dict:
        """Perform response spectrum analysis"""
        # Eigenvalue analysis
        eigenvalues, eigenvectors = np.linalg.eig(
            np.linalg.inv(mass_matrix) @ stiffness_matrix
        )
        
        # Natural frequencies
        omega = np.sqrt(np.abs(eigenvalues))
        frequencies = omega / (2 * np.pi)
        periods = 1 / frequencies
        
        # Modal participation factors
        ones = np.ones(mass_matrix.shape[0])
        participation_factors = []
        
        for i in range(len(eigenvalues)):
            phi = eigenvectors[:, i]
            gamma = (phi.T @ mass_matrix @ ones) / (phi.T @ mass_matrix @ phi)
            participation_factors.append(gamma)
        
        # Spectral accelerations for each mode
        spectral_accelerations = []
        for T in periods:
            Sa = self._spectral_acceleration_is1893(T)
            spectral_accelerations.append(Sa)
        
        # Modal base shears
        modal_base_shears = []
        for i, (gamma, Sa) in enumerate(zip(participation_factors, spectral_accelerations)):
            phi = eigenvectors[:, i]
            Vbi = gamma * Sa * (phi.T @ mass_matrix @ ones)
            modal_base_shears.append(abs(Vbi))
        
        # SRSS combination
        total_base_shear = np.sqrt(sum(v**2 for v in modal_base_shears))
        
        return {
            "frequencies": frequencies.tolist(),
            "periods": periods.tolist(),
            "participation_factors": participation_factors,
            "spectral_accelerations": spectral_accelerations,
            "modal_base_shears": modal_base_shears,
            "total_base_shear_srss": total_base_shear,
            "damping_ratio": damping_ratio
        }
    
    def story_drift_check(self, story_displacements: List[float], 
                         story_heights: List[float]) -> Dict:
        """Check story drift limits per IS 1893"""
        drifts = []
        drift_ratios = []
        
        for i in range(1, len(story_displacements)):
            drift = story_displacements[i] - story_displacements[i-1]
            height = story_heights[i] - story_heights[i-1]
            drift_ratio = drift / height
            
            drifts.append(drift)
            drift_ratios.append(drift_ratio)
        
        # IS 1893 limit: 0.004 * story height
        limit = 0.004
        
        checks = []
        for i, ratio in enumerate(drift_ratios):
            status = "OK" if ratio <= limit else "FAIL"
            checks.append({
                "story": i + 1,
                "drift": drifts[i],
                "drift_ratio": ratio,
                "limit": limit,
                "status": status
            })
        
        return {
            "checks": checks,
            "max_drift_ratio": max(drift_ratios),
            "limit": limit,
            "overall_status": "OK" if max(drift_ratios) <= limit else "FAIL"
        }
    
    def torsional_irregularity_check(self, max_drift: float, 
                                     avg_drift: float) -> Dict:
        """Check torsional irregularity per IS 1893"""
        ratio = max_drift / avg_drift
        
        # IS 1893: Torsional irregularity if ratio > 1.2
        is_irregular = ratio > 1.2
        
        return {
            "max_drift": max_drift,
            "avg_drift": avg_drift,
            "ratio": ratio,
            "limit": 1.2,
            "is_irregular": is_irregular,
            "status": "IRREGULAR" if is_irregular else "REGULAR"
        }
    
    def soft_story_check(self, story_stiffnesses: List[float]) -> Dict:
        """Check for soft story per IS 1893"""
        checks = []
        
        for i in range(1, len(story_stiffnesses)):
            ratio = story_stiffnesses[i] / story_stiffnesses[i-1]
            
            # Soft story if stiffness < 70% of story above
            is_soft = ratio < 0.70
            
            checks.append({
                "story": i + 1,
                "stiffness": story_stiffnesses[i],
                "ratio_to_above": ratio,
                "limit": 0.70,
                "is_soft_story": is_soft
            })
        
        has_soft_story = any(c["is_soft_story"] for c in checks)
        
        return {
            "checks": checks,
            "has_soft_story": has_soft_story,
            "status": "SOFT STORY DETECTED" if has_soft_story else "OK"
        }
    
    def calculate_time_period(self, height: float, building_type: str = "RC_MRF") -> float:
        """Calculate fundamental time period per IS 1893"""
        h = height  # in meters
        
        if building_type == "RC_MRF":
            # Moment resisting frame
            T = 0.075 * (h ** 0.75)
        elif building_type == "STEEL_MRF":
            T = 0.085 * (h ** 0.75)
        elif building_type == "RC_SHEAR_WALL":
            T = 0.075 * (h ** 0.75)
        else:
            T = 0.09 * (h / np.sqrt(1.0))  # Default formula
        
        return T
    
    def seismic_load_distribution(self, base_shear: float, 
                                  story_weights: List[float],
                                  story_heights: List[float]) -> Dict:
        """Distribute base shear to stories per IS 1893"""
        n = len(story_weights)
        
        # Calculate Wi * hi^2
        Wh2 = [w * h**2 for w, h in zip(story_weights, story_heights)]
        sum_Wh2 = sum(Wh2)
        
        # Story forces
        story_forces = []
        for i in range(n):
            Fi = base_shear * Wh2[i] / sum_Wh2
            story_forces.append(Fi)
        
        # Cumulative shear
        cumulative_shear = []
        for i in range(n):
            shear = sum(story_forces[i:])
            cumulative_shear.append(shear)
        
        # Overturning moment at base
        moments = []
        for i in range(n):
            M = sum(story_forces[j] * story_heights[j] for j in range(i, n))
            moments.append(M)
        
        return {
            "story_forces": story_forces,
            "cumulative_shear": cumulative_shear,
            "overturning_moments": moments,
            "base_shear": base_shear,
            "distribution_method": "IS 1893 - Vertical distribution"
        }
