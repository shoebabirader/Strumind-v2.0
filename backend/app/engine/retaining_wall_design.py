"""
Retaining Wall Design Module
Gravity, Cantilever, Counterfort Retaining Walls
"""
import numpy as np
from typing import Dict, Tuple

class RetainingWallDesign:
    """Comprehensive retaining wall design"""
    
    def __init__(self, code: str = "IS456"):
        self.code = code
        self.fck = 25  # MPa
        self.fy = 415  # MPa
        self.gamma_soil = 18  # kN/m³
        self.phi = 30  # Angle of internal friction (degrees)
        
    def cantilever_retaining_wall(self, height: float, stem_thickness_top: float,
                                  stem_thickness_bottom: float, base_width: float,
                                  base_thickness: float, toe_length: float,
                                  surcharge: float = 0) -> Dict:
        """
        Design cantilever retaining wall
        
        Args:
            height: Wall height above base (mm)
            stem_thickness_top: Stem thickness at top (mm)
            stem_thickness_bottom: Stem thickness at bottom (mm)
            base_width: Total base width (mm)
            base_thickness: Base slab thickness (mm)
            toe_length: Toe projection (mm)
            surcharge: Surcharge load (kN/m²)
        """
        # Convert to meters for calculations
        H = height / 1000
        B = base_width / 1000
        t_base = base_thickness / 1000
        L_toe = toe_length / 1000
        L_heel = B - L_toe - stem_thickness_bottom / 1000
        
        # Active earth pressure coefficient
        Ka = (1 - np.sin(np.radians(self.phi))) / (1 + np.sin(np.radians(self.phi)))
        
        # Earth pressure
        Pa = 0.5 * Ka * self.gamma_soil * H**2  # kN/m
        
        # Surcharge pressure
        if surcharge > 0:
            Pa_surcharge = Ka * surcharge * H
            Pa_total = Pa + Pa_surcharge
            h_resultant = (Pa * H/3 + Pa_surcharge * H/2) / Pa_total
        else:
            Pa_total = Pa
            h_resultant = H / 3
        
        # Overturning moment about toe
        Mo = Pa_total * h_resultant  # kNm/m
        
        # Resisting forces and moments
        # Stem weight
        stem_avg_thickness = (stem_thickness_top + stem_thickness_bottom) / 2000  # m
        W_stem = 25 * stem_avg_thickness * H  # kN/m
        x_stem = L_toe + stem_thickness_bottom / 2000
        
        # Base weight
        W_base = 25 * B * t_base  # kN/m
        x_base = B / 2
        
        # Soil on heel
        W_soil = self.gamma_soil * L_heel * H  # kN/m
        x_soil = L_toe + stem_thickness_bottom / 1000 + L_heel / 2
        
        # Total vertical load
        W_total = W_stem + W_base + W_soil
        
        # Resisting moment
        Mr = W_stem * x_stem + W_base * x_base + W_soil * x_soil
        
        # Factor of safety against overturning
        FOS_overturning = Mr / Mo
        
        # Sliding check
        # Friction coefficient
        mu = np.tan(np.radians(self.phi * 2/3))  # Reduced friction angle
        Fr = mu * W_total  # Resisting force
        
        FOS_sliding = Fr / Pa_total
        
        # Base pressure
        e = B / 2 - (Mr - Mo) / W_total  # Eccentricity
        
        if e < B / 6:
            # No tension
            q_max = (W_total / B) * (1 + 6 * e / B)
            q_min = (W_total / B) * (1 - 6 * e / B)
            base_pressure_ok = q_min >= 0
        else:
            # Tension exists
            base_pressure_ok = False
            q_max = 2 * W_total / (3 * (B/2 - e))
            q_min = 0
        
        # Bearing capacity check (assumed)
        q_safe = 200  # kN/m² (assumed)
        bearing_ok = q_max <= q_safe
        
        # Stem design
        # Maximum moment at base
        M_stem = 0.5 * Ka * self.gamma_soil * H**3 / 3  # kNm/m
        
        # Factored moment
        Mu_stem = 1.5 * M_stem
        
        # Effective depth
        cover = 50
        bar_dia = 16
        d_stem = stem_thickness_bottom - cover - bar_dia/2
        
        # Required steel
        Ast_stem = (Mu_stem * 1e6) / (0.87 * self.fy * 0.9 * d_stem)
        Ast_min = 0.12 * 1000 * stem_thickness_bottom / 100
        Ast_stem = max(Ast_stem, Ast_min)
        
        bar_area = np.pi * bar_dia**2 / 4
        spacing_stem = bar_area * 1000 / Ast_stem
        spacing_stem = min(spacing_stem, 3 * stem_thickness_bottom, 300)
        
        # Base slab design
        # Toe design
        M_toe = q_max * L_toe**2 / 2  # kNm/m
        Mu_toe = 1.5 * M_toe
        
        d_base = base_thickness - cover - bar_dia/2
        Ast_toe = (Mu_toe * 1e6) / (0.87 * self.fy * 0.9 * d_base)
        Ast_min_base = 0.12 * 1000 * base_thickness / 100
        Ast_toe = max(Ast_toe, Ast_min_base)
        
        spacing_toe = bar_area * 1000 / Ast_toe
        spacing_toe = min(spacing_toe, 3 * base_thickness, 300)
        
        # Heel design
        # Net upward pressure
        q_heel = q_min + self.gamma_soil * H / 1000
        M_heel = q_heel * L_heel**2 / 2  # kNm/m
        Mu_heel = 1.5 * M_heel
        
        Ast_heel = (Mu_heel * 1e6) / (0.87 * self.fy * 0.9 * d_base)
        Ast_heel = max(Ast_heel, Ast_min_base)
        
        spacing_heel = bar_area * 1000 / Ast_heel
        spacing_heel = min(spacing_heel, 3 * base_thickness, 300)
        
        # Overall status
        overall_ok = (FOS_overturning >= 2.0 and FOS_sliding >= 1.5 and 
                     base_pressure_ok and bearing_ok)
        
        return {
            "wall_type": "cantilever_retaining_wall",
            "stability": {
                "overturning": {
                    "resisting_moment": Mr,
                    "overturning_moment": Mo,
                    "FOS": FOS_overturning,
                    "required_FOS": 2.0,
                    "status": "OK" if FOS_overturning >= 2.0 else "FAIL"
                },
                "sliding": {
                    "resisting_force": Fr,
                    "driving_force": Pa_total,
                    "FOS": FOS_sliding,
                    "required_FOS": 1.5,
                    "status": "OK" if FOS_sliding >= 1.5 else "FAIL"
                },
                "base_pressure": {
                    "q_max": q_max,
                    "q_min": q_min,
                    "eccentricity": e,
                    "allowable_eccentricity": B / 6,
                    "status": "OK" if base_pressure_ok else "TENSION_EXISTS"
                },
                "bearing_capacity": {
                    "applied_pressure": q_max,
                    "safe_bearing_capacity": q_safe,
                    "status": "OK" if bearing_ok else "FAIL"
                }
            },
            "stem_design": {
                "design_moment": Mu_stem,
                "Ast_required": Ast_stem,
                "bar_diameter": bar_dia,
                "spacing": spacing_stem,
                "designation": f"{bar_dia}mm @ {spacing_stem:.0f}mm c/c",
                "face": "earth face (tension)"
            },
            "base_design": {
                "toe": {
                    "design_moment": Mu_toe,
                    "Ast_required": Ast_toe,
                    "spacing": spacing_toe,
                    "designation": f"{bar_dia}mm @ {spacing_toe:.0f}mm c/c",
                    "face": "bottom (tension)"
                },
                "heel": {
                    "design_moment": Mu_heel,
                    "Ast_required": Ast_heel,
                    "spacing": spacing_heel,
                    "designation": f"{bar_dia}mm @ {spacing_heel:.0f}mm c/c",
                    "face": "top (tension)"
                }
            },
            "overall_status": "OK" if overall_ok else "REDESIGN_REQUIRED",
            "code": self.code
        }
    
    def gravity_retaining_wall(self, height: float, top_width: float,
                               bottom_width: float, surcharge: float = 0) -> Dict:
        """
        Design gravity retaining wall (masonry/concrete)
        
        Args:
            height: Wall height (mm)
            top_width: Width at top (mm)
            bottom_width: Width at bottom (mm)
            surcharge: Surcharge load (kN/m²)
        """
        H = height / 1000
        B = bottom_width / 1000
        
        # Active earth pressure
        Ka = (1 - np.sin(np.radians(self.phi))) / (1 + np.sin(np.radians(self.phi)))
        Pa = 0.5 * Ka * self.gamma_soil * H**2
        
        # Wall weight (trapezoidal)
        avg_width = (top_width + bottom_width) / 2000
        W = 25 * avg_width * H  # Assuming concrete
        
        # Overturning moment
        Mo = Pa * H / 3
        
        # Resisting moment (about toe)
        Mr = W * B / 2
        
        FOS_overturning = Mr / Mo
        
        # Sliding
        mu = 0.5  # For masonry/concrete on soil
        Fr = mu * W
        FOS_sliding = Fr / Pa
        
        return {
            "wall_type": "gravity_retaining_wall",
            "FOS_overturning": FOS_overturning,
            "FOS_sliding": FOS_sliding,
            "status": "OK" if (FOS_overturning >= 2.0 and FOS_sliding >= 1.5) else "FAIL",
            "code": self.code
        }
