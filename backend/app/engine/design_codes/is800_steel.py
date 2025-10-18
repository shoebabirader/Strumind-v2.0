"""
IS 800:2007 - Indian Standard Code for Steel Design
Complete implementation of tension, compression, and bending design
"""
import math
from typing import Dict, Tuple, Optional
from enum import Enum


class SteelGrade(str, Enum):
    """Standard steel grades per IS 800"""
    E165 = "E165"
    E250 = "E250"
    E300 = "E300"
    E350 = "E350"
    E410 = "E410"
    E450 = "E450"


class BucklingClass(str, Enum):
    """Buckling classes per IS 800 Table 10"""
    CLASS_A = "a"  # Rolled I, H sections (tf > 40mm)
    CLASS_B = "b"  # Rolled I, H sections (tf ≤ 40mm)
    CLASS_C = "c"  # Hot rolled hollow sections
    CLASS_D = "d"  # Welded sections


class IS800SteelDesign:
    """IS 800:2007 Steel Design Implementation"""
    
    # Partial safety factors (Clause 5.4.1)
    GAMMA_M0 = 1.10  # Resistance governed by yielding
    GAMMA_M1 = 1.25  # Resistance governed by ultimate stress
    
    # Steel grades (MPa)
    STEEL_GRADES = {
        SteelGrade.E165: {'fy': 165, 'fu': 290},
        SteelGrade.E250: {'fy': 250, 'fu': 410},
        SteelGrade.E300: {'fy': 300, 'fu': 440},
        SteelGrade.E350: {'fy': 350, 'fu': 490},
        SteelGrade.E410: {'fy': 410, 'fu': 540},
        SteelGrade.E450: {'fy': 450, 'fu': 550},
    }
    
    def __init__(self, fy: float, fu: float):
        """
        Initialize design parameters
        
        Args:
            fy: Yield strength (MPa)
            fu: Ultimate tensile strength (MPa)
        """
        self.fy = fy
        self.fu = fu
        self.E = 200000  # Young's modulus (MPa)
    
    def tension_member_design(self, T: float, Ag: float, An: float, 
                             Anc: float = None, Avg: float = None) -> Dict:
        """
        Design tension member per IS 800:2007 Clause 6.2
        
        Args:
            T: Design tension force (kN)
            Ag: Gross area of cross-section (mm²)
            An: Net area of cross-section (mm²)
            Anc: Net area at critical section for block shear (mm²)
            Avg: Gross area subjected to shear for block shear (mm²)
        
        Returns:
            Dict with design results
        """
        T_N = T * 1000  # Convert to N
        
        # Design strength governed by yielding (Clause 6.2)
        Tdg = (Ag * self.fy) / self.GAMMA_M0  # N
        
        # Design strength governed by rupture (Clause 6.3)
        Tdn = (0.9 * An * self.fu) / self.GAMMA_M1  # N
        
        # Design strength governed by block shear (Clause 6.4)
        if Anc is not None and Avg is not None:
            # Block shear strength
            Tdb = ((Avg * self.fy / (math.sqrt(3) * self.GAMMA_M0)) + 
                   (0.9 * Anc * self.fu / self.GAMMA_M1))  # N
        else:
            Tdb = float('inf')
        
        # Governing design strength
        Td = min(Tdg, Tdn, Tdb)  # N
        
        # Check adequacy
        utilization_ratio = T_N / Td
        design_ok = utilization_ratio <= 1.0
        
        # Determine governing criterion
        if Td == Tdg:
            governing = 'yielding'
        elif Td == Tdn:
            governing = 'rupture'
        else:
            governing = 'block_shear'
        
        return {
            'status': 'design_ok' if design_ok else 'inadequate',
            'T_applied': T,
            'Tdg_yielding': round(Tdg / 1000, 2),  # kN
            'Tdn_rupture': round(Tdn / 1000, 2),  # kN
            'Tdb_block_shear': round(Tdb / 1000, 2) if Tdb != float('inf') else 'N/A',
            'Td_capacity': round(Td / 1000, 2),  # kN
            'governing_criterion': governing,
            'utilization_ratio': round(utilization_ratio, 3),
            'design_ok': design_ok
        }
    
    def compression_member_design(self, P: float, L: float, section: Dict,
                                  buckling_class: BucklingClass = BucklingClass.CLASS_B,
                                  Kx: float = 1.0, Ky: float = 1.0) -> Dict:
        """
        Design compression member per IS 800:2007 Clause 7
        
        Args:
            P: Design compression force (kN)
            L: Unsupported length (mm)
            section: Dict with section properties (A, rx, ry, Iz, Iy)
            buckling_class: Buckling class (a, b, c, d)
            Kx: Effective length factor about x-axis
            Ky: Effective length factor about y-axis
        
        Returns:
            Dict with design results
        """
        P_N = P * 1000  # Convert to N
        
        A = section['A']  # mm²
        rx = section.get('rx', math.sqrt(section.get('Iz', 0) / A))  # mm
        ry = section.get('ry', math.sqrt(section.get('Iy', 0) / A))  # mm
        
        # Effective lengths
        Lx = Kx * L  # mm
        Ly = Ky * L  # mm
        
        # Slenderness ratios (Clause 7.1.2)
        lambda_x = Lx / rx
        lambda_y = Ly / ry
        lambda_max = max(lambda_x, lambda_y)
        
        # Check slenderness limit (Clause 3.7.1)
        if lambda_max > 180:
            return {
                'status': 'slenderness_exceeded',
                'lambda_max': round(lambda_max, 2),
                'message': f'Slenderness ratio {lambda_max:.1f} exceeds limit of 180'
            }
        
        # Non-dimensional slenderness ratio
        lambda_bar = (lambda_max / math.pi) * math.sqrt(self.fy / self.E)
        
        # Imperfection factor (Table 10)
        alpha = self._get_imperfection_factor(buckling_class)
        
        # Design compressive stress (Clause 7.1.2)
        phi = 0.5 * (1 + alpha * (lambda_bar - 0.2) + lambda_bar**2)
        chi = min(1.0, 1.0 / (phi + math.sqrt(phi**2 - lambda_bar**2)))
        
        fcd = chi * self.fy / self.GAMMA_M0  # N/mm²
        
        # Design compressive strength
        Pd = fcd * A  # N
        
        # Check adequacy
        utilization_ratio = P_N / Pd
        design_ok = utilization_ratio <= 1.0
        
        return {
            'status': 'design_ok' if design_ok else 'inadequate',
            'P_applied': P,
            'lambda_x': round(lambda_x, 2),
            'lambda_y': round(lambda_y, 2),
            'lambda_max': round(lambda_max, 2),
            'lambda_bar': round(lambda_bar, 3),
            'chi': round(chi, 3),
            'fcd': round(fcd, 2),
            'Pd_capacity': round(Pd / 1000, 2),  # kN
            'utilization_ratio': round(utilization_ratio, 3),
            'design_ok': design_ok,
            'buckling_class': buckling_class
        }

    
    def beam_design(self, M: float, V: float, section: Dict,
                   Lb: float = None, lateral_support: str = 'full') -> Dict:
        """
        Design beam for bending per IS 800:2007 Clause 8
        
        Args:
            M: Design bending moment (kN·m)
            V: Design shear force (kN)
            section: Dict with section properties (Zp, Ze, d, tw, Iz, Iy)
            Lb: Laterally unsupported length (mm)
            lateral_support: 'full', 'partial', or 'none'
        
        Returns:
            Dict with design results
        """
        M_Nmm = M * 1e6  # Convert to N·mm
        V_N = V * 1000  # Convert to N
        
        Zp = section.get('Zp', section.get('Ze', 0))  # Plastic section modulus (mm³)
        Ze = section.get('Ze', 0)  # Elastic section modulus (mm³)
        d = section.get('d', 0)  # Depth (mm)
        tw = section.get('tw', 0)  # Web thickness (mm)
        
        # Design bending strength (Clause 8.2)
        if lateral_support == 'full':
            # Fully laterally supported
            beta_b = 1.0
            Md = beta_b * Zp * self.fy / self.GAMMA_M0  # N·mm
        else:
            # Laterally unsupported - check lateral-torsional buckling
            if Lb is None:
                return {
                    'status': 'error',
                    'message': 'Laterally unsupported length required for LTB check'
                }
            
            # Simplified LTB check (Clause 8.2.2)
            Md = self._lateral_torsional_buckling_strength(section, Lb)
        
        # Design shear strength (Clause 8.4)
        Av = d * tw  # Shear area (simplified)
        Vd = (Av * self.fy) / (math.sqrt(3) * self.GAMMA_M0)  # N
        
        # Check adequacy
        bending_ur = M_Nmm / Md
        shear_ur = V_N / Vd
        design_ok = bending_ur <= 1.0 and shear_ur <= 1.0
        
        # Check interaction (high shear)
        if shear_ur > 0.6:
            # Reduce moment capacity (Clause 9.2.2)
            Md_reduced = Md * (1 - ((2 * shear_ur - 1) ** 2))
            bending_ur_reduced = M_Nmm / Md_reduced
            interaction_check = bending_ur_reduced <= 1.0
        else:
            Md_reduced = Md
            interaction_check = True
        
        return {
            'status': 'design_ok' if design_ok and interaction_check else 'inadequate',
            'M_applied': M,
            'Md_capacity': round(Md / 1e6, 2),  # kN·m
            'bending_ur': round(bending_ur, 3),
            'V_applied': V,
            'Vd_capacity': round(Vd / 1000, 2),  # kN
            'shear_ur': round(shear_ur, 3),
            'Md_reduced': round(Md_reduced / 1e6, 2) if shear_ur > 0.6 else 'N/A',
            'interaction_check': interaction_check,
            'design_ok': design_ok and interaction_check,
            'lateral_support': lateral_support
        }
    
    def beam_column_design(self, P: float, Mx: float, My: float,
                          section: Dict, L: float,
                          buckling_class: BucklingClass = BucklingClass.CLASS_B) -> Dict:
        """
        Design beam-column (combined axial and bending) per IS 800 Clause 9
        
        Args:
            P: Design axial force (kN, compression positive)
            Mx: Design moment about major axis (kN·m)
            My: Design moment about minor axis (kN·m)
            section: Dict with section properties
            L: Unsupported length (mm)
            buckling_class: Buckling class
        
        Returns:
            Dict with design results
        """
        # Get compression capacity
        comp_result = self.compression_member_design(P, L, section, buckling_class)
        
        if comp_result['status'] != 'design_ok' and P > 0:
            return {
                'status': 'compression_inadequate',
                'message': 'Section inadequate for compression alone',
                'compression_result': comp_result
            }
        
        # Get bending capacities
        Zp_x = section.get('Zp_x', section.get('Zp', 0))
        Zp_y = section.get('Zp_y', Zp_x * 0.6)  # Approximate if not given
        
        Mdx = Zp_x * self.fy / self.GAMMA_M0 / 1e6  # kN·m
        Mdy = Zp_y * self.fy / self.GAMMA_M0 / 1e6  # kN·m
        
        # Interaction check (Clause 9.3.1)
        P_N = P * 1000
        Pd = comp_result.get('Pd_capacity', 1e10) * 1000  # N
        
        if P_N / Pd <= 0.2:
            # Low axial force - simplified check
            interaction_ratio = (Mx / Mdx) + (My / Mdy)
        else:
            # High axial force - use interaction formula
            Cmx = 0.6  # Equivalent uniform moment factor (simplified)
            Cmy = 0.6
            
            interaction_ratio = (P_N / Pd) + (Cmx * Mx / Mdx) + (Cmy * My / Mdy)
        
        design_ok = interaction_ratio <= 1.0
        
        return {
            'status': 'design_ok' if design_ok else 'inadequate',
            'P_applied': P,
            'Pd_capacity': comp_result.get('Pd_capacity', 0),
            'Mx_applied': Mx,
            'Mdx_capacity': round(Mdx, 2),
            'My_applied': My,
            'Mdy_capacity': round(Mdy, 2),
            'interaction_ratio': round(interaction_ratio, 3),
            'design_ok': design_ok
        }
    
    def connection_bolt_design(self, V: float, n_bolts: int, dia: float,
                              connection_type: str = 'bearing') -> Dict:
        """
        Design bolted connection per IS 800 Clause 10.3
        
        Args:
            V: Design shear force (kN)
            n_bolts: Number of bolts
            dia: Bolt diameter (mm)
            connection_type: 'bearing' or 'friction'
        
        Returns:
            Dict with design results
        """
        V_N = V * 1000  # Convert to N
        
        # Bolt area
        Ab = math.pi * dia**2 / 4  # mm²
        
        # Shear capacity per bolt (Clause 10.3.3)
        # Assuming grade 4.6 bolts
        fub = 400  # Ultimate tensile strength (MPa)
        
        if connection_type == 'bearing':
            # Bearing type connection
            nn = 1  # Number of shear planes (single shear)
            Vdsb = (fub * nn * Ab) / (math.sqrt(3) * self.GAMMA_M1)  # N
        else:
            # Friction type connection (HSFG bolts)
            mu = 0.55  # Coefficient of friction
            Kh = 1.0  # Hole type factor
            ne = 1  # Number of effective interfaces
            Fo = 0.7 * fub * Ab  # Proof load
            Vdsf = (mu * Kh * ne * Fo) / self.GAMMA_M1  # N
            Vdsb = Vdsf
        
        # Total capacity
        Vd_total = n_bolts * Vdsb  # N
        
        # Check adequacy
        utilization_ratio = V_N / Vd_total
        design_ok = utilization_ratio <= 1.0
        
        return {
            'status': 'design_ok' if design_ok else 'inadequate',
            'V_applied': V,
            'Vdsb_per_bolt': round(Vdsb / 1000, 2),  # kN
            'Vd_total': round(Vd_total / 1000, 2),  # kN
            'n_bolts': n_bolts,
            'bolt_diameter': dia,
            'utilization_ratio': round(utilization_ratio, 3),
            'design_ok': design_ok,
            'connection_type': connection_type
        }
    
    def connection_weld_design(self, V: float, L: float, throat: float,
                              weld_type: str = 'fillet') -> Dict:
        """
        Design welded connection per IS 800 Clause 10.5
        
        Args:
            V: Design shear force (kN)
            L: Effective length of weld (mm)
            throat: Throat thickness (mm)
            weld_type: 'fillet' or 'butt'
        
        Returns:
            Dict with design results
        """
        V_N = V * 1000  # Convert to N
        
        # Weld strength (Clause 10.5.7)
        fu = 410  # Ultimate strength of weld metal (MPa)
        
        if weld_type == 'fillet':
            # Effective throat area
            Aw = throat * L  # mm²
            
            # Design strength
            fwd = fu / (math.sqrt(3) * self.GAMMA_M1)  # N/mm²
            Vd = fwd * Aw  # N
        else:
            # Butt weld
            Aw = throat * L
            fwd = fu / self.GAMMA_M1
            Vd = fwd * Aw
        
        # Check adequacy
        utilization_ratio = V_N / Vd
        design_ok = utilization_ratio <= 1.0
        
        return {
            'status': 'design_ok' if design_ok else 'inadequate',
            'V_applied': V,
            'Vd_capacity': round(Vd / 1000, 2),  # kN
            'throat_thickness': throat,
            'weld_length': L,
            'utilization_ratio': round(utilization_ratio, 3),
            'design_ok': design_ok,
            'weld_type': weld_type
        }
    
    def _get_imperfection_factor(self, buckling_class: BucklingClass) -> float:
        """
        Get imperfection factor from IS 800 Table 10
        
        Args:
            buckling_class: Buckling class (a, b, c, d)
        
        Returns:
            Imperfection factor alpha
        """
        factors = {
            BucklingClass.CLASS_A: 0.21,
            BucklingClass.CLASS_B: 0.34,
            BucklingClass.CLASS_C: 0.49,
            BucklingClass.CLASS_D: 0.76,
        }
        return factors.get(buckling_class, 0.34)
    
    def _lateral_torsional_buckling_strength(self, section: Dict, Lb: float) -> float:
        """
        Calculate lateral-torsional buckling strength (simplified)
        
        Args:
            section: Section properties
            Lb: Laterally unsupported length (mm)
        
        Returns:
            Design moment capacity (N·mm)
        """
        Zp = section.get('Zp', section.get('Ze', 0))
        Iy = section.get('Iy', 0)
        A = section.get('A', 0)
        
        # Simplified LTB check
        ry = math.sqrt(Iy / A) if A > 0 else 1
        lambda_LT = Lb / ry
        
        # Non-dimensional slenderness
        lambda_LT_bar = (lambda_LT / math.pi) * math.sqrt(self.fy / self.E)
        
        # Reduction factor (simplified)
        if lambda_LT_bar <= 0.4:
            chi_LT = 1.0
        else:
            phi_LT = 0.5 * (1 + 0.21 * (lambda_LT_bar - 0.2) + lambda_LT_bar**2)
            chi_LT = min(1.0, 1.0 / (phi_LT + math.sqrt(phi_LT**2 - lambda_LT_bar**2)))
        
        Md = chi_LT * Zp * self.fy / self.GAMMA_M0  # N·mm
        
        return Md
    
    def deflection_check(self, L: float, delta: float, 
                        load_type: str = 'live') -> Dict:
        """
        Check deflection limits per IS 800 Clause 5.6.1
        
        Args:
            L: Span length (mm)
            delta: Actual deflection (mm)
            load_type: 'live', 'dead', or 'total'
        
        Returns:
            Dict with deflection check results
        """
        # Deflection limits (Table 6)
        limits = {
            'live': L / 360,  # For live load
            'dead': L / 250,  # For dead load
            'total': L / 250,  # For total load
        }
        
        limit = limits.get(load_type, L / 360)
        
        deflection_ok = delta <= limit
        
        return {
            'actual_deflection': round(delta, 2),
            'allowable_deflection': round(limit, 2),
            'L_delta_ratio': round(L / delta, 0) if delta > 0 else float('inf'),
            'deflection_ok': deflection_ok,
            'load_type': load_type
        }


# Helper functions
def quick_tension_design(T: float, Ag: float, An: float,
                        fy: float = 250, fu: float = 410) -> Dict:
    """Quick tension member design"""
    designer = IS800SteelDesign(fy, fu)
    return designer.tension_member_design(T, Ag, An)


def quick_compression_design(P: float, L: float, section: Dict,
                            fy: float = 250, fu: float = 410) -> Dict:
    """Quick compression member design"""
    designer = IS800SteelDesign(fy, fu)
    return designer.compression_member_design(P, L, section)
