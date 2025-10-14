"""
Staircase Design Module
RC Staircase Design - Dog-legged, Spiral, Cantilever
"""
import numpy as np
from typing import Dict, List

class StaircaseDesign:
    """Comprehensive staircase design"""
    
    def __init__(self, code: str = "IS456"):
        self.code = code
        self.fck = 25  # MPa
        self.fy = 415  # MPa
        
    def dog_legged_stair(self, flight_length: float, flight_width: float,
                        waist_thickness: float, riser: float, tread: float,
                        loads: Dict) -> Dict:
        """
        Design dog-legged staircase
        
        Args:
            flight_length: Horizontal length of flight (mm)
            flight_width: Width of flight (mm)
            waist_thickness: Waist slab thickness (mm)
            riser: Riser height (mm)
            tread: Tread width (mm)
            loads: Load dictionary
        """
        # Calculate inclined length
        n_risers = int(flight_length / tread)
        vertical_rise = n_risers * riser
        inclined_length = np.sqrt(flight_length**2 + vertical_rise**2)
        
        # Load calculation
        dead_load = loads.get('dead', 0)  # kN/m²
        live_load = loads.get('live', 3.0)  # kN/m²
        
        # Self weight
        self_weight = waist_thickness * 25 / 1e6  # kN/m²
        
        # Step weight
        step_weight = (riser / 2) * 25 / 1e6  # Average
        
        # Total dead load on inclined surface
        total_dead = (self_weight + step_weight + dead_load) * (inclined_length / flight_length)
        
        # Factored load per meter width
        wu = 1.5 * total_dead + 1.5 * live_load  # kN/m²
        
        # Design as simply supported beam
        L = inclined_length / 1000  # m
        Mu = wu * L**2 / 8  # kNm/m
        
        # Effective depth
        cover = 25
        bar_dia = 12
        d = waist_thickness - cover - bar_dia/2
        
        # Flexural design
        b = 1000  # Per meter width
        Ast = (Mu * 1e6) / (0.87 * self.fy * 0.9 * d)
        
        # Minimum steel
        Ast_min = 0.12 * b * waist_thickness / 100
        Ast = max(Ast, Ast_min)
        
        # Main reinforcement spacing
        bar_area = np.pi * bar_dia**2 / 4
        spacing_main = bar_area * 1000 / Ast
        spacing_main = min(spacing_main, 3 * waist_thickness, 300)
        
        # Distribution steel
        Ast_dist = 0.12 * b * waist_thickness / 100
        spacing_dist = bar_area * 1000 / Ast_dist
        spacing_dist = min(spacing_dist, 5 * waist_thickness, 450)
        
        # Deflection check
        span_depth_ratio = (inclined_length / d)
        allowable_ratio = 20  # Basic value
        
        deflection_ok = span_depth_ratio <= allowable_ratio
        
        return {
            "stair_type": "dog_legged",
            "geometry": {
                "inclined_length": inclined_length,
                "number_of_risers": n_risers,
                "vertical_rise": vertical_rise,
                "angle": np.degrees(np.arctan(vertical_rise / flight_length))
            },
            "loads": {
                "dead_load": total_dead,
                "live_load": live_load,
                "factored_load": wu
            },
            "design_moment": Mu,
            "main_reinforcement": {
                "Ast_required": Ast,
                "Ast_provided": bar_area * 1000 / spacing_main,
                "bar_diameter": bar_dia,
                "spacing": spacing_main,
                "designation": f"{bar_dia}mm @ {spacing_main:.0f}mm c/c",
                "direction": "parallel to span"
            },
            "distribution_steel": {
                "Ast_required": Ast_dist,
                "bar_diameter": 10,
                "spacing": spacing_dist,
                "designation": f"10mm @ {spacing_dist:.0f}mm c/c",
                "direction": "perpendicular to span"
            },
            "deflection_check": {
                "span_depth_ratio": span_depth_ratio,
                "allowable_ratio": allowable_ratio,
                "status": "OK" if deflection_ok else "INCREASE_DEPTH"
            },
            "code": self.code
        }
    
    def cantilever_stair(self, cantilever_length: float, width: float,
                        waist_thickness: float, riser: float, tread: float,
                        loads: Dict) -> Dict:
        """
        Design cantilever staircase
        
        Args:
            cantilever_length: Cantilever projection (mm)
            width: Tread width (mm)
            waist_thickness: Waist thickness (mm)
            riser: Riser height (mm)
            tread: Tread width (mm)
            loads: Load dictionary
        """
        # Load calculation
        dead_load = loads.get('dead', 0)
        live_load = loads.get('live', 3.0)
        
        self_weight = waist_thickness * 25 / 1e6
        step_weight = (riser / 2) * 25 / 1e6
        
        total_dead = self_weight + step_weight + dead_load
        wu = 1.5 * total_dead + 1.5 * live_load
        
        # Cantilever moment
        L = cantilever_length / 1000
        Mu = wu * L**2 / 2  # kNm/m
        
        # Effective depth
        cover = 25
        bar_dia = 16  # Larger bars for cantilever
        d = waist_thickness - cover - bar_dia/2
        
        # Flexural design
        b = 1000
        Ast = (Mu * 1e6) / (0.87 * self.fy * 0.9 * d)
        
        Ast_min = 0.12 * b * waist_thickness / 100
        Ast = max(Ast, Ast_min)
        
        # Main reinforcement (top)
        bar_area = np.pi * bar_dia**2 / 4
        spacing_main = bar_area * 1000 / Ast
        spacing_main = min(spacing_main, 3 * waist_thickness, 200)  # Tighter spacing
        
        # Distribution steel
        Ast_dist = 0.12 * b * waist_thickness / 100
        spacing_dist = bar_area * 1000 / Ast_dist
        spacing_dist = min(spacing_dist, 5 * waist_thickness, 450)
        
        return {
            "stair_type": "cantilever",
            "design_moment": Mu,
            "main_reinforcement": {
                "Ast_required": Ast,
                "bar_diameter": bar_dia,
                "spacing": spacing_main,
                "designation": f"{bar_dia}mm @ {spacing_main:.0f}mm c/c",
                "location": "top (tension face)"
            },
            "distribution_steel": {
                "bar_diameter": 10,
                "spacing": spacing_dist,
                "designation": f"10mm @ {spacing_dist:.0f}mm c/c"
            },
            "code": self.code
        }
    
    def spiral_stair(self, inner_radius: float, outer_radius: float,
                    waist_thickness: float, total_angle: float,
                    loads: Dict) -> Dict:
        """
        Design spiral staircase
        
        Args:
            inner_radius: Inner radius (mm)
            outer_radius: Outer radius (mm)
            waist_thickness: Waist thickness (mm)
            total_angle: Total angle of spiral (degrees)
            loads: Load dictionary
        """
        # Average radius
        r_avg = (inner_radius + outer_radius) / 2
        
        # Arc length
        arc_length = r_avg * np.radians(total_angle)
        
        # Load calculation
        dead_load = loads.get('dead', 0)
        live_load = loads.get('live', 3.0)
        
        self_weight = waist_thickness * 25 / 1e6
        total_dead = self_weight + dead_load
        wu = 1.5 * total_dead + 1.5 * live_load
        
        # Radial moment
        width = outer_radius - inner_radius
        Mr = wu * width**2 / 8 / 1e6  # kNm/m
        
        # Tangential moment
        Mt = wu * (arc_length / 1000)**2 / 8  # kNm/m
        
        # Design for maximum moment
        Mu = max(Mr, Mt)
        
        # Effective depth
        cover = 25
        bar_dia = 12
        d = waist_thickness - cover - bar_dia/2
        
        # Radial reinforcement
        Ast_r = (Mr * 1e6) / (0.87 * self.fy * 0.9 * d)
        Ast_min = 0.12 * 1000 * waist_thickness / 100
        Ast_r = max(Ast_r, Ast_min)
        
        bar_area = np.pi * bar_dia**2 / 4
        spacing_r = bar_area * 1000 / Ast_r
        spacing_r = min(spacing_r, 3 * waist_thickness, 300)
        
        # Tangential reinforcement
        Ast_t = (Mt * 1e6) / (0.87 * self.fy * 0.9 * d)
        Ast_t = max(Ast_t, Ast_min)
        
        spacing_t = bar_area * 1000 / Ast_t
        spacing_t = min(spacing_t, 3 * waist_thickness, 300)
        
        return {
            "stair_type": "spiral",
            "geometry": {
                "inner_radius": inner_radius,
                "outer_radius": outer_radius,
                "average_radius": r_avg,
                "arc_length": arc_length,
                "total_angle": total_angle
            },
            "design_moments": {
                "radial": Mr,
                "tangential": Mt
            },
            "radial_reinforcement": {
                "Ast_required": Ast_r,
                "spacing": spacing_r,
                "designation": f"{bar_dia}mm @ {spacing_r:.0f}mm c/c"
            },
            "tangential_reinforcement": {
                "Ast_required": Ast_t,
                "spacing": spacing_t,
                "designation": f"{bar_dia}mm @ {spacing_t:.0f}mm c/c"
            },
            "code": self.code
        }
