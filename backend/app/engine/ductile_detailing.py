"""
Ductile detailing for seismic design
Implements IS 13920, ACI 318 Chapter 18, and Eurocode 8 requirements
"""
import numpy as np
from typing import Dict, List


class DuctileDetailing:
    """Ductile detailing requirements for seismic zones"""
    
    def __init__(self, design_code: str = "IS 13920"):
        self.design_code = design_code
    
    def design_beam_detailing(self, beam_data: Dict, seismic_zone: str) -> Dict:
        """
        Design ductile detailing for beams
        
        Requirements:
        - Minimum longitudinal reinforcement
        - Maximum spacing of stirrups
        - Confinement requirements
        - Anchorage lengths
        """
        
        b = beam_data.get("width", 300)  # mm
        d = beam_data.get("depth", 500)  # mm
        fck = beam_data.get("concrete_grade", 25)  # MPa
        fy = beam_data.get("steel_grade", 415)  # MPa
        
        # Minimum reinforcement
        As_min = 0.24 * np.sqrt(fck) / fy * b * d
        
        # Maximum reinforcement
        As_max = 0.025 * b * d
        
        # Stirrup spacing in critical zones
        if self.design_code == "IS 13920":
            # Critical zone = 2d from face of support
            critical_zone_length = 2 * d
            
            # Spacing in critical zone
            s_critical = min(d / 4, 8 * 12, 24 * 8, 300)  # mm
            
            # Spacing outside critical zone
            s_normal = min(d / 2, 300)  # mm
            
        elif self.design_code == "ACI 318-18":
            critical_zone_length = 2 * d
            s_critical = min(d / 4, 6 * 12, 150)  # mm
            s_normal = d / 2
        
        else:  # Eurocode 8
            critical_zone_length = 1.5 * d
            s_critical = min(d / 4, 6 * 12, 125)  # mm
            s_normal = d / 2
        
        # Confinement reinforcement
        stirrup_dia = self._select_stirrup_diameter(b, d)
        
        # Anchorage length
        Ld = self._calculate_anchorage_length(fy, fck, 20)  # Assuming 20mm bars
        
        return {
            "min_reinforcement": As_min,
            "max_reinforcement": As_max,
            "critical_zone_length": critical_zone_length,
            "stirrup_spacing_critical": s_critical,
            "stirrup_spacing_normal": s_normal,
            "stirrup_diameter": stirrup_dia,
            "anchorage_length": Ld,
            "requirements": self._get_beam_requirements()
        }
    
    def design_column_detailing(self, column_data: Dict, seismic_zone: str) -> Dict:
        """
        Design ductile detailing for columns
        
        Requirements:
        - Minimum longitudinal reinforcement
        - Maximum spacing of ties
        - Confinement requirements
        - Lap splice requirements
        """
        
        b = column_data.get("width", 400)  # mm
        D = column_data.get("depth", 400)  # mm
        fck = column_data.get("concrete_grade", 25)  # MPa
        fy = column_data.get("steel_grade", 415)  # MPa
        
        Ag = b * D  # Gross area
        
        # Minimum reinforcement
        rho_min = 0.008 if self.design_code == "IS 13920" else 0.01
        As_min = rho_min * Ag
        
        # Maximum reinforcement
        rho_max = 0.04 if self.design_code == "IS 13920" else 0.06
        As_max = rho_max * Ag
        
        # Confinement zone length
        if self.design_code == "IS 13920":
            Lo = max(D, b, 450)  # mm
        else:
            Lo = max(D, b, 500)  # mm
        
        # Tie spacing in confinement zone
        s_confine = min(b / 2, D / 2, 100)  # mm
        
        # Tie spacing outside confinement zone
        s_normal = min(b / 2, D / 2, 300)  # mm
        
        # Minimum tie diameter
        tie_dia = max(8, 0.25 * 20)  # Assuming 20mm longitudinal bars
        
        # Lap splice length
        Ld = self._calculate_anchorage_length(fy, fck, 20)
        Ls = 2.0 * Ld  # Lap splice length
        
        return {
            "min_reinforcement": As_min,
            "max_reinforcement": As_max,
            "confinement_zone_length": Lo,
            "tie_spacing_confine": s_confine,
            "tie_spacing_normal": s_normal,
            "tie_diameter": tie_dia,
            "lap_splice_length": Ls,
            "requirements": self._get_column_requirements()
        }
    
    def design_beam_column_joint(self, joint_data: Dict) -> Dict:
        """
        Design beam-column joint detailing
        
        Critical for seismic performance
        """
        
        bc = joint_data.get("column_width", 400)  # mm
        Dc = joint_data.get("column_depth", 400)  # mm
        bb = joint_data.get("beam_width", 300)  # mm
        Db = joint_data.get("beam_depth", 500)  # mm
        fck = joint_data.get("concrete_grade", 25)  # MPa
        fy = joint_data.get("steel_grade", 415)  # MPa
        
        # Calculate confinement spacing based on column dimensions
        # Per IS 13920 Clause 7.4.8
        s_confine = min(bc / 2, Dc / 2, 100)  # mm
        
        # Joint shear stress
        if self.design_code == "IS 13920":
            tau_max = 1.6 * np.sqrt(fck)  # MPa
        else:
            tau_max = 1.7 * np.sqrt(fck)  # MPa
        
        # Joint reinforcement
        # Horizontal ties in joint (IS 13920 Clause 7.4.8)
        Ash = 0.3 * (bc * Dc / bb - 1) * (fck / fy) * bb * s_confine
        
        # Vertical stirrups
        tie_spacing = min(150, bc / 2)
        
        return {
            "max_shear_stress": tau_max,
            "horizontal_ties_area": Ash,
            "tie_spacing": tie_spacing,
            "confinement_spacing": s_confine,
            "requirements": self._get_joint_requirements()
        }
    
    def design_shear_wall_detailing(self, wall_data: Dict) -> Dict:
        """Design ductile detailing for shear walls"""
        
        lw = wall_data.get("length", 3000)  # mm
        tw = wall_data.get("thickness", 200)  # mm
        hw = wall_data.get("height", 3000)  # mm
        fck = wall_data.get("concrete_grade", 25)  # MPa
        fy = wall_data.get("steel_grade", 415)  # MPa
        
        # Minimum vertical reinforcement
        rho_v_min = 0.0025
        Asv_min = rho_v_min * tw * 1000  # per meter height
        
        # Minimum horizontal reinforcement
        rho_h_min = 0.0025
        Ash_min = rho_h_min * tw * 1000  # per meter length
        
        # Boundary element requirements
        if lw / tw > 16:
            # Boundary elements required
            boundary_length = max(0.15 * lw, 1.5 * tw)
            
            # Confinement in boundary elements
            s_confine = min(100, 6 * 12)  # mm
            
            boundary_required = True
        else:
            boundary_required = False
            boundary_length = 0
            s_confine = 0
        
        # Spacing of reinforcement
        s_max = min(tw, 300, 3 * tw)  # mm
        
        return {
            "min_vertical_reinforcement": Asv_min,
            "min_horizontal_reinforcement": Ash_min,
            "boundary_elements_required": boundary_required,
            "boundary_element_length": boundary_length,
            "confinement_spacing": s_confine,
            "max_spacing": s_max,
            "requirements": self._get_shear_wall_requirements()
        }
    
    def _select_stirrup_diameter(self, b: float, d: float) -> int:
        """Select appropriate stirrup diameter"""
        if b <= 300 or d <= 450:
            return 8
        elif b <= 450 or d <= 600:
            return 10
        else:
            return 12
    
    def _calculate_anchorage_length(self, fy: float, fck: float, dia: float) -> float:
        """Calculate development/anchorage length"""
        
        if self.design_code == "IS 13920":
            # IS 456 formula
            Ld = fy * dia / (4 * 1.6 * np.sqrt(fck))
        else:
            # ACI formula
            Ld = fy * dia / (1.1 * np.sqrt(fck))
        
        return Ld
    
    def _get_beam_requirements(self) -> List[str]:
        """Get list of beam detailing requirements"""
        return [
            "Provide closed stirrups in critical zones",
            "First stirrup within 50mm from face of support",
            "Minimum 2 bars continuous at top and bottom",
            "Lap splices not allowed in critical zones",
            "Hooks of stirrups must be 135 degrees",
            "Positive reinforcement at least 50% of negative reinforcement"
        ]
    
    def _get_column_requirements(self) -> List[str]:
        """Get list of column detailing requirements"""
        return [
            "Provide confinement reinforcement in end zones",
            "Minimum 6 longitudinal bars",
            "Lap splices only in central half of column",
            "Ties must have 135-degree hooks",
            "Minimum 4 bars in rectangular ties",
            "Longitudinal bars must be laterally supported"
        ]
    
    def _get_joint_requirements(self) -> List[str]:
        """Get list of joint detailing requirements"""
        return [
            "Provide horizontal ties throughout joint depth",
            "Continue beam bottom bars through joint",
            "Provide adequate anchorage for beam bars",
            "Joint shear stress must not exceed limits",
            "Minimum joint depth equal to column depth"
        ]
    
    def _get_shear_wall_requirements(self) -> List[str]:
        """Get list of shear wall detailing requirements"""
        return [
            "Provide two curtains of reinforcement if thickness > 200mm",
            "Boundary elements required for slender walls",
            "Horizontal reinforcement must be anchored in boundary elements",
            "Minimum reinforcement ratio 0.0025 each direction",
            "Maximum spacing 300mm or 3 times wall thickness"
        ]


def get_ductile_detailing(element_type: str, element_data: Dict,
                          design_code: str = "IS 13920") -> Dict:
    """
    Main function to get ductile detailing requirements
    
    Args:
        element_type: 'beam', 'column', 'joint', or 'shear_wall'
        element_data: Element properties
        design_code: Design code to use
    """
    
    detailer = DuctileDetailing(design_code)
    
    if element_type == "beam":
        return detailer.design_beam_detailing(element_data, "high")
    elif element_type == "column":
        return detailer.design_column_detailing(element_data, "high")
    elif element_type == "joint":
        return detailer.design_beam_column_joint(element_data)
    elif element_type == "shear_wall":
        return detailer.design_shear_wall_detailing(element_data)
    else:
        raise ValueError(f"Unknown element type: {element_type}")
