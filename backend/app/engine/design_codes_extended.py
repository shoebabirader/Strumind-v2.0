"""
Extended Design Codes Module
Eurocode, British Standards, Australian Standards, Chinese Codes
"""
import numpy as np
from typing import Dict

class Eurocode2(object):
    """Eurocode 2 - Design of Concrete Structures"""
    
    def __init__(self):
        self.code_name = "EC2"
        self.gamma_c = 1.5  # Partial factor for concrete
        self.gamma_s = 1.15  # Partial factor for steel
        
    def flexural_design(self, M: float, b: float, d: float, 
                       fck: float, fyk: float) -> Dict:
        """
        Flexural design per Eurocode 2
        
        Args:
            M: Design moment (kNm)
            b: Width (mm)
            d: Effective depth (mm)
            fck: Characteristic concrete strength (MPa)
            fyk: Characteristic steel strength (MPa)
        """
        # Design strengths
        fcd = fck / self.gamma_c
        fyd = fyk / self.gamma_s
        
        # Moment coefficient
        K = (M * 1e6) / (b * d**2 * fcd)
        
        # Check if compression reinforcement needed
        K_bal = 0.167  # Balanced section
        
        if K <= K_bal:
            # Singly reinforced
            z = d * (0.5 + np.sqrt(0.25 - K / 1.134))
            z = min(z, 0.95 * d)
            As = (M * 1e6) / (fyd * z)
            
            return {
                "section_type": "singly_reinforced",
                "As_required": As,
                "z_lever_arm": z,
                "K": K,
                "status": "OK",
                "code": "Eurocode 2"
            }
        else:
            # Doubly reinforced required
            return {
                "section_type": "doubly_reinforced",
                "status": "REQUIRES_COMPRESSION_STEEL",
                "K": K,
                "code": "Eurocode 2"
            }
    
    def shear_design(self, V: float, b: float, d: float,
                    fck: float, As: float) -> Dict:
        """Shear design per Eurocode 2"""
        # Concrete shear resistance
        rho_l = min(As / (b * d), 0.02)
        k = min(1 + np.sqrt(200 / d), 2.0)
        
        v_min = 0.035 * k**1.5 * np.sqrt(fck)
        v_Rd_c = max(0.12 * k * (100 * rho_l * fck)**(1/3), v_min)
        
        V_Rd_c = v_Rd_c * b * d / 1000  # kN
        
        if V <= V_Rd_c:
            return {
                "shear_reinforcement": "minimum",
                "V_Rd_c": V_Rd_c,
                "status": "OK",
                "code": "Eurocode 2"
            }
        else:
            # Calculate required shear reinforcement
            theta = 21.8  # degrees (cot theta = 2.5)
            Asw_s = (V * 1000) / (0.9 * d * (fyk / self.gamma_s) * 2.5)
            
            return {
                "shear_reinforcement": "required",
                "Asw_s": Asw_s,
                "V_Rd_c": V_Rd_c,
                "status": "OK",
                "code": "Eurocode 2"
            }

class BS8110(object):
    """BS 8110 - British Standard for Concrete Design"""
    
    def __init__(self):
        self.code_name = "BS8110"
        self.gamma_m = 1.5  # Material safety factor
        
    def flexural_design(self, M: float, b: float, d: float,
                       fcu: float, fy: float) -> Dict:
        """
        Flexural design per BS 8110
        
        Args:
            M: Design moment (kNm)
            b: Width (mm)
            d: Effective depth (mm)
            fcu: Characteristic cube strength (MPa)
            fy: Characteristic steel strength (MPa)
        """
        # Design stresses
        fcu_design = 0.67 * fcu / self.gamma_m
        fy_design = 0.87 * fy
        
        # Moment coefficient
        K = (M * 1e6) / (b * d**2 * fcu_design)
        
        # K' for balanced section
        K_prime = 0.156
        
        if K <= K_prime:
            # Singly reinforced
            z = d * (0.5 + np.sqrt(0.25 - K / 0.9))
            z = min(z, 0.95 * d)
            As = (M * 1e6) / (fy_design * z)
            
            # Minimum reinforcement
            As_min = 0.13 * b * d / 100
            As = max(As, As_min)
            
            return {
                "section_type": "singly_reinforced",
                "As_required": As,
                "As_min": As_min,
                "z_lever_arm": z,
                "status": "OK",
                "code": "BS 8110"
            }
        else:
            return {
                "section_type": "doubly_reinforced",
                "status": "REQUIRES_COMPRESSION_STEEL",
                "code": "BS 8110"
            }
    
    def shear_design(self, V: float, b: float, d: float,
                    fcu: float, As: float) -> Dict:
        """Shear design per BS 8110"""
        # Concrete shear stress
        v = (V * 1000) / (b * d)
        
        # Design concrete shear stress
        rho = min(100 * As / (b * d), 3.0)
        vc = 0.79 * (rho / 100)**(1/3) * (fcu / 25)**(1/3) / self.gamma_m
        vc = max(vc, 0.4)
        
        if v <= vc:
            return {
                "shear_reinforcement": "minimum",
                "vc": vc,
                "v": v,
                "status": "OK",
                "code": "BS 8110"
            }
        else:
            # Required shear reinforcement
            Asv_sv = (v - vc) * b / (0.87 * 460)  # Assuming fy = 460 MPa
            
            return {
                "shear_reinforcement": "required",
                "Asv_sv": Asv_sv,
                "vc": vc,
                "v": v,
                "status": "OK",
                "code": "BS 8110"
            }

class AS3600(object):
    """AS 3600 - Australian Standard for Concrete Design"""
    
    def __init__(self):
        self.code_name = "AS3600"
        self.phi = 0.8  # Capacity reduction factor for flexure
        
    def flexural_design(self, M: float, b: float, d: float,
                       fc: float, fsy: float) -> Dict:
        """Flexural design per AS 3600"""
        # Design moment
        Mu = M
        
        # Concrete stress block parameters
        alpha2 = 0.85 - 0.0015 * fc
        alpha2 = max(alpha2, 0.67)
        gamma = 0.97 - 0.0025 * fc
        gamma = max(gamma, 0.67)
        
        # Moment coefficient
        Mu_star = Mu * 1e6
        ku = Mu_star / (self.phi * b * d**2 * alpha2 * fc)
        
        if ku <= 0.36:
            # Singly reinforced
            dn = ku * d
            z = d - gamma * dn / 2
            Ast = Mu_star / (self.phi * fsy * z)
            
            # Minimum reinforcement
            Ast_min = 0.2 * np.sqrt(fc) * b * d / fsy
            Ast = max(Ast, Ast_min)
            
            return {
                "section_type": "singly_reinforced",
                "Ast_required": Ast,
                "Ast_min": Ast_min,
                "ku": ku,
                "status": "OK",
                "code": "AS 3600"
            }
        else:
            return {
                "section_type": "doubly_reinforced",
                "status": "REQUIRES_COMPRESSION_STEEL",
                "ku": ku,
                "code": "AS 3600"
            }

class GB50010(object):
    """GB 50010 - Chinese Code for Concrete Design"""
    
    def __init__(self):
        self.code_name = "GB50010"
        self.gamma_c = 1.4  # Partial factor for concrete
        self.gamma_s = 1.1  # Partial factor for steel
        
    def flexural_design(self, M: float, b: float, h0: float,
                       fc: float, fy: float) -> Dict:
        """Flexural design per GB 50010"""
        # Design strengths
        fc_design = fc / self.gamma_c
        fy_design = fy / self.gamma_s
        
        # Relative height of compression zone
        alpha_s = M * 1e6 / (fc_design * b * h0**2)
        
        if alpha_s <= 0.35:
            # Singly reinforced
            xi = 1 - np.sqrt(1 - 2 * alpha_s)
            As = (fc_design * b * h0 * xi) / fy_design
            
            # Minimum reinforcement
            rho_min = max(0.2, 45 / fy)
            As_min = rho_min * b * h0 / 100
            As = max(As, As_min)
            
            return {
                "section_type": "singly_reinforced",
                "As_required": As,
                "As_min": As_min,
                "xi": xi,
                "status": "OK",
                "code": "GB 50010"
            }
        else:
            return {
                "section_type": "doubly_reinforced",
                "status": "REQUIRES_COMPRESSION_STEEL",
                "code": "GB 50010"
            }

class Eurocode3(object):
    """Eurocode 3 - Design of Steel Structures"""
    
    def __init__(self):
        self.code_name = "EC3"
        self.gamma_M0 = 1.0
        self.gamma_M1 = 1.0
        
    def member_design(self, N: float, M: float, A: float,
                     W: float, fy: float) -> Dict:
        """Member design per Eurocode 3"""
        # Design strength
        fy_design = fy / self.gamma_M0
        
        # Axial capacity
        Nc_Rd = A * fy_design / 1000  # kN
        
        # Moment capacity
        Mc_Rd = W * fy_design / 1e6  # kNm
        
        # Interaction check
        if N / Nc_Rd + M / Mc_Rd <= 1.0:
            status = "OK"
        else:
            status = "FAIL"
        
        return {
            "Nc_Rd": Nc_Rd,
            "Mc_Rd": Mc_Rd,
            "utilization": (N / Nc_Rd + M / Mc_Rd) * 100,
            "status": status,
            "code": "Eurocode 3"
        }

class BS5950(object):
    """BS 5950 - British Standard for Steel Design"""
    
    def __init__(self):
        self.code_name = "BS5950"
        self.gamma_m = 1.0
        
    def member_design(self, N: float, M: float, A: float,
                     Z: float, py: float) -> Dict:
        """Member design per BS 5950"""
        # Design strength
        py_design = py / self.gamma_m
        
        # Axial capacity
        Pc = A * py_design / 1000  # kN
        
        # Moment capacity
        Mc = Z * py_design / 1e6  # kNm
        
        # Interaction check (simplified)
        utilization = N / Pc + M / Mc
        
        if utilization <= 1.0:
            status = "OK"
        else:
            status = "FAIL"
        
        return {
            "Pc": Pc,
            "Mc": Mc,
            "utilization": utilization * 100,
            "status": status,
            "code": "BS 5950"
        }
