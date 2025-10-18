"""
Shear Wall Design Module
RC Shear Wall Design per various codes
"""
import numpy as np
from typing import Dict, List, Tuple

class ShearWallDesign:
    """Comprehensive shear wall design"""
    
    def __init__(self, code: str = "IS456"):
        self.code = code
        self.fck = 25  # MPa
        self.fy = 415  # MPa
        self.gamma_c = 1.5
        self.gamma_s = 1.15
        
    def design_shear_wall(self, height: float, length: float, thickness: float,
                         axial_load: float, shear_force: float, moment: float,
                         boundary_element: bool = True) -> Dict:
        """
        Design RC shear wall
        
        Args:
            height: Wall height (mm)
            length: Wall length (mm)
            thickness: Wall thickness (mm)
            axial_load: Factored axial load (kN)
            shear_force: Factored shear force (kN)
            moment: Factored moment (kNm)
            boundary_element: Include boundary elements
        """
        # Validate inputs to prevent division by zero
        if thickness <= 0:
            raise ValueError(f"Wall thickness must be positive. Got thickness={thickness}")
        
        # Slenderness check
        slenderness_ratio = height / thickness
        
        # Effective length factor
        if slenderness_ratio < 12:
            k = 1.0  # Short wall
        else:
            k = 1.2  # Slender wall
        
        # Axial capacity check
        Ag = length * thickness  # mm²
        P_max = 0.4 * self.fck * Ag / 1000  # kN
        
        axial_check = axial_load <= P_max
        
        # Flexural design
        d = length - 50  # Effective depth
        Mu = moment * 1e6  # Nmm
        Pu = axial_load * 1000  # N
        
        # Interaction diagram approach
        # Simplified - assume tension controls
        c = d / 2  # Neutral axis depth (initial guess)
        
        # Compression zone
        Cc = 0.36 * self.fck * c * thickness
        
        # Required tension steel
        T = Mu / (0.9 * d) + Pu
        Ast = T / (0.87 * self.fy)
        
        # Minimum steel
        Ast_min = 0.0025 * Ag  # 0.25% of gross area
        Ast = max(Ast, Ast_min)
        
        # Distribute steel in boundary elements
        if boundary_element:
            # Boundary element width
            be_width = max(thickness, length / 10)
            be_length = max(3 * thickness, 450)
            
            # Concentrate 60% in boundary elements
            Ast_boundary = 0.6 * Ast
            Ast_web = 0.4 * Ast
            
            # Boundary element design
            bar_dia = 20  # mm
            bar_area = np.pi * bar_dia**2 / 4
            n_bars = int(np.ceil(Ast_boundary / (2 * bar_area)))
            
            boundary_steel = {
                "width": be_width,
                "length": be_length,
                "bars": n_bars,
                "bar_diameter": bar_dia,
                "designation": f"{n_bars}-{bar_dia}mm bars each end"
            }
        else:
            boundary_steel = None
            Ast_web = Ast
        
        # Web reinforcement
        # Horizontal steel
        rho_h_min = 0.0025  # 0.25%
        Ash = rho_h_min * thickness * 1000  # mm²/m
        
        bar_dia_h = 12
        bar_area_h = np.pi * bar_dia_h**2 / 4
        spacing_h = bar_area_h * 1000 / Ash
        spacing_h = min(spacing_h, 3 * thickness, 450)
        
        # Vertical steel
        rho_v_min = 0.0025
        Asv = rho_v_min * thickness * 1000
        
        bar_dia_v = 12
        bar_area_v = np.pi * bar_dia_v**2 / 4
        spacing_v = bar_area_v * 1000 / Asv
        spacing_v = min(spacing_v, 3 * thickness, 450)
        
        # Shear design
        tau_v = (shear_force * 1000) / (length * thickness)  # MPa
        
        # Shear strength of concrete
        tau_c = 0.25 * np.sqrt(self.fck)  # Simplified
        
        if tau_v <= tau_c:
            shear_status = "OK - Concrete alone sufficient"
            shear_reinforcement = "Minimum"
        else:
            shear_status = "Additional shear reinforcement required"
            # Calculate additional shear reinforcement
            Vus = (tau_v - tau_c) * length * thickness / 1000  # kN
            
            # Horizontal shear reinforcement
            Ash_shear = (Vus * 1000) / (0.87 * self.fy * 0.9 * length)
            spacing_h = min(spacing_h, bar_area_h * 1000 / Ash_shear)
            
            shear_reinforcement = f"Enhanced - {bar_dia_h}mm @ {spacing_h:.0f}mm"
        
        return {
            "wall_type": "shear_wall",
            "slenderness_ratio": slenderness_ratio,
            "classification": "short" if slenderness_ratio < 12 else "slender",
            "axial_capacity": {
                "applied_load": axial_load,
                "capacity": P_max,
                "utilization": (axial_load / P_max) * 100,
                "status": "OK" if axial_check else "FAIL"
            },
            "flexural_design": {
                "required_steel": Ast,
                "provided_steel": Ast,
                "boundary_elements": boundary_steel
            },
            "web_reinforcement": {
                "horizontal": {
                    "bar_diameter": bar_dia_h,
                    "spacing": spacing_h,
                    "designation": f"{bar_dia_h}mm @ {spacing_h:.0f}mm c/c"
                },
                "vertical": {
                    "bar_diameter": bar_dia_v,
                    "spacing": spacing_v,
                    "designation": f"{bar_dia_v}mm @ {spacing_v:.0f}mm c/c"
                }
            },
            "shear_design": {
                "applied_stress": tau_v,
                "concrete_capacity": tau_c,
                "status": shear_status,
                "reinforcement": shear_reinforcement
            },
            "code": self.code
        }
    
    def design_coupling_beam(self, span: float, depth: float, width: float,
                            shear_force: float, moment: float) -> Dict:
        """
        Design coupling beam between shear walls
        
        Args:
            span: Clear span (mm)
            depth: Beam depth (mm)
            width: Beam width (mm)
            shear_force: Factored shear (kN)
            moment: Factored moment (kNm)
        """
        # Effective depth
        cover = 40
        bar_dia = 20
        d = depth - cover - bar_dia/2
        
        # Flexural design
        Mu = moment * 1e6  # Nmm
        b = width
        
        # Required steel
        Ast = (Mu) / (0.87 * self.fy * 0.9 * d)
        
        # Minimum steel
        Ast_min = 0.85 * b * d / self.fy
        Ast = max(Ast, Ast_min)
        
        # Bar arrangement
        bar_area = np.pi * bar_dia**2 / 4
        n_bars = int(np.ceil(Ast / bar_area))
        
        # Shear design
        Vu = shear_force * 1000  # N
        tau_v = Vu / (b * d)  # MPa
        
        # Diagonal reinforcement for high shear
        if tau_v > 0.5 * np.sqrt(self.fck):
            # Use diagonal bars
            diagonal_design = True
            
            # Diagonal bar area
            alpha = 45  # degrees
            Asd = Vu / (2 * 0.87 * self.fy * np.sin(np.radians(alpha)))
            
            n_diag_bars = int(np.ceil(Asd / bar_area))
            
            diagonal_steel = {
                "required": True,
                "bars": n_diag_bars,
                "diameter": bar_dia,
                "angle": alpha,
                "designation": f"{n_diag_bars}-{bar_dia}mm diagonal bars"
            }
        else:
            diagonal_design = False
            diagonal_steel = {"required": False}
        
        # Stirrups
        stirrup_dia = 10
        stirrup_area = 2 * np.pi * stirrup_dia**2 / 4  # 2-legged
        
        # Spacing
        Vs = Vu - 0.5 * np.sqrt(self.fck) * b * d
        if Vs > 0:
            spacing = (0.87 * self.fy * stirrup_area * d) / Vs
            spacing = min(spacing, 0.75 * d, 300)
        else:
            spacing = min(0.75 * d, 300)
        
        return {
            "beam_type": "coupling_beam",
            "flexural_design": {
                "Ast_required": Ast,
                "bars": n_bars,
                "diameter": bar_dia,
                "designation": f"{n_bars}-{bar_dia}mm"
            },
            "shear_design": {
                "applied_stress": tau_v,
                "diagonal_reinforcement": diagonal_steel,
                "stirrups": {
                    "diameter": stirrup_dia,
                    "spacing": spacing,
                    "designation": f"{stirrup_dia}mm @ {spacing:.0f}mm c/c"
                }
            },
            "code": self.code
        }
