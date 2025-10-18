"""
Serviceability Checks Module
Deflection, Crack Width, Vibration, Fatigue Checks
"""
import numpy as np
from typing import Dict, Tuple

class ServiceabilityChecks:
    """Comprehensive serviceability checks"""
    
    def __init__(self, code: str = "IS456"):
        self.code = code
        self.fck = 25  # MPa
        self.fy = 415  # MPa
        self.Es = 200000  # MPa
        self.Ec = 5000 * np.sqrt(self.fck)  # MPa
        
    def deflection_check(self, span: float, actual_deflection: float,
                        member_type: str = "beam", support_condition: str = "simply_supported",
                        loading_type: str = "live") -> Dict:
        """
        Check deflection limits per code
        
        Args:
            span: Member span (mm)
            actual_deflection: Calculated deflection (mm)
            member_type: 'beam', 'slab', 'cantilever'
            support_condition: Support conditions
            loading_type: 'live', 'total', 'dead'
        """
        # Deflection limits per IS 456
        if member_type == "cantilever":
            if loading_type == "live":
                limit_ratio = 180  # L/180
            else:
                limit_ratio = 90  # L/90
        else:  # beam or slab
            if loading_type == "live":
                limit_ratio = 360  # L/360
            else:
                limit_ratio = 250  # L/250
        
        # Validate inputs to prevent division by zero
        if limit_ratio <= 0:
            raise ValueError(f"Limit ratio must be positive. Got limit_ratio={limit_ratio}")
        
        # Calculate allowable deflection
        allowable_deflection = span / limit_ratio
        
        # Check status
        utilization = (actual_deflection / allowable_deflection) * 100
        status = "OK" if actual_deflection <= allowable_deflection else "FAIL"
        
        # Additional limits
        limits = {
            'L/180': span / 180,
            'L/250': span / 250,
            'L/300': span / 300,
            'L/360': span / 360,
            'L/500': span / 500
        }
        
        checks = {limit: actual_deflection <= value for limit, value in limits.items()}
        
        return {
            "check_type": "deflection",
            "member_type": member_type,
            "span": span,
            "actual_deflection": actual_deflection,
            "allowable_deflection": allowable_deflection,
            "limit_ratio": f"L/{limit_ratio}",
            "utilization": utilization,
            "status": status,
            "additional_limits": limits,
            "additional_checks": checks,
            "code": self.code
        }
    
    def crack_width_check(self, stress_steel: float, cover: float,
                         bar_diameter: float, spacing: float,
                         exposure_condition: str = "moderate") -> Dict:
        """
        Check crack width per code
        
        Args:
            stress_steel: Steel stress under service loads (MPa)
            cover: Concrete cover (mm)
            bar_diameter: Bar diameter (mm)
            spacing: Bar spacing (mm)
            exposure_condition: 'mild', 'moderate', 'severe', 'very_severe'
        """
        # Allowable crack width per IS 456
        crack_width_limits = {
            'mild': 0.3,  # mm
            'moderate': 0.3,
            'severe': 0.2,
            'very_severe': 0.2
        }
        
        allowable_crack_width = crack_width_limits.get(exposure_condition, 0.3)
        
        # Calculate crack width (simplified Gergely-Lutz equation)
        acr = np.sqrt(cover**2 + (spacing/2)**2)  # Distance from bar to tension face
        
        # Crack width
        w = (3 * stress_steel * acr) / (self.Es * 1000)  # mm
        
        # Check status
        utilization = (w / allowable_crack_width) * 100
        status = "OK" if w <= allowable_crack_width else "FAIL"
        
        # Recommendations
        recommendations = []
        if w > allowable_crack_width:
            recommendations.append("Reduce bar spacing")
            recommendations.append("Increase concrete cover")
            recommendations.append("Use smaller diameter bars with closer spacing")
        
        return {
            "check_type": "crack_width",
            "exposure_condition": exposure_condition,
            "steel_stress": stress_steel,
            "cover": cover,
            "bar_diameter": bar_diameter,
            "spacing": spacing,
            "calculated_crack_width": w,
            "allowable_crack_width": allowable_crack_width,
            "utilization": utilization,
            "status": status,
            "recommendations": recommendations,
            "code": self.code
        }
    
    def vibration_check(self, natural_frequency: float, floor_type: str = "office",
                       damping_ratio: float = 0.05) -> Dict:
        """
        Check vibration limits for floors
        
        Args:
            natural_frequency: Natural frequency (Hz)
            floor_type: 'office', 'residential', 'hospital', 'laboratory'
            damping_ratio: Damping ratio
        """
        # Minimum frequency requirements
        frequency_limits = {
            'office': 3.0,  # Hz
            'residential': 4.0,
            'hospital': 5.0,
            'laboratory': 8.0,
            'dance_hall': 6.0
        }
        
        min_frequency = frequency_limits.get(floor_type, 3.0)
        
        # Check frequency
        frequency_ok = natural_frequency >= min_frequency
        
        # Peak acceleration limit (% of g)
        # Per ISO 2631 for human comfort
        if floor_type in ['hospital', 'laboratory']:
            max_acceleration = 0.5  # % g
        elif floor_type == 'residential':
            max_acceleration = 1.5  # % g
        else:  # office
            max_acceleration = 2.0  # % g
        
        # Estimate peak acceleration (simplified)
        # a = (2*pi*f)^2 * delta
        # Assuming delta = 1mm for walking
        delta = 1.0  # mm
        peak_acceleration = (2 * np.pi * natural_frequency)**2 * delta / 9810  # % g
        
        acceleration_ok = peak_acceleration <= max_acceleration
        
        # Overall status
        status = "OK" if (frequency_ok and acceleration_ok) else "FAIL"
        
        # Recommendations
        recommendations = []
        if not frequency_ok:
            recommendations.append(f"Increase stiffness to achieve minimum frequency of {min_frequency} Hz")
        if not acceleration_ok:
            recommendations.append("Reduce floor flexibility or add damping")
        
        return {
            "check_type": "vibration",
            "floor_type": floor_type,
            "natural_frequency": natural_frequency,
            "minimum_frequency": min_frequency,
            "frequency_check": "OK" if frequency_ok else "FAIL",
            "peak_acceleration": peak_acceleration,
            "max_acceleration": max_acceleration,
            "acceleration_check": "OK" if acceleration_ok else "FAIL",
            "damping_ratio": damping_ratio,
            "status": status,
            "recommendations": recommendations
        }
    
    def punching_shear_check(self, column_size: float, slab_thickness: float,
                            column_load: float, fck: float = None) -> Dict:
        """
        Check punching shear for flat slabs
        
        Args:
            column_size: Column size (mm) - assuming square
            slab_thickness: Slab thickness (mm)
            column_load: Factored column load (kN)
            fck: Concrete strength (MPa)
        """
        if fck is None:
            fck = self.fck
        
        # Effective depth
        cover = 25
        bar_dia = 12
        d = slab_thickness - cover - bar_dia/2
        
        # Critical perimeter (at d/2 from column face)
        bo = 4 * (column_size + d)  # mm
        
        # Punching shear stress
        vu = (column_load * 1000) / (bo * d)  # MPa
        
        # Allowable punching shear stress (IS 456)
        ks = 0.5 + column_size / column_size  # For square column = 1.0
        ks = min(ks, 1.0)
        
        tau_c = 0.25 * np.sqrt(fck)  # Simplified
        vu_max = ks * tau_c
        
        # Check status
        utilization = (vu / vu_max) * 100
        status = "OK" if vu <= vu_max else "FAIL"
        
        # Shear reinforcement requirement
        if vu > tau_c:
            shear_reinforcement_required = True
            # Calculate required shear reinforcement
            Vus = (vu - tau_c) * bo * d / 1000  # kN
        else:
            shear_reinforcement_required = False
            Vus = 0
        
        # Recommendations
        recommendations = []
        if status == "FAIL":
            recommendations.append("Increase slab thickness")
            recommendations.append("Provide drop panel or column capital")
            recommendations.append("Provide shear reinforcement (studs/stirrups)")
        
        return {
            "check_type": "punching_shear",
            "column_size": column_size,
            "slab_thickness": slab_thickness,
            "effective_depth": d,
            "critical_perimeter": bo,
            "column_load": column_load,
            "applied_stress": vu,
            "allowable_stress": vu_max,
            "utilization": utilization,
            "status": status,
            "shear_reinforcement_required": shear_reinforcement_required,
            "shear_to_be_resisted": Vus,
            "recommendations": recommendations,
            "code": self.code
        }
    
    def fatigue_check(self, stress_range: float, n_cycles: float,
                     material: str = "steel", detail_category: str = "C") -> Dict:
        """
        Check fatigue for steel structures
        
        Args:
            stress_range: Stress range (MPa)
            n_cycles: Number of cycles
            material: 'steel' or 'concrete'
            detail_category: 'A', 'B', 'C', 'D', 'E', 'F' (for steel)
        """
        if material == "steel":
            # Fatigue strength per detail category (at 2 million cycles)
            fatigue_strength = {
                'A': 160,  # MPa
                'B': 125,
                'C': 100,
                'D': 80,
                'E': 71,
                'F': 50
            }
            
            delta_sigma_c = fatigue_strength.get(detail_category, 100)
            
            # Constant amplitude fatigue limit (CAFL)
            # For N > 5 million cycles
            cafl = 0.74 * delta_sigma_c
            
            # Variable amplitude fatigue limit (VAFL)
            # For N > 100 million cycles
            vafl = 0.49 * delta_sigma_c
            
            # Check based on number of cycles
            if n_cycles <= 2e6:
                allowable_stress_range = delta_sigma_c
                limit_type = "Detail Category Limit"
            elif n_cycles <= 5e6:
                # Interpolate
                allowable_stress_range = delta_sigma_c * (2e6 / n_cycles) ** (1/3)
                limit_type = "Finite Life"
            else:
                allowable_stress_range = cafl
                limit_type = "CAFL"
            
            # Check status
            utilization = (stress_range / allowable_stress_range) * 100
            status = "OK" if stress_range <= allowable_stress_range else "FAIL"
            
            # Life estimation
            if stress_range > 0:
                estimated_life = 2e6 * (delta_sigma_c / stress_range) ** 3
            else:
                estimated_life = float('inf')
            
            return {
                "check_type": "fatigue",
                "material": material,
                "detail_category": detail_category,
                "stress_range": stress_range,
                "number_of_cycles": n_cycles,
                "allowable_stress_range": allowable_stress_range,
                "limit_type": limit_type,
                "utilization": utilization,
                "status": status,
                "estimated_life_cycles": estimated_life,
                "CAFL": cafl,
                "VAFL": vafl
            }
        
        else:  # concrete
            # Simplified fatigue check for concrete
            # Based on stress ratio
            max_stress = stress_range  # Assuming this is the maximum stress
            
            # Allowable stress for fatigue (typically 0.5 * fck for high cycle)
            allowable_stress = 0.5 * self.fck
            
            status = "OK" if max_stress <= allowable_stress else "FAIL"
            
            return {
                "check_type": "fatigue",
                "material": material,
                "stress_range": stress_range,
                "number_of_cycles": n_cycles,
                "allowable_stress": allowable_stress,
                "status": status
            }
    
    def slenderness_check(self, length: float, radius_of_gyration: float,
                         member_type: str = "column", end_conditions: str = "pinned_pinned") -> Dict:
        """
        Check slenderness ratio
        
        Args:
            length: Member length (mm)
            radius_of_gyration: Radius of gyration (mm)
            member_type: 'column', 'strut', 'tie'
            end_conditions: 'fixed_fixed', 'fixed_pinned', 'pinned_pinned', 'fixed_free'
        """
        # Effective length factors
        k_factors = {
            'fixed_fixed': 0.5,
            'fixed_pinned': 0.7,
            'pinned_pinned': 1.0,
            'fixed_free': 2.0
        }
        
        k = k_factors.get(end_conditions, 1.0)
        
        # Effective length
        L_eff = k * length
        
        # Slenderness ratio
        slenderness_ratio = L_eff / radius_of_gyration
        
        # Limits per IS 456
        if member_type == "column":
            max_slenderness = 60  # For braced columns
        elif member_type == "strut":
            max_slenderness = 180
        else:  # tie
            max_slenderness = 400
        
        # Classification
        if slenderness_ratio < 12:
            classification = "short"
        elif slenderness_ratio < max_slenderness:
            classification = "slender"
        else:
            classification = "very_slender"
        
        # Check status
        status = "OK" if slenderness_ratio <= max_slenderness else "FAIL"
        
        return {
            "check_type": "slenderness",
            "member_type": member_type,
            "length": length,
            "effective_length": L_eff,
            "radius_of_gyration": radius_of_gyration,
            "slenderness_ratio": slenderness_ratio,
            "max_slenderness": max_slenderness,
            "classification": classification,
            "end_conditions": end_conditions,
            "effective_length_factor": k,
            "status": status,
            "code": self.code
        }
