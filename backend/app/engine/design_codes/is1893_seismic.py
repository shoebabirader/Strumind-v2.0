"""
IS 1893:2016 - Indian Standard for Seismic Design
Complete implementation of seismic analysis and design
"""
import math
from typing import Dict, List, Tuple, Optional
from enum import Enum
import numpy as np


class SeismicZone(str, Enum):
    """Seismic zones per IS 1893"""
    ZONE_II = "II"
    ZONE_III = "III"
    ZONE_IV = "IV"
    ZONE_V = "V"


class SoilType(str, Enum):
    """Soil types per IS 1893 Table 3"""
    TYPE_I = "I"  # Rock or hard soil
    TYPE_II = "II"  # Medium soil
    TYPE_III = "III"  # Soft soil


class ImportanceFactor(str, Enum):
    """Importance factors per IS 1893 Table 8"""
    ORDINARY = "ordinary"  # I = 1.0
    IMPORTANT = "important"  # I = 1.2
    CRITICAL = "critical"  # I = 1.5


class IS1893SeismicDesign:
    """IS 1893:2016 Seismic Design Implementation"""
    
    # Zone factors (Table 3)
    ZONE_FACTORS = {
        SeismicZone.ZONE_II: 0.10,
        SeismicZone.ZONE_III: 0.16,
        SeismicZone.ZONE_IV: 0.24,
        SeismicZone.ZONE_V: 0.36,
    }
    
    # Importance factors (Table 8)
    IMPORTANCE_FACTORS = {
        ImportanceFactor.ORDINARY: 1.0,
        ImportanceFactor.IMPORTANT: 1.2,
        ImportanceFactor.CRITICAL: 1.5,
    }
    
    # Response reduction factors (Table 9)
    RESPONSE_REDUCTION_FACTORS = {
        'OMRF': 3.0,  # Ordinary moment resisting frame
        'SMRF': 5.0,  # Special moment resisting frame
        'OMRF_SW': 4.0,  # OMRF with shear walls
        'SMRF_SW': 5.0,  # SMRF with shear walls
        'Braced': 4.0,  # Braced frame
        'Shear_wall': 4.0,  # Shear wall
    }
    
    def __init__(self, zone: SeismicZone, soil_type: SoilType, 
                 importance: ImportanceFactor = ImportanceFactor.ORDINARY):
        """
        Initialize seismic design parameters
        
        Args:
            zone: Seismic zone
            soil_type: Soil type
            importance: Importance factor
        """
        self.zone = zone
        self.soil_type = soil_type
        self.importance = importance
        
        self.Z = self.ZONE_FACTORS[zone]
        self.I = self.IMPORTANCE_FACTORS[importance]
    
    def design_spectrum(self, damping: float = 0.05) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate design response spectrum per IS 1893 Clause 6.4
        
        Args:
            damping: Damping ratio (default 5%)
        
        Returns:
            (periods, spectral_accelerations)
        """
        # Spectral acceleration coefficient (Sa/g)
        if self.soil_type == SoilType.TYPE_I:
            # Rock or hard soil
            T_corners = [0.0, 0.10, 0.40, 4.0]
            Sa_g_values = [1.0, 2.5, 2.5, 1.0]
        elif self.soil_type == SoilType.TYPE_II:
            # Medium soil
            T_corners = [0.0, 0.10, 0.55, 4.0]
            Sa_g_values = [1.0, 2.5, 2.5, 1.36]
        else:  # TYPE_III
            # Soft soil
            T_corners = [0.0, 0.10, 0.67, 4.0]
            Sa_g_values = [1.0, 2.5, 2.5, 1.67]
        
        # Generate spectrum
        T = np.linspace(0, 4, 200)
        Sa_g = np.zeros_like(T)
        
        for i, t in enumerate(T):
            if t <= T_corners[1]:
                # Ascending branch
                Sa_g[i] = Sa_g_values[0] + (Sa_g_values[1] - Sa_g_values[0]) * t / T_corners[1]
            elif t <= T_corners[2]:
                # Plateau
                Sa_g[i] = Sa_g_values[2]
            else:
                # Descending branch
                Sa_g[i] = Sa_g_values[2] * T_corners[2] / t
        
        # Apply damping correction if not 5%
        if damping != 0.05:
            damping_factor = math.sqrt(0.05 / damping)
            Sa_g = Sa_g * damping_factor
        
        return T, Sa_g
    
    def base_shear(self, W: float, T: float, R: float = 5.0) -> Dict:
        """
        Calculate design base shear per IS 1893 Clause 7.5
        
        V_B = Ah * W
        where Ah = (Z/2) * (I/R) * (Sa/g)
        
        Args:
            W: Seismic weight (kN)
            T: Fundamental period (seconds)
            R: Response reduction factor
        
        Returns:
            Dict with base shear and parameters
        """
        # Get spectral acceleration
        T_array, Sa_g_array = self.design_spectrum()
        
        # Interpolate Sa/g for given period
        Sa_g = np.interp(T, T_array, Sa_g_array)
        
        # Design horizontal acceleration spectrum (Clause 6.4.2)
        Ah = (self.Z / 2) * (self.I / R) * Sa_g
        
        # Base shear
        V_B = Ah * W
        
        return {
            'V_B': round(V_B, 2),
            'Ah': round(Ah, 4),
            'Z': self.Z,
            'I': self.I,
            'R': R,
            'Sa_g': round(Sa_g, 3),
            'T': T,
            'W': W
        }
    
    def fundamental_period(self, h: float, building_type: str = 'RC_MRF') -> float:
        """
        Calculate fundamental period per IS 1893 Clause 7.6
        
        Args:
            h: Height of building (m)
            building_type: Type of building
        
        Returns:
            Fundamental period (seconds)
        """
        # Empirical period formulas (Table 7)
        if building_type == 'RC_MRF':
            # RC moment resisting frame without brick infill
            Ta = 0.075 * h**0.75
        elif building_type == 'RC_MRF_infill':
            # RC moment resisting frame with brick infill
            Ta = 0.09 * h / math.sqrt(d) if 'd' in locals() else 0.09 * h / math.sqrt(h)
        elif building_type == 'Steel_MRF':
            # Steel moment resisting frame without brick infill
            Ta = 0.085 * h**0.75
        elif building_type == 'Shear_wall':
            # All other buildings including shear walls
            Ta = 0.09 * h / math.sqrt(d) if 'd' in locals() else 0.075 * h**0.75
        else:
            # Default
            Ta = 0.075 * h**0.75
        
        return round(Ta, 3)
    
    def story_drift_check(self, delta_i: float, h_i: float, 
                         building_type: str = 'RC') -> Dict:
        """
        Check story drift per IS 1893 Clause 7.11.1
        
        Args:
            delta_i: Story drift (m)
            h_i: Story height (m)
            building_type: Building type (RC, Steel, Masonry)
        
        Returns:
            Dict with drift check results
        """
        # Drift limits (Table 11)
        if building_type == 'RC':
            drift_limit = 0.004 * h_i
        elif building_type == 'Steel':
            drift_limit = 0.004 * h_i
        elif building_type == 'Masonry':
            drift_limit = 0.002 * h_i
        else:
            drift_limit = 0.004 * h_i
        
        drift_ratio = delta_i / h_i
        drift_ok = delta_i <= drift_limit
        
        return {
            'delta_i': round(delta_i * 1000, 2),  # mm
            'h_i': round(h_i * 1000, 0),  # mm
            'drift_ratio': round(drift_ratio, 5),
            'drift_limit': round(drift_limit * 1000, 2),  # mm
            'drift_ok': drift_ok,
            'message': 'OK' if drift_ok else f'Drift exceeds limit ({drift_limit*1000:.2f} mm)'
        }
    
    def torsional_provision(self, eccentricity: float, 
                           building_dimension: float) -> Dict:
        """
        Calculate design eccentricity per IS 1893 Clause 7.9
        
        Accidental eccentricity = ±0.05 * dimension
        
        Args:
            eccentricity: Calculated eccentricity (m)
            building_dimension: Building dimension perpendicular to earthquake (m)
        
        Returns:
            Dict with design eccentricity
        """
        # Accidental eccentricity
        e_acc = 0.05 * building_dimension
        
        # Design eccentricity (add accidental to calculated)
        e_design_plus = eccentricity + e_acc
        e_design_minus = eccentricity - e_acc
        
        return {
            'e_calculated': round(eccentricity, 3),
            'e_accidental': round(e_acc, 3),
            'e_design_plus': round(e_design_plus, 3),
            'e_design_minus': round(e_design_minus, 3),
            'building_dimension': building_dimension
        }
    
    def vertical_distribution_of_base_shear(self, V_B: float, 
                                           story_weights: List[float],
                                           story_heights: List[float]) -> Dict:
        """
        Distribute base shear to stories per IS 1893 Clause 7.7.1
        
        Q_i = V_B * (W_i * h_i^2) / Σ(W_j * h_j^2)
        
        Args:
            V_B: Base shear (kN)
            story_weights: List of story weights (kN)
            story_heights: List of story heights from base (m)
        
        Returns:
            Dict with story forces
        """
        n_stories = len(story_weights)
        
        # Calculate Σ(W_i * h_i^2)
        sum_Wh2 = sum(W * h**2 for W, h in zip(story_weights, story_heights))
        
        # Calculate story forces
        story_forces = []
        for i in range(n_stories):
            Q_i = V_B * (story_weights[i] * story_heights[i]**2) / sum_Wh2
            story_forces.append(round(Q_i, 2))
        
        return {
            'V_B': V_B,
            'story_forces': story_forces,
            'story_weights': story_weights,
            'story_heights': story_heights,
            'sum_Wh2': round(sum_Wh2, 2)
        }
    
    def soft_story_check(self, story_stiffnesses: List[float]) -> Dict:
        """
        Check for soft story per IS 1893 Clause 7.10.3
        
        A soft story is one where lateral stiffness is less than 70% of that
        in the story above or less than 80% of average stiffness of three stories above
        
        Args:
            story_stiffnesses: List of story stiffnesses (kN/m)
        
        Returns:
            Dict with soft story check results
        """
        n_stories = len(story_stiffnesses)
        soft_stories = []
        
        for i in range(n_stories - 1):
            k_i = story_stiffnesses[i]
            k_above = story_stiffnesses[i + 1]
            
            # Check 1: Less than 70% of story above
            if k_i < 0.70 * k_above:
                soft_stories.append({
                    'story': i + 1,
                    'stiffness': k_i,
                    'ratio': k_i / k_above,
                    'criterion': '< 0.70 of story above'
                })
            
            # Check 2: Less than 80% of average of three stories above
            if i + 3 < n_stories:
                k_avg_above = sum(story_stiffnesses[i+1:i+4]) / 3
                if k_i < 0.80 * k_avg_above:
                    soft_stories.append({
                        'story': i + 1,
                        'stiffness': k_i,
                        'ratio': k_i / k_avg_above,
                        'criterion': '< 0.80 of average of 3 stories above'
                    })
        
        has_soft_story = len(soft_stories) > 0
        
        return {
            'has_soft_story': has_soft_story,
            'soft_stories': soft_stories,
            'message': 'Soft story detected!' if has_soft_story else 'No soft story'
        }
    
    def torsional_irregularity_check(self, max_drift: float, avg_drift: float) -> Dict:
        """
        Check torsional irregularity per IS 1893 Clause 7.1
        
        Torsional irregularity exists when max drift > 1.2 * avg drift
        
        Args:
            max_drift: Maximum story drift (m)
            avg_drift: Average story drift (m)
        
        Returns:
            Dict with torsional irregularity check
        """
        ratio = max_drift / avg_drift if avg_drift > 0 else 0
        is_irregular = ratio > 1.2
        
        return {
            'max_drift': round(max_drift * 1000, 2),  # mm
            'avg_drift': round(avg_drift * 1000, 2),  # mm
            'ratio': round(ratio, 3),
            'is_irregular': is_irregular,
            'limit': 1.2,
            'message': 'Torsionally irregular!' if is_irregular else 'OK'
        }


# Helper functions
def quick_base_shear(W: float, h: float, zone: str = "III", 
                    soil_type: str = "II", R: float = 5.0) -> Dict:
    """Quick base shear calculation"""
    designer = IS1893SeismicDesign(
        SeismicZone(zone),
        SoilType(soil_type)
    )
    T = designer.fundamental_period(h)
    return designer.base_shear(W, T, R)


def quick_drift_check(delta_i: float, h_i: float, 
                     building_type: str = "RC") -> Dict:
    """Quick drift check"""
    designer = IS1893SeismicDesign(
        SeismicZone.ZONE_III,
        SoilType.TYPE_II
    )
    return designer.story_drift_check(delta_i, h_i, building_type)
