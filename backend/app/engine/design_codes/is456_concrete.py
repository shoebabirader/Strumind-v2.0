"""
IS 456:2000 - Indian Standard Code for Concrete Design
Complete implementation of flexural, shear, and torsion design
"""
import math
from typing import Dict, Tuple, Optional
from enum import Enum


class ConcreteGrade(str, Enum):
    """Standard concrete grades per IS 456"""
    M15 = "M15"
    M20 = "M20"
    M25 = "M25"
    M30 = "M30"
    M35 = "M35"
    M40 = "M40"
    M45 = "M45"
    M50 = "M50"


class SteelGrade(str, Enum):
    """Standard steel grades per IS 456"""
    Fe250 = "Fe250"
    Fe415 = "Fe415"
    Fe500 = "Fe500"
    Fe550 = "Fe550"


class IS456ConcreteDesign:
    """IS 456:2000 Concrete Design Implementation"""
    
    # Material properties
    CONCRETE_GRADES = {
        ConcreteGrade.M15: 15,
        ConcreteGrade.M20: 20,
        ConcreteGrade.M25: 25,
        ConcreteGrade.M30: 30,
        ConcreteGrade.M35: 35,
        ConcreteGrade.M40: 40,
        ConcreteGrade.M45: 45,
        ConcreteGrade.M50: 50,
    }
    
    STEEL_GRADES = {
        SteelGrade.Fe250: 250,
        SteelGrade.Fe415: 415,
        SteelGrade.Fe500: 500,
        SteelGrade.Fe550: 550,
    }
    
    # Partial safety factors (Clause 36.4.2)
    GAMMA_M_CONCRETE = 1.5  # For concrete
    GAMMA_M_STEEL = 1.15  # For steel
    
    def __init__(self, fck: float, fy: float):
        """
        Initialize design parameters
        
        Args:
            fck: Characteristic compressive strength of concrete (MPa)
            fy: Characteristic strength of steel (MPa)
        """
        self.fck = fck
        self.fy = fy
        
        # Design strengths
        self.fcd = 0.67 * fck / self.GAMMA_M_CONCRETE  # Clause 36.4.2
        self.fyd = fy / self.GAMMA_M_STEEL
        
        # Limiting values (Clause 38.1)
        self.xu_max_d = 0.48 if fck <= 30 else (0.46 if fck <= 35 else 0.44)
        
    def flexural_design_singly_reinforced(self, M: float, b: float, d: float) -> Dict:
        """
        Design singly reinforced rectangular beam for flexure
        Per IS 456:2000 Clause 38
        
        Args:
            M: Design moment (kN·m)
            b: Width of beam (mm)
            d: Effective depth (mm)
        
        Returns:
            Dict with design results
        """
        M_Nmm = M * 1e6  # Convert kN·m to N·mm
        
        # Step 1: Calculate limiting moment of resistance (Clause 38.1)
        Mu_lim = 0.138 * self.fck * b * d**2 / 1e6  # kN·m
        
        # Step 2: Check if singly reinforced is sufficient
        if M > Mu_lim:
            return {
                'status': 'doubly_reinforced_required',
                'Mu_lim': Mu_lim,
                'M': M,
                'message': f'Moment {M:.2f} kN·m exceeds limiting moment {Mu_lim:.2f} kN·m. Doubly reinforced section required.'
            }
        
        # Step 3: Calculate required steel area (Clause 38.1)
        # M = 0.87 * fy * Ast * d * (1 - (Ast * fy)/(b * d * fck))
        # Solving quadratic equation
        
        R = M_Nmm / (b * d**2)  # N/mm²
        
        # Using simplified formula
        k = M_Nmm / (self.fck * b * d**2)
        j = 1 - (k / 3)
        
        Ast = M_Nmm / (0.87 * self.fy * j * d)  # mm²
        
        # Step 4: Check minimum steel (Clause 26.5.1.1)
        Ast_min = 0.85 * b * d / self.fy  # mm²
        
        if Ast < Ast_min:
            Ast = Ast_min
            status = 'minimum_steel_governs'
        else:
            status = 'design_ok'
        
        # Step 5: Check maximum steel (Clause 26.5.1.1)
        Ast_max = 0.04 * b * d  # mm² (4% of gross area)
        
        if Ast > Ast_max:
            return {
                'status': 'maximum_steel_exceeded',
                'Ast_required': Ast,
                'Ast_max': Ast_max,
                'message': f'Required steel {Ast:.0f} mm² exceeds maximum {Ast_max:.0f} mm²'
            }
        
        # Step 6: Calculate neutral axis depth
        xu = (0.87 * self.fy * Ast) / (0.36 * self.fck * b)  # mm
        xu_d = xu / d
        
        # Step 7: Check if section is under-reinforced
        if xu_d > self.xu_max_d:
            section_type = 'over_reinforced'
        else:
            section_type = 'under_reinforced'
        
        # Step 8: Calculate moment capacity
        Mu = 0.87 * self.fy * Ast * d * (1 - (0.42 * xu / d)) / 1e6  # kN·m
        
        # Step 9: Bar spacing and detailing
        bar_sizes = [8, 10, 12, 16, 20, 25, 32, 40]  # mm
        bar_details = self._calculate_bar_arrangement(Ast, b, bar_sizes)
        
        return {
            'status': status,
            'section_type': section_type,
            'Ast_required': round(Ast, 2),
            'Ast_min': round(Ast_min, 2),
            'Ast_max': round(Ast_max, 2),
            'xu': round(xu, 2),
            'xu_d': round(xu_d, 3),
            'xu_max_d': self.xu_max_d,
            'Mu_capacity': round(Mu, 2),
            'M_applied': M,
            'utilization_ratio': round(M / Mu, 3),
            'bar_arrangement': bar_details,
            'design_ok': M <= Mu and Ast >= Ast_min and Ast <= Ast_max
        }
    
    def flexural_design_doubly_reinforced(self, M: float, b: float, d: float, 
                                         d_prime: float = None) -> Dict:
        """
        Design doubly reinforced rectangular beam
        Per IS 456:2000 Clause 38.1
        
        Args:
            M: Design moment (kN·m)
            b: Width of beam (mm)
            d: Effective depth (mm)
            d_prime: Effective cover to compression steel (mm)
        
        Returns:
            Dict with design results
        """
        if d_prime is None:
            d_prime = 0.1 * d  # Assume 10% of d
        
        M_Nmm = M * 1e6
        
        # Step 1: Calculate limiting moment
        Mu_lim = 0.138 * self.fck * b * d**2 / 1e6  # kN·m
        
        # Step 2: Calculate additional moment
        Mu2 = M - Mu_lim  # kN·m
        Mu2_Nmm = Mu2 * 1e6
        
        # Step 3: Calculate compression steel
        fsc = 0.87 * self.fy  # Stress in compression steel
        Asc = Mu2_Nmm / (fsc * (d - d_prime))  # mm²
        
        # Step 4: Calculate tension steel
        # For limiting moment
        Ast1 = (0.138 * self.fck * b * d) / (0.87 * self.fy)  # mm²
        
        # For additional moment
        Ast2 = Mu2_Nmm / (0.87 * self.fy * (d - d_prime))  # mm²
        
        Ast = Ast1 + Ast2  # mm²
        
        # Step 5: Check minimum and maximum steel
        Ast_min = 0.85 * b * d / self.fy
        Ast_max = 0.04 * b * d
        
        if Ast < Ast_min:
            Ast = Ast_min
        
        if Ast > Ast_max or Asc > 0.04 * b * d:
            return {
                'status': 'maximum_steel_exceeded',
                'message': 'Steel area exceeds maximum limit'
            }
        
        # Step 6: Calculate moment capacity
        Mu = Mu_lim + (0.87 * self.fy * Asc * (d - d_prime)) / 1e6  # kN·m
        
        return {
            'status': 'design_ok',
            'section_type': 'doubly_reinforced',
            'Ast_required': round(Ast, 2),
            'Asc_required': round(Asc, 2),
            'Mu_lim': round(Mu_lim, 2),
            'Mu_capacity': round(Mu, 2),
            'M_applied': M,
            'utilization_ratio': round(M / Mu, 3),
            'design_ok': M <= Mu
        }
    
    def shear_design(self, V: float, b: float, d: float, Ast: float) -> Dict:
        """
        Design for shear per IS 456:2000 Clause 40
        
        Args:
            V: Design shear force (kN)
            b: Width of beam (mm)
            d: Effective depth (mm)
            Ast: Area of tension steel (mm²)
        
        Returns:
            Dict with shear design results
        """
        V_N = V * 1000  # Convert kN to N
        
        # Step 1: Calculate nominal shear stress (Clause 40.1)
        tau_v = V_N / (b * d)  # N/mm²
        
        # Step 2: Calculate percentage of steel
        pt = 100 * Ast / (b * d)  # %
        
        # Step 3: Get permissible shear stress (Table 19)
        tau_c = self._get_permissible_shear_stress(pt, self.fck)
        
        # Step 4: Check if shear reinforcement is required
        if tau_v <= tau_c:
            return {
                'status': 'no_shear_reinforcement_required',
                'tau_v': round(tau_v, 3),
                'tau_c': round(tau_c, 3),
                'shear_reinforcement': 'minimum',
                'message': 'Provide minimum shear reinforcement'
            }
        
        # Step 5: Check maximum shear stress (Clause 40.2.3)
        tau_c_max = self._get_max_shear_stress(self.fck)
        
        if tau_v > tau_c_max:
            return {
                'status': 'section_inadequate',
                'tau_v': round(tau_v, 3),
                'tau_c_max': round(tau_c_max, 3),
                'message': f'Shear stress {tau_v:.3f} exceeds maximum {tau_c_max:.3f}. Increase section size.'
            }
        
        # Step 6: Design shear reinforcement (Clause 40.4)
        Vus = V_N - tau_c * b * d  # Shear to be resisted by stirrups (N)
        
        # Assume 2-legged stirrups
        Asv_s = Vus / (0.87 * self.fy * d)  # mm²/mm
        
        # Step 7: Check minimum shear reinforcement (Clause 26.5.1.6)
        Asv_s_min = 0.4 * b / (0.87 * self.fy)  # mm²/mm
        
        if Asv_s < Asv_s_min:
            Asv_s = Asv_s_min
            status = 'minimum_shear_reinforcement'
        else:
            status = 'design_ok'
        
        # Step 8: Suggest stirrup arrangement
        stirrup_details = self._calculate_stirrup_spacing(Asv_s, d)
        
        return {
            'status': status,
            'tau_v': round(tau_v, 3),
            'tau_c': round(tau_c, 3),
            'tau_c_max': round(tau_c_max, 3),
            'Vus': round(Vus / 1000, 2),  # kN
            'Asv_s_required': round(Asv_s, 4),
            'Asv_s_min': round(Asv_s_min, 4),
            'stirrup_arrangement': stirrup_details,
            'design_ok': tau_v <= tau_c_max
        }

    
    def torsion_design(self, T: float, b: float, D: float, Ast: float, Asc: float = 0) -> Dict:
        """
        Design for torsion per IS 456:2000 Clause 41
        
        Args:
            T: Design torsional moment (kN·m)
            b: Width of beam (mm)
            D: Overall depth of beam (mm)
            Ast: Area of tension steel (mm²)
            Asc: Area of compression steel (mm²)
        
        Returns:
            Dict with torsion design results
        """
        T_Nmm = T * 1e6  # Convert to N·mm
        
        # Step 1: Calculate equivalent shear (Clause 41.1)
        # For rectangular sections
        Ve = T_Nmm / (b * D)  # Equivalent shear stress
        
        # Step 2: Calculate torsional shear stress
        tau_t = T_Nmm / (b**2 * D)  # N/mm²
        
        # Step 3: Check if torsion can be ignored (Clause 41.2)
        tau_t_min = 0.15 * math.sqrt(self.fck)  # N/mm²
        
        if tau_t < tau_t_min:
            return {
                'status': 'torsion_negligible',
                'tau_t': round(tau_t, 3),
                'tau_t_min': round(tau_t_min, 3),
                'message': 'Torsion can be ignored'
            }
        
        # Step 4: Calculate required reinforcement
        # Longitudinal steel for torsion
        x1 = b - 2 * 40  # Assuming 40mm cover
        y1 = D - 2 * 40
        
        Asl_torsion = (T_Nmm * (x1 + y1)) / (0.87 * self.fy * x1 * y1)  # mm²
        
        # Transverse steel for torsion
        Asv_torsion = (T_Nmm) / (0.87 * self.fy * x1 * y1)  # mm²/mm
        
        # Step 5: Total steel requirement
        total_Ast = Ast + Asl_torsion
        
        return {
            'status': 'design_ok',
            'tau_t': round(tau_t, 3),
            'tau_t_min': round(tau_t_min, 3),
            'Asl_torsion': round(Asl_torsion, 2),
            'Asv_torsion': round(Asv_torsion, 4),
            'total_Ast_required': round(total_Ast, 2),
            'design_ok': True
        }
    
    def _get_permissible_shear_stress(self, pt: float, fck: float) -> float:
        """
        Get permissible shear stress from IS 456 Table 19
        
        Args:
            pt: Percentage of tension steel
            fck: Characteristic strength of concrete (MPa)
        
        Returns:
            Permissible shear stress (N/mm²)
        """
        # Simplified interpolation from Table 19
        # For detailed implementation, use full table
        
        if pt <= 0.15:
            k = 0.28
        elif pt <= 0.25:
            k = 0.36
        elif pt <= 0.50:
            k = 0.48
        elif pt <= 0.75:
            k = 0.56
        elif pt <= 1.00:
            k = 0.62
        elif pt <= 1.25:
            k = 0.67
        elif pt <= 1.50:
            k = 0.72
        elif pt <= 1.75:
            k = 0.75
        elif pt <= 2.00:
            k = 0.79
        elif pt <= 2.50:
            k = 0.82
        elif pt <= 3.00:
            k = 0.87
        else:
            k = 0.87
        
        # Adjust for concrete grade
        if fck <= 20:
            factor = 1.0
        elif fck <= 25:
            factor = 1.1
        elif fck <= 30:
            factor = 1.2
        elif fck <= 35:
            factor = 1.25
        else:
            factor = 1.3
        
        return k * factor
    
    def _get_max_shear_stress(self, fck: float) -> float:
        """
        Get maximum shear stress per IS 456 Table 20
        
        Args:
            fck: Characteristic strength of concrete (MPa)
        
        Returns:
            Maximum shear stress (N/mm²)
        """
        # From Table 20
        if fck <= 15:
            return 2.5
        elif fck <= 20:
            return 2.8
        elif fck <= 25:
            return 3.1
        elif fck <= 30:
            return 3.5
        elif fck <= 35:
            return 3.7
        elif fck <= 40:
            return 4.0
        else:
            return 4.0
    
    def _calculate_bar_arrangement(self, Ast: float, b: float, 
                                   bar_sizes: list) -> Dict:
        """
        Calculate bar arrangement for given steel area
        
        Args:
            Ast: Required steel area (mm²)
            b: Width of beam (mm)
            bar_sizes: Available bar sizes (mm)
        
        Returns:
            Dict with bar arrangement options
        """
        arrangements = []
        
        for dia in bar_sizes:
            bar_area = math.pi * dia**2 / 4
            n_bars = math.ceil(Ast / bar_area)
            
            # Check if bars fit in width
            clear_cover = 40  # mm
            stirrup_dia = 8  # mm
            clear_spacing = 25  # mm minimum
            
            required_width = (2 * clear_cover + 2 * stirrup_dia + 
                            n_bars * dia + (n_bars - 1) * clear_spacing)
            
            if required_width <= b:
                provided_area = n_bars * bar_area
                arrangements.append({
                    'bar_size': dia,
                    'number_of_bars': n_bars,
                    'provided_area': round(provided_area, 2),
                    'fits_in_width': True
                })
        
        return arrangements[0] if arrangements else {
            'message': 'No suitable arrangement found. Increase beam width.'
        }
    
    def _calculate_stirrup_spacing(self, Asv_s: float, d: float) -> Dict:
        """
        Calculate stirrup spacing
        
        Args:
            Asv_s: Required stirrup area per unit length (mm²/mm)
            d: Effective depth (mm)
        
        Returns:
            Dict with stirrup details
        """
        stirrup_sizes = [6, 8, 10, 12]  # mm
        arrangements = []
        
        for dia in stirrup_sizes:
            bar_area = math.pi * dia**2 / 4
            # 2-legged stirrup
            Asv = 2 * bar_area
            
            # Calculate spacing
            s = Asv / Asv_s  # mm
            
            # Check maximum spacing (Clause 26.5.1.5)
            s_max = min(0.75 * d, 300)  # mm
            
            if s > s_max:
                s = s_max
            
            # Round to nearest 25mm
            s = math.floor(s / 25) * 25
            
            if s >= 50:  # Minimum practical spacing
                arrangements.append({
                    'stirrup_size': dia,
                    'legs': 2,
                    'spacing': s,
                    'provided_Asv_s': round(Asv / s, 4)
                })
        
        return arrangements[0] if arrangements else {
            'message': 'Use larger stirrup size or reduce spacing'
        }
    
    def development_length(self, dia: float, stress_type: str = 'tension') -> float:
        """
        Calculate development length per IS 456 Clause 26.2.1
        
        Args:
            dia: Bar diameter (mm)
            stress_type: 'tension' or 'compression'
        
        Returns:
            Development length (mm)
        """
        # Design bond stress (Table 21)
        if self.fck <= 20:
            tau_bd = 1.2  # N/mm²
        elif self.fck <= 25:
            tau_bd = 1.4
        elif self.fck <= 30:
            tau_bd = 1.5
        elif self.fck <= 35:
            tau_bd = 1.7
        else:
            tau_bd = 1.9
        
        # Development length
        Ld = (0.87 * self.fy * dia) / (4 * tau_bd)
        
        if stress_type == 'compression':
            Ld = Ld * 0.8  # Reduced for compression
        
        return round(Ld, 0)
    
    def deflection_check(self, L: float, d: float, pt: float, 
                        service_stress: float = None) -> Dict:
        """
        Check deflection per IS 456 Clause 23.2
        
        Args:
            L: Effective span (mm)
            d: Effective depth (mm)
            pt: Percentage of tension steel
            service_stress: Service stress in steel (MPa)
        
        Returns:
            Dict with deflection check results
        """
        # Basic span-to-depth ratio (Table 23)
        basic_ratio = 20  # For simply supported beam
        
        # Modification factor for tension steel (Fig. 4)
        if service_stress is None:
            service_stress = 0.58 * self.fy  # Assumed
        
        # Simplified modification factor
        if service_stress <= 240:
            mf_tension = 2.0
        elif service_stress <= 300:
            mf_tension = 1.5
        else:
            mf_tension = 1.0
        
        # Modification factor for compression steel
        mf_compression = 1.0  # Simplified
        
        # Allowable span-to-depth ratio
        allowable_ratio = basic_ratio * mf_tension * mf_compression
        
        # Actual ratio
        actual_ratio = L / d
        
        return {
            'actual_L_d': round(actual_ratio, 2),
            'allowable_L_d': round(allowable_ratio, 2),
            'deflection_ok': actual_ratio <= allowable_ratio,
            'message': 'OK' if actual_ratio <= allowable_ratio else 'Increase depth'
        }
    
    def crack_width_check(self, spacing: float, cover: float, 
                         dia: float, exposure: str = 'moderate') -> Dict:
        """
        Check crack width per IS 456 Clause 26.3.3
        
        Args:
            spacing: Center-to-center spacing of bars (mm)
            cover: Clear cover to reinforcement (mm)
            dia: Bar diameter (mm)
            exposure: 'mild', 'moderate', 'severe', 'very_severe', 'extreme'
        
        Returns:
            Dict with crack width check results
        """
        # Maximum spacing (Table 26)
        max_spacing_map = {
            'mild': 300,
            'moderate': 300,
            'severe': 150,
            'very_severe': 100,
            'extreme': 100
        }
        
        max_spacing = max_spacing_map.get(exposure, 300)
        
        # Maximum clear cover
        max_cover_map = {
            'mild': 45,
            'moderate': 45,
            'severe': 30,
            'very_severe': 25,
            'extreme': 25
        }
        
        max_cover = max_cover_map.get(exposure, 45)
        
        spacing_ok = spacing <= max_spacing
        cover_ok = cover <= max_cover
        
        return {
            'spacing': spacing,
            'max_spacing': max_spacing,
            'spacing_ok': spacing_ok,
            'cover': cover,
            'max_cover': max_cover,
            'cover_ok': cover_ok,
            'crack_width_ok': spacing_ok and cover_ok,
            'message': 'OK' if (spacing_ok and cover_ok) else 'Reduce spacing or cover'
        }


# Helper functions for quick calculations
def quick_flexural_design(M: float, b: float, d: float, 
                         fck: float = 25, fy: float = 415) -> Dict:
    """Quick flexural design with default material properties"""
    designer = IS456ConcreteDesign(fck, fy)
    return designer.flexural_design_singly_reinforced(M, b, d)


def quick_shear_design(V: float, b: float, d: float, Ast: float,
                      fck: float = 25, fy: float = 415) -> Dict:
    """Quick shear design with default material properties"""
    designer = IS456ConcreteDesign(fck, fy)
    return designer.shear_design(V, b, d, Ast)
