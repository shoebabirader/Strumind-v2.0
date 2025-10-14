"""
Composite Beam Design Module
Steel-Concrete Composite Beams per various codes
"""
import numpy as np
from typing import Dict, Tuple

class CompositeBeamDesign:
    """Comprehensive composite beam design"""
    
    def __init__(self, code: str = "AISC360"):
        self.code = code
        self.fck = 25  # MPa (concrete)
        self.fy_steel = 250  # MPa (steel beam)
        self.fy_rebar = 415  # MPa (reinforcement)
        self.Es = 200000  # MPa
        self.Ec = 5000 * np.sqrt(self.fck)  # MPa
        
    def design_composite_beam(self, span: float, steel_section: Dict,
                             slab_thickness: float, slab_width: float,
                             loads: Dict, shear_connectors: str = "stud") -> Dict:
        """
        Design steel-concrete composite beam
        
        Args:
            span: Beam span (mm)
            steel_section: Steel section properties
            slab_thickness: Concrete slab thickness (mm)
            slab_width: Effective slab width (mm)
            loads: Load dictionary
            shear_connectors: Type of shear connectors
        """
        # Extract steel section properties
        d_steel = steel_section.get('depth', 500)  # mm
        bf = steel_section.get('width', 200)  # mm
        tf = steel_section.get('flange_thickness', 15)  # mm
        tw = steel_section.get('web_thickness', 10)  # mm
        A_steel = steel_section.get('area', 8000)  # mm²
        I_steel = steel_section.get('Ixx', 200e6)  # mm⁴
        
        # Load calculation
        dead_load = loads.get('dead', 0)  # kN/m
        live_load = loads.get('live', 0)  # kN/m
        
        # Self weight
        slab_weight = slab_thickness * slab_width * 25 / 1e6  # kN/m
        steel_weight = A_steel * 78.5 / 1e6  # kN/m
        
        total_dead = dead_load + slab_weight + steel_weight
        
        # Construction stage (steel beam alone)
        w_construction = 1.2 * total_dead  # Factored
        M_construction = w_construction * (span/1000)**2 / 8  # kNm
        
        # Composite stage (steel + concrete)
        w_composite = 1.2 * total_dead + 1.6 * live_load
        M_composite = w_composite * (span/1000)**2 / 8  # kNm
        
        # Modular ratio
        n = self.Es / self.Ec
        
        # Effective slab width
        b_eff = min(slab_width, span / 4, bf + 16 * slab_thickness)
        
        # Transformed section properties
        # Concrete area transformed to steel
        A_concrete_transformed = b_eff * slab_thickness / n
        
        # Neutral axis location (from top of steel)
        y_na = (A_steel * (slab_thickness + d_steel/2) + 
                A_concrete_transformed * slab_thickness/2) / (A_steel + A_concrete_transformed)
        
        # Moment of inertia of composite section
        I_composite = (I_steel + A_steel * (y_na - slab_thickness - d_steel/2)**2 +
                      b_eff * slab_thickness**3 / (12 * n) + 
                      A_concrete_transformed * (y_na - slab_thickness/2)**2)
        
        # Section modulus
        # Top of slab
        S_top = I_composite / y_na
        # Bottom of steel
        S_bottom = I_composite / (slab_thickness + d_steel - y_na)
        
        # Stress check - Construction stage
        sigma_construction = M_construction * 1e6 / (I_steel / (d_steel/2))  # MPa
        construction_ok = sigma_construction <= 0.66 * self.fy_steel
        
        # Stress check - Composite stage
        # Concrete stress
        sigma_concrete = M_composite * 1e6 / S_top * n  # MPa
        concrete_ok = sigma_concrete <= 0.45 * self.fck
        
        # Steel stress
        sigma_steel = M_composite * 1e6 / S_bottom  # MPa
        steel_ok = sigma_steel <= 0.66 * self.fy_steel
        
        # Shear connector design
        # Horizontal shear force
        V_h = 0.85 * self.fck * b_eff * slab_thickness / 2 / 1000  # kN
        
        if shear_connectors == "stud":
            # Stud connector capacity
            d_stud = 19  # mm
            h_stud = 100  # mm
            
            # Capacity per stud (simplified)
            Q_stud = 0.5 * np.pi * d_stud**2 / 4 * np.sqrt(self.fck * self.Ec) / 1000  # kN
            Q_stud = min(Q_stud, 0.4 * np.pi * d_stud**2 / 4 * 400 / 1000)  # kN
            
            # Number of studs required
            n_studs = int(np.ceil(V_h / Q_stud))
            
            # Spacing
            spacing_studs = (span / 2) / n_studs  # mm
            
            connector_design = {
                "type": "headed_stud",
                "diameter": d_stud,
                "height": h_stud,
                "capacity_per_stud": Q_stud,
                "number_required": n_studs,
                "spacing": spacing_studs,
                "designation": f"{d_stud}mm dia x {h_stud}mm @ {spacing_studs:.0f}mm c/c"
            }
        else:
            connector_design = {"type": "to_be_designed"}
        
        # Deflection check
        # Construction stage
        delta_construction = (5 * w_construction * (span/1000)**4) / (384 * self.Es * I_steel / 1e12)  # m
        delta_construction_mm = delta_construction * 1000
        
        # Composite stage (additional deflection)
        w_additional = 1.0 * live_load  # Unfactored
        delta_additional = (5 * w_additional * (span/1000)**4) / (384 * self.Es * I_composite / 1e12)
        delta_additional_mm = delta_additional * 1000
        
        # Total deflection
        delta_total = delta_construction_mm + delta_additional_mm
        
        # Allowable deflection
        delta_allowable = span / 360  # L/360
        
        deflection_ok = delta_total <= delta_allowable
        
        return {
            "beam_type": "composite_steel_concrete",
            "construction_stage": {
                "moment": M_construction,
                "stress": sigma_construction,
                "allowable_stress": 0.66 * self.fy_steel,
                "utilization": (sigma_construction / (0.66 * self.fy_steel)) * 100,
                "status": "OK" if construction_ok else "FAIL"
            },
            "composite_stage": {
                "moment": M_composite,
                "concrete_stress": sigma_concrete,
                "steel_stress": sigma_steel,
                "concrete_utilization": (sigma_concrete / (0.45 * self.fck)) * 100,
                "steel_utilization": (sigma_steel / (0.66 * self.fy_steel)) * 100,
                "status": "OK" if (concrete_ok and steel_ok) else "FAIL"
            },
            "section_properties": {
                "effective_slab_width": b_eff,
                "neutral_axis_depth": y_na,
                "composite_inertia": I_composite,
                "section_modulus_top": S_top,
                "section_modulus_bottom": S_bottom
            },
            "shear_connectors": connector_design,
            "deflection": {
                "construction_stage": delta_construction_mm,
                "live_load": delta_additional_mm,
                "total": delta_total,
                "allowable": delta_allowable,
                "status": "OK" if deflection_ok else "EXCESSIVE"
            },
            "overall_status": "OK" if (construction_ok and concrete_ok and steel_ok and deflection_ok) else "REDESIGN",
            "code": self.code
        }
    
    def design_composite_column(self, height: float, steel_section: Dict,
                               concrete_dimensions: Dict, axial_load: float,
                               moment: float) -> Dict:
        """
        Design composite column (steel encased in concrete)
        
        Args:
            height: Column height (mm)
            steel_section: Steel section properties
            concrete_dimensions: {'width': mm, 'depth': mm}
            axial_load: Factored axial load (kN)
            moment: Factored moment (kNm)
        """
        # Extract properties
        A_steel = steel_section.get('area', 8000)  # mm²
        I_steel = steel_section.get('Ixx', 200e6)  # mm⁴
        
        b = concrete_dimensions.get('width', 400)  # mm
        h = concrete_dimensions.get('depth', 400)  # mm
        
        # Concrete area
        A_concrete = b * h - A_steel  # mm²
        
        # Transformed area
        n = self.Es / self.Ec
        A_transformed = A_concrete / n + A_steel
        
        # Slenderness check
        r = np.sqrt(I_steel / A_steel)  # Radius of gyration
        slenderness_ratio = height / r
        
        # Axial capacity
        # Squash load
        P_squash = (0.4 * self.fck * A_concrete + self.fy_steel * A_steel) / 1000  # kN
        
        # Reduction factor for slenderness
        if slenderness_ratio < 12:
            reduction_factor = 1.0
        else:
            reduction_factor = 1.0 - 0.008 * (slenderness_ratio - 12)
        
        P_capacity = reduction_factor * P_squash
        
        # Moment capacity (simplified)
        M_capacity = 0.15 * P_capacity * min(b, h) / 1000  # kNm
        
        # Interaction check
        interaction_ratio = (axial_load / P_capacity) + (moment / M_capacity)
        
        interaction_ok = interaction_ratio <= 1.0
        
        # Reinforcement
        # Minimum longitudinal steel
        Ast_min = 0.008 * b * h  # 0.8%
        Ast_provided = max(A_steel, Ast_min)
        
        # Ties/stirrups
        tie_dia = 10  # mm
        tie_spacing = min(b, h, 300)  # mm
        
        return {
            "column_type": "composite_encased",
            "slenderness_ratio": slenderness_ratio,
            "classification": "short" if slenderness_ratio < 12 else "slender",
            "axial_capacity": {
                "applied_load": axial_load,
                "capacity": P_capacity,
                "utilization": (axial_load / P_capacity) * 100
            },
            "moment_capacity": {
                "applied_moment": moment,
                "capacity": M_capacity,
                "utilization": (moment / M_capacity) * 100
            },
            "interaction_check": {
                "ratio": interaction_ratio,
                "status": "OK" if interaction_ok else "FAIL"
            },
            "reinforcement": {
                "longitudinal_steel": Ast_provided,
                "ties": {
                    "diameter": tie_dia,
                    "spacing": tie_spacing,
                    "designation": f"{tie_dia}mm @ {tie_spacing}mm c/c"
                }
            },
            "code": self.code
        }
