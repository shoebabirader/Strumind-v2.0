"""
Temperature Analysis Module
Thermal loads and temperature-induced stresses
"""
import numpy as np
from typing import Dict, List

class TemperatureAnalysis:
    """Temperature load analysis"""
    
    def __init__(self):
        self.alpha_steel = 12e-6  # /°C
        self.alpha_concrete = 10e-6  # /°C
        self.E_steel = 200000  # MPa
        self.E_concrete = 25000  # MPa
        
    def uniform_temperature_load(self, delta_T: float, material: str,
                                 length: float, area: float,
                                 restraint: str = "fixed") -> Dict:
        """
        Calculate effects of uniform temperature change
        
        Args:
            delta_T: Temperature change (°C)
            material: 'steel' or 'concrete'
            length: Member length (mm)
            area: Cross-sectional area (mm²)
            restraint: 'fixed', 'free', 'partial'
        """
        # Thermal expansion coefficient
        alpha = self.alpha_steel if material == "steel" else self.alpha_concrete
        E = self.E_steel if material == "steel" else self.E_concrete
        
        # Free thermal strain
        epsilon_thermal = alpha * delta_T
        
        # Free thermal expansion
        delta_free = epsilon_thermal * length  # mm
        
        if restraint == "free":
            # No stress, only expansion
            stress = 0
            force = 0
            displacement = delta_free
            
        elif restraint == "fixed":
            # Fully restrained - thermal stress develops
            stress = -E * epsilon_thermal  # MPa (negative = compression for heating)
            force = stress * area / 1000  # kN
            displacement = 0
            
        else:  # partial restraint
            # Assume 50% restraint
            restraint_factor = 0.5
            stress = -E * epsilon_thermal * restraint_factor
            force = stress * area / 1000
            displacement = delta_free * (1 - restraint_factor)
        
        return {
            "temperature_change": delta_T,
            "material": material,
            "thermal_coefficient": alpha,
            "free_expansion": delta_free,
            "restraint_condition": restraint,
            "thermal_stress": stress,
            "thermal_force": force,
            "actual_displacement": displacement,
            "thermal_strain": epsilon_thermal
        }
    
    def gradient_temperature_load(self, T_top: float, T_bottom: float,
                                  depth: float, material: str,
                                  length: float, I: float) -> Dict:
        """
        Calculate effects of temperature gradient through depth
        
        Args:
            T_top: Temperature at top fiber (°C)
            T_bottom: Temperature at bottom fiber (°C)
            depth: Section depth (mm)
            material: Material type
            length: Member length (mm)
            I: Moment of inertia (mm⁴)
        """
        alpha = self.alpha_steel if material == "steel" else self.alpha_concrete
        E = self.E_steel if material == "steel" else self.E_concrete
        
        # Average temperature (causes axial effects)
        T_avg = (T_top + T_bottom) / 2
        
        # Temperature gradient (causes bending)
        delta_T = T_top - T_bottom
        
        # Curvature due to temperature gradient
        kappa = alpha * delta_T / depth  # 1/mm
        
        # Thermal moment
        M_thermal = E * I * kappa / 1e6  # kNm
        
        # Deflection (for simply supported beam)
        delta_mid = kappa * length**2 / 8  # mm
        
        # Axial strain
        epsilon_axial = alpha * T_avg
        
        return {
            "temperature_top": T_top,
            "temperature_bottom": T_bottom,
            "average_temperature": T_avg,
            "temperature_gradient": delta_T,
            "thermal_curvature": kappa,
            "thermal_moment": M_thermal,
            "midspan_deflection": delta_mid,
            "axial_strain": epsilon_axial,
            "material": material
        }
    
    def fire_exposure_analysis(self, fire_duration: float, section_type: str,
                               dimensions: Dict, cover: float = 50) -> Dict:
        """
        Simplified fire exposure analysis
        
        Args:
            fire_duration: Fire exposure time (minutes)
            section_type: 'beam', 'column', 'slab'
            dimensions: Section dimensions
            cover: Concrete cover (mm)
        """
        # ISO 834 standard fire curve
        # T = 20 + 345 * log10(8*t + 1)
        # where t is time in minutes
        
        T_fire = 20 + 345 * np.log10(8 * fire_duration + 1)
        
        # Temperature penetration depth (simplified)
        # Concrete thermal diffusivity ~ 0.5 mm²/s
        penetration_depth = np.sqrt(0.5 * fire_duration * 60)  # mm
        
        # Check if reinforcement is affected
        if penetration_depth > cover:
            rebar_affected = True
            T_rebar = T_fire * (1 - cover / penetration_depth)
        else:
            rebar_affected = False
            T_rebar = 20  # Ambient
        
        # Strength reduction factors (simplified)
        # Concrete
        if T_fire < 400:
            k_concrete = 1.0
        elif T_fire < 600:
            k_concrete = 0.75
        elif T_fire < 800:
            k_concrete = 0.45
        else:
            k_concrete = 0.0
        
        # Steel reinforcement
        if T_rebar < 400:
            k_steel = 1.0
        elif T_rebar < 600:
            k_steel = 0.5
        else:
            k_steel = 0.0
        
        # Fire resistance rating
        if fire_duration < 30:
            rating = "R30"
        elif fire_duration < 60:
            rating = "R60"
        elif fire_duration < 90:
            rating = "R90"
        elif fire_duration < 120:
            rating = "R120"
        else:
            rating = "R120+"
        
        return {
            "fire_duration": fire_duration,
            "fire_temperature": T_fire,
            "penetration_depth": penetration_depth,
            "concrete_cover": cover,
            "reinforcement_affected": rebar_affected,
            "reinforcement_temperature": T_rebar,
            "strength_reduction": {
                "concrete": k_concrete,
                "steel": k_steel
            },
            "fire_resistance_rating": rating,
            "status": "ADEQUATE" if not rebar_affected else "CRITICAL"
        }
    
    def seasonal_temperature_effects(self, T_summer: float, T_winter: float,
                                    length: float, material: str,
                                    expansion_joint_spacing: float = None) -> Dict:
        """
        Analyze seasonal temperature effects
        
        Args:
            T_summer: Maximum summer temperature (°C)
            T_winter: Minimum winter temperature (°C)
            length: Structure length (mm)
            material: Material type
            expansion_joint_spacing: Spacing of expansion joints (mm)
        """
        alpha = self.alpha_steel if material == "steel" else self.alpha_concrete
        
        # Temperature range
        delta_T = T_summer - T_winter
        
        # Total expansion/contraction
        delta_L = alpha * delta_T * length  # mm
        
        # If expansion joints provided
        if expansion_joint_spacing:
            n_joints = int(np.ceil(length / expansion_joint_spacing))
            delta_L_per_joint = delta_L / n_joints
            
            # Required joint capacity
            joint_capacity_required = delta_L_per_joint * 1.5  # 50% safety factor
            
            joint_design = {
                "number_of_joints": n_joints,
                "spacing": expansion_joint_spacing,
                "movement_per_joint": delta_L_per_joint,
                "required_capacity": joint_capacity_required
            }
        else:
            joint_design = {
                "recommendation": "Provide expansion joints",
                "suggested_spacing": min(30000, length / 3)  # 30m or L/3
            }
        
        return {
            "temperature_range": delta_T,
            "summer_temperature": T_summer,
            "winter_temperature": T_winter,
            "total_movement": delta_L,
            "material": material,
            "expansion_coefficient": alpha,
            "expansion_joints": joint_design
        }
