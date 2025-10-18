"""
Steel Connection Design Module
Supports: IS 800, AISC 360
"""
import numpy as np
from typing import Dict, List
from enum import Enum

class ConnectionType(Enum):
    MOMENT_WELDED = "moment_welded"
    MOMENT_BOLTED = "moment_bolted"
    SHEAR_SIMPLE = "shear_simple"
    SHEAR_SEMI_RIGID = "shear_semi_rigid"
    BASE_PLATE = "base_plate"
    SPLICE = "splice"

class SteelConnectionDesign:
    """Steel connection design per IS 800 and AISC 360"""
    
    def __init__(self, code: str = "IS800"):
        self.code = code
        self.fy = 250  # MPa (steel grade)
        self.fu = 410  # MPa (ultimate strength)
        self.gamma_m0 = 1.10  # Partial safety factor (IS 800)
        self.gamma_m1 = 1.25  # Partial safety factor (IS 800)
        
    def moment_connection_bolted(self, M: float, V: float, 
                                 beam_depth: float, bolt_dia: float,
                                 n_bolts: int) -> Dict:
        """
        Design bolted moment connection
        
        Args:
            M: Applied moment (kNm)
            V: Applied shear (kN)
            beam_depth: Beam depth (mm)
            bolt_dia: Bolt diameter (mm)
            n_bolts: Number of bolts in tension zone
        """
        # Validate beam depth to prevent division by zero
        if beam_depth <= 100:
            raise ValueError(
                f"Beam depth must be greater than 100mm for moment connection. "
                f"Got beam_depth={beam_depth}mm. Minimum recommended: 150mm"
            )
        
        # Bolt properties
        if self.code == "IS800":
            fub = 400  # MPa for Grade 4.6 bolts
            Anb = np.pi * (bolt_dia - 2) ** 2 / 4  # Net area
            Asb = np.pi * bolt_dia ** 2 / 4  # Shank area
        else:  # AISC
            fub = 400
            Anb = 0.75 * np.pi * bolt_dia ** 2 / 4
            Asb = np.pi * bolt_dia ** 2 / 4
        
        # Bolt capacity in tension
        Tnb = 0.9 * fub * Anb / (self.gamma_m1 * 1000)  # kN
        
        # Bolt capacity in shear
        Vnsb = (fub / np.sqrt(3)) * Asb / (self.gamma_m1 * 1000)  # kN
        
        # Force per bolt due to moment
        lever_arm = beam_depth - 100  # Approximate
        T_per_bolt = (M * 1000) / (n_bolts * lever_arm)  # kN
        
        # Force per bolt due to shear
        V_per_bolt = V / (n_bolts * 2)  # Assuming bolts on both sides
        
        # Interaction check
        interaction = (T_per_bolt / Tnb) ** 2 + (V_per_bolt / Vnsb) ** 2
        
        status = "OK" if interaction <= 1.0 else "FAIL"
        
        return {
            "bolt_diameter": bolt_dia,
            "number_of_bolts": n_bolts,
            "tension_capacity": Tnb,
            "shear_capacity": Vnsb,
            "tension_demand": T_per_bolt,
            "shear_demand": V_per_bolt,
            "interaction_ratio": interaction,
            "utilization": interaction * 100,
            "status": status,
            "code": self.code
        }
    
    def moment_connection_welded(self, M: float, V: float,
                                 beam_depth: float, flange_width: float,
                                 weld_size: float) -> Dict:
        """
        Design welded moment connection
        
        Args:
            M: Applied moment (kNm)
            V: Applied shear (kN)
            beam_depth: Beam depth (mm)
            flange_width: Flange width (mm)
            weld_size: Fillet weld size (mm)
        """
        # Validate beam depth to prevent division by zero
        if beam_depth <= 20:
            raise ValueError(
                f"Beam depth must be greater than 20mm for welded moment connection. "
                f"Got beam_depth={beam_depth}mm. Minimum recommended: 100mm"
            )
        
        # Weld properties
        fu_weld = 410  # MPa
        throat_thickness = 0.7 * weld_size  # mm
        
        # Weld strength per IS 800
        fwd = fu_weld / (np.sqrt(3) * self.gamma_m1)  # MPa
        
        # Flange weld (resists moment)
        lever_arm = beam_depth - 20  # Approximate
        flange_force = (M * 1000) / lever_arm  # kN
        
        # Required weld length for flange
        weld_length_flange = flange_width
        weld_capacity_flange = fwd * throat_thickness * weld_length_flange / 1000  # kN
        
        # Web weld (resists shear)
        weld_length_web = beam_depth - 2 * 20  # Excluding flanges
        weld_capacity_web = fwd * throat_thickness * weld_length_web / 1000  # kN
        
        # Utilization
        flange_utilization = flange_force / weld_capacity_flange
        web_utilization = V / weld_capacity_web
        
        status = "OK" if max(flange_utilization, web_utilization) <= 1.0 else "FAIL"
        
        return {
            "weld_size": weld_size,
            "throat_thickness": throat_thickness,
            "weld_strength": fwd,
            "flange_weld_length": weld_length_flange,
            "flange_capacity": weld_capacity_flange,
            "flange_demand": flange_force,
            "flange_utilization": flange_utilization * 100,
            "web_weld_length": weld_length_web,
            "web_capacity": weld_capacity_web,
            "web_demand": V,
            "web_utilization": web_utilization * 100,
            "status": status,
            "code": self.code
        }
    
    def shear_connection_simple(self, V: float, bolt_dia: float,
                                n_bolts: int, edge_distance: float) -> Dict:
        """
        Design simple shear connection (shear tab or angle)
        """
        # Bolt shear capacity
        fub = 400  # MPa
        Asb = np.pi * bolt_dia ** 2 / 4
        Vnsb = (fub / np.sqrt(3)) * Asb / (self.gamma_m1 * 1000)  # kN per bolt
        
        # Total capacity
        total_capacity = n_bolts * Vnsb
        
        # Bearing capacity check
        fu_plate = self.fu
        t_plate = 10  # mm (assumed plate thickness)
        kb = min(edge_distance / (3 * bolt_dia), fub / fu_plate, 1.0)
        Vnpb = 2.5 * kb * bolt_dia * t_plate * fu_plate / (self.gamma_m1 * 1000)  # kN
        
        # Governing capacity
        capacity = min(total_capacity, n_bolts * Vnpb)
        utilization = V / capacity
        
        status = "OK" if utilization <= 1.0 else "FAIL"
        
        return {
            "bolt_diameter": bolt_dia,
            "number_of_bolts": n_bolts,
            "bolt_shear_capacity": Vnsb,
            "bearing_capacity": Vnpb,
            "total_capacity": capacity,
            "shear_demand": V,
            "utilization": utilization * 100,
            "status": status,
            "code": self.code
        }
    
    def base_plate_design(self, P: float, M: float, 
                         column_size: float, concrete_grade: float) -> Dict:
        """
        Design column base plate
        
        Args:
            P: Axial load (kN)
            M: Moment (kNm)
            column_size: Column dimension (mm)
            concrete_grade: fck (MPa)
        """
        # Assume square base plate
        # Required area
        fck = concrete_grade
        bearing_strength = 0.45 * fck  # MPa
        
        # Eccentricity
        e = (M * 1000) / P if P > 0 else 0  # mm
        
        # Required base plate size (simplified)
        B_req = np.sqrt((P * 1000) / bearing_strength)  # mm
        B = max(B_req, column_size + 200)  # Add margin
        
        # Actual bearing pressure
        if e < B / 6:
            # No tension
            p_max = (P * 1000 / (B ** 2)) * (1 + 6 * e / B)  # MPa
            p_min = (P * 1000 / (B ** 2)) * (1 - 6 * e / B)  # MPa
        else:
            # Tension exists
            a = 3 * (B / 2 - e)  # Compression zone
            p_max = 2 * P * 1000 / (B * a)  # MPa
            p_min = 0
        
        # Base plate thickness
        c = (B - column_size) / 2  # Cantilever length
        M_plate = p_max * c ** 2 / 2  # Moment in plate
        t_req = np.sqrt(6 * M_plate * self.gamma_m0 / self.fy)  # mm
        t = max(t_req, 20)  # Minimum 20mm
        
        status = "OK" if p_max <= bearing_strength else "FAIL"
        
        return {
            "base_plate_size": f"{B}x{B}",
            "base_plate_thickness": t,
            "bearing_pressure_max": p_max,
            "bearing_pressure_min": p_min,
            "bearing_strength": bearing_strength,
            "utilization": (p_max / bearing_strength) * 100,
            "eccentricity": e,
            "status": status,
            "code": self.code
        }
    
    def splice_connection(self, P: float, M: float, V: float,
                         section_depth: float, bolt_dia: float) -> Dict:
        """Design column or beam splice connection"""
        # Validate section depth to prevent division by zero
        if section_depth <= 100:
            raise ValueError(
                f"Section depth must be greater than 100mm for splice connection. "
                f"Got section_depth={section_depth}mm. Minimum recommended: 150mm"
            )
        
        # Number of bolts required
        fub = 400
        Asb = np.pi * bolt_dia ** 2 / 4
        Vnsb = (fub / np.sqrt(3)) * Asb / (self.gamma_m1 * 1000)
        
        # Bolts for shear
        n_shear = int(np.ceil(V / Vnsb)) + 2  # Add 2 for safety
        
        # Bolts for moment (tension/compression)
        # Lever arm is section depth minus cover/edge distance (typically 100mm)
        lever_arm = section_depth - 100
        T = (M * 1000) / lever_arm
        Tnb = 0.9 * fub * 0.75 * Asb / (self.gamma_m1 * 1000)
        n_moment = int(np.ceil(T / Tnb)) + 2
        
        # Total bolts
        n_total = max(n_shear, n_moment)
        n_total = max(n_total, 4)  # Minimum 4 bolts
        
        return {
            "bolt_diameter": bolt_dia,
            "total_bolts": n_total,
            "bolts_for_shear": n_shear,
            "bolts_for_moment": n_moment,
            "bolt_capacity_shear": Vnsb,
            "bolt_capacity_tension": Tnb,
            "status": "OK",
            "code": self.code
        }
    
    def bracing_connection(self, P: float, angle: float,
                          gusset_thickness: float) -> Dict:
        """Design bracing connection with gusset plate"""
        # Resolve forces
        Px = P * np.cos(np.radians(angle))
        Py = P * np.sin(np.radians(angle))
        
        # Gusset plate design
        fy_gusset = self.fy
        t = gusset_thickness
        
        # Whitmore section
        whitmore_width = 200  # mm (assumed)
        A_whitmore = whitmore_width * t
        
        # Capacity
        capacity = fy_gusset * A_whitmore / (self.gamma_m0 * 1000)  # kN
        
        utilization = P / capacity
        status = "OK" if utilization <= 1.0 else "FAIL"
        
        return {
            "gusset_thickness": t,
            "whitmore_width": whitmore_width,
            "capacity": capacity,
            "demand": P,
            "utilization": utilization * 100,
            "horizontal_force": Px,
            "vertical_force": Py,
            "status": status,
            "code": self.code
        }
