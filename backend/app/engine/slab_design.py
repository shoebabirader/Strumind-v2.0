"""
Slab Design Module
"""
import numpy as np
from typing import Dict

class SlabDesign:
    """Slab design calculations"""
    
    def __init__(self, code: str = "IS456"):
        self.code = code
        self.fck = 25  # MPa
        self.fy = 415  # MPa
        
    def one_way_slab_design(self, span: float, thickness: float,
                           loads: Dict, support_condition: str = "simply_supported") -> Dict:
        """One-way slab design"""
        dead_load = loads.get('dead', 0)
        live_load = loads.get('live', 0)
        
        self_weight = thickness * 25 / 1e6
        total_dead = dead_load + self_weight
        wu = 1.5 * total_dead + 1.5 * live_load
        
        moment_coeff = 1/8 if support_condition == "simply_supported" else 1/12
        L = span / 1000
        Mu = moment_coeff * wu * L**2
        
        cover = 25
        bar_dia = 12
        d = thickness - cover - bar_dia/2
        
        Ast = (Mu * 1e6) / (0.87 * self.fy * 0.9 * d)
        Ast_min = 0.12 * 1000 * thickness / 100
        Ast = max(Ast, Ast_min)
        
        bar_area = np.pi * bar_dia**2 / 4
        spacing = bar_area * 1000 / Ast
        spacing = min(spacing, 3 * thickness, 300)
        
        return {
            "slab_type": "one_way",
            "design_moment": Mu,
            "main_reinforcement": {
                "Ast_required": Ast,
                "bar_diameter": bar_dia,
                "spacing": spacing,
                "designation": f"{bar_dia}mm @ {spacing:.0f}mm c/c"
            },
            "status": "OK",
            "code": self.code
        }
    
    def two_way_slab_design(self, lx: float, ly: float, thickness: float,
                           loads: Dict, support_condition: str = "all_edges_supported") -> Dict:
        """Two-way slab design"""
        if lx > ly:
            lx, ly = ly, lx
        
        aspect_ratio = ly / lx
        
        dead_load = loads.get('dead', 0)
        live_load = loads.get('live', 0)
        self_weight = thickness * 25 / 1e6
        
        wu = 1.5 * (dead_load + self_weight) + 1.5 * live_load
        
        if aspect_ratio <= 2.0:
            if aspect_ratio == 1.0:
                alpha_x = alpha_y = 0.062
            else:
                alpha_x = 0.062 + (aspect_ratio - 1.0) * 0.033
                alpha_y = 0.062 - (aspect_ratio - 1.0) * 0.050
        else:
            alpha_x = 1/8
            alpha_y = 0.0
        
        Lx = lx / 1000
        Ly = ly / 1000
        
        Mx = alpha_x * wu * Lx**2
        My = alpha_y * wu * Ly**2
        
        cover = 25
        bar_dia = 12
        d = thickness - cover - bar_dia/2
        
        Ast_x = (Mx * 1e6) / (0.87 * self.fy * 0.9 * d) if Mx > 0 else 0
        Ast_min = 0.12 * 1000 * thickness / 100
        Ast_x = max(Ast_x, Ast_min)
        
        bar_area = np.pi * bar_dia**2 / 4
        spacing_x = bar_area * 1000 / Ast_x if Ast_x > 0 else 300
        spacing_x = min(spacing_x, 3 * thickness, 300)
        
        Ast_y = (My * 1e6) / (0.87 * self.fy * 0.9 * d) if My > 0 else 0
        Ast_y = max(Ast_y, Ast_min)
        
        spacing_y = bar_area * 1000 / Ast_y if Ast_y > 0 else 300
        spacing_y = min(spacing_y, 3 * thickness, 300)
        
        return {
            "slab_type": "two_way",
            "aspect_ratio": aspect_ratio,
            "design_moments": {
                "Mx": Mx,
                "My": My
            },
            "x_direction_steel": {
                "Ast_required": Ast_x,
                "spacing": spacing_x,
                "designation": f"{bar_dia}mm @ {spacing_x:.0f}mm c/c"
            },
            "y_direction_steel": {
                "Ast_required": Ast_y,
                "spacing": spacing_y,
                "designation": f"{bar_dia}mm @ {spacing_y:.0f}mm c/c"
            },
            "status": "OK",
            "code": self.code
        }
    
    def flat_slab_design(self, panel_size: float, column_size: float,
                        thickness: float, loads: Dict) -> Dict:
        """Flat slab design"""
        dead_load = loads.get('dead', 0)
        live_load = loads.get('live', 0)
        self_weight = thickness * 25 / 1e6
        
        wu = 1.5 * (dead_load + self_weight) + 1.5 * live_load
        
        tributary_area = (panel_size / 1000)**2
        Pu = wu * tributary_area
        
        d = thickness - 25 - 6
        bo = 4 * (column_size + d)
        vu = (Pu * 1000) / (bo * d)
        
        tau_c = 0.25 * np.sqrt(self.fck)
        punching_check = vu <= tau_c
        
        return {
            "slab_type": "flat_slab",
            "punching_shear": {
                "applied_stress": vu,
                "allowable_stress": tau_c,
                "status": "OK" if punching_check else "FAIL"
            },
            "status": "OK" if punching_check else "INCREASE_THICKNESS",
            "code": self.code
        }
