from typing import Dict
import numpy as np

class DesignCode:
    """Base class for design codes"""
    def __init__(self, code_name: str):
        self.code_name = code_name
    
    def check_flexure(self, M: float, section: Dict, material: Dict) -> Dict:
        raise NotImplementedError
    
    def check_shear(self, V: float, section: Dict, material: Dict) -> Dict:
        raise NotImplementedError

class IS456(DesignCode):
    """IS 456:2000 - Indian Standard for RC Design"""
    def __init__(self):
        super().__init__("IS456")
    
    def check_flexure(self, M: float, section: Dict, material: Dict) -> Dict:
        b = section['width']
        d = section['effective_depth']
        fck = material['fck']
        fy = material['fy']
        
        Mu_lim = 0.138 * fck * b * d**2
        
        if M <= Mu_lim:
            Ast = M / (0.87 * fy * 0.9 * d)
            return {"status": "OK", "Ast_required": Ast, "section": "singly"}
        else:
            return {"status": "FAIL", "message": "Doubly reinforced required"}
    
    def check_shear(self, V: float, section: Dict, material: Dict) -> Dict:
        b = section['width']
        d = section['effective_depth']
        tau_v = V / (b * d)
        tau_c = 0.85  # Simplified
        
        if tau_v <= tau_c:
            return {"status": "OK", "stirrups": "minimum"}
        else:
            Asv_s = (tau_v - tau_c) * b / (0.87 * material['fy'])
            return {"status": "OK", "Asv_s_required": Asv_s}

class ACI318(DesignCode):
    """ACI 318 - American Concrete Institute"""
    def __init__(self):
        super().__init__("ACI318")
    
    def check_flexure(self, M: float, section: Dict, material: Dict) -> Dict:
        b = section['width']
        d = section['effective_depth']
        fc = material['fc']
        fy = material['fy']
        
        rho_min = max(3 * np.sqrt(fc) / fy, 200 / fy)
        As_min = rho_min * b * d
        
        return {"status": "OK", "As_min": As_min}
    
    def check_shear(self, V: float, section: Dict, material: Dict) -> Dict:
        b = section['width']
        d = section['effective_depth']
        Vc = 0.17 * np.sqrt(material['fc']) * b * d
        
        if V <= Vc:
            return {"status": "OK", "stirrups": "minimum"}
        else:
            return {"status": "OK", "Vs_required": V - Vc}
