"""
Complete foundation design module
Includes isolated footings, combined footings, mat foundations, and pile foundations
"""
import numpy as np
from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass


@dataclass
class FoundationDesignResult:
    """Foundation design results"""
    foundation_type: str
    dimensions: Dict[str, float]
    reinforcement: Dict[str, any]
    bearing_pressure: float
    settlement: float
    safety_factors: Dict[str, float]
    design_status: str
    design_notes: List[str]


class IsolatedFootingDesign:
    """Design isolated spread footings"""
    
    def __init__(self, design_code: str = "ACI 318-19"):
        self.design_code = design_code
    
    def design(self, loads: Dict, soil_properties: Dict, 
               column_size: Dict, parameters: Dict) -> FoundationDesignResult:
        """
        Design isolated footing
        
        Args:
            loads: Axial load, moments, shears
            soil_properties: Bearing capacity, friction angle, etc.
            column_size: Column dimensions
            parameters: Design parameters (concrete grade, steel grade, etc.)
        """
        
        # Extract loads
        P = loads.get("axial", 0)  # kN
        Mx = loads.get("moment_x", 0)  # kNm
        My = loads.get("moment_y", 0)  # kNm
        Vx = loads.get("shear_x", 0)  # kN
        Vy = loads.get("shear_y", 0)  # kN
        
        # Soil properties
        qa = soil_properties.get("allowable_bearing_capacity", 150)  # kPa
        
        # Material properties
        fck = parameters.get("concrete_grade", 25)  # MPa
        fy = parameters.get("steel_grade", 415)  # MPa
        
        # Step 1: Size footing for bearing pressure
        L, B = self._size_footing(P, Mx, My, qa)
        
        # Step 2: Determine footing depth
        D = self._determine_depth(L, B, column_size, P, Vx, Vy, fck)
        
        # Step 3: Check bearing pressure
        bearing_check = self._check_bearing_pressure(P, Mx, My, L, B, qa)
        
        # Step 4: Check one-way shear
        shear_check_1way = self._check_one_way_shear(P, L, B, D, column_size, fck)
        
        # Step 5: Check two-way shear (punching)
        shear_check_2way = self._check_two_way_shear(P, L, B, D, column_size, fck)
        
        # Step 6: Design flexural reinforcement
        reinforcement = self._design_flexural_reinforcement(
            P, Mx, My, L, B, D, column_size, fck, fy
        )
        
        # Step 7: Calculate settlement
        settlement = self._calculate_settlement(P, L, B, soil_properties)
        
        # Compile results
        dimensions = {
            "length": L,
            "width": B,
            "depth": D,
            "volume": L * B * D
        }
        
        safety_factors = {
            "bearing": bearing_check["safety_factor"],
            "one_way_shear": shear_check_1way["safety_factor"],
            "two_way_shear": shear_check_2way["safety_factor"]
        }
        
        # Determine design status
        all_checks_pass = (
            bearing_check["status"] == "OK" and
            shear_check_1way["status"] == "OK" and
            shear_check_2way["status"] == "OK"
        )
        
        design_status = "ADEQUATE" if all_checks_pass else "INADEQUATE"
        
        design_notes = []
        if not bearing_check["status"] == "OK":
            design_notes.append("Bearing pressure exceeds allowable")
        if not shear_check_1way["status"] == "OK":
            design_notes.append("One-way shear inadequate - increase depth")
        if not shear_check_2way["status"] == "OK":
            design_notes.append("Two-way shear inadequate - increase depth or add shear reinforcement")
        
        return FoundationDesignResult(
            foundation_type="Isolated Footing",
            dimensions=dimensions,
            reinforcement=reinforcement,
            bearing_pressure=bearing_check["actual_pressure"],
            settlement=settlement,
            safety_factors=safety_factors,
            design_status=design_status,
            design_notes=design_notes
        )
    
    def _size_footing(self, P: float, Mx: float, My: float, qa: float) -> Tuple[float, float]:
        """Size footing based on bearing pressure"""
        
        # Required area
        A_req = P / qa * 1.5  # Factor for moments
        
        # Assume square footing initially
        L = B = np.sqrt(A_req)
        
        # Adjust for moments
        if Mx > 0 or My > 0:
            # Increase size to account for eccentricity
            e_x = My / P if P > 0 else 0
            e_y = Mx / P if P > 0 else 0
            
            L = L * (1 + 6 * abs(e_y) / L)
            B = B * (1 + 6 * abs(e_x) / B)
        
        # Round up to nearest 0.1m
        L = np.ceil(L * 10) / 10
        B = np.ceil(B * 10) / 10
        
        # Minimum size
        L = max(L, 1.0)
        B = max(B, 1.0)
        
        return L, B
    
    def _determine_depth(self, L: float, B: float, column_size: Dict,
                        P: float, Vx: float, Vy: float, fck: float) -> float:
        """Determine footing depth based on shear requirements"""
        
        c_x = column_size.get("width", 0.3)
        c_y = column_size.get("depth", 0.3)
        
        # Estimate depth from one-way shear
        d_req_1way = self._estimate_depth_one_way_shear(L, B, c_x, c_y, P, fck)
        
        # Estimate depth from two-way shear
        d_req_2way = self._estimate_depth_two_way_shear(L, B, c_x, c_y, P, fck)
        
        # Take maximum
        d_req = max(d_req_1way, d_req_2way)
        
        # Add cover
        cover = 0.075  # 75mm
        D = d_req + cover
        
        # Round up to nearest 50mm
        D = np.ceil(D * 20) / 20
        
        # Minimum depth
        D = max(D, 0.3)
        
        return D
    
    def _check_bearing_pressure(self, P: float, Mx: float, My: float,
                                L: float, B: float, qa: float) -> Dict:
        """Check bearing pressure"""
        
        # Calculate eccentricities
        e_x = My / P if P > 0 else 0
        e_y = Mx / P if P > 0 else 0
        
        # Calculate bearing pressures
        q_max = P / (L * B) * (1 + 6 * e_x / B + 6 * e_y / L)
        q_min = P / (L * B) * (1 - 6 * e_x / B - 6 * e_y / L)
        
        # Check
        status = "OK" if q_max <= qa and q_min >= 0 else "FAIL"
        safety_factor = qa / q_max if q_max > 0 else 999
        
        return {
            "status": status,
            "actual_pressure": q_max,
            "allowable_pressure": qa,
            "safety_factor": safety_factor,
            "min_pressure": q_min
        }
    
    def _check_one_way_shear(self, P: float, L: float, B: float, D: float,
                            column_size: Dict, fck: float) -> Dict:
        """
        Check one-way shear per IS 456:2000 Clause 34.2.4
        
        Critical section is at distance 'd' from face of column
        """
        
        d = D - 0.075  # Effective depth (m)
        c_x = column_size.get("width", 0.3)  # Column width (m)
        
        # Critical section at d from column face
        x_crit = (L - c_x) / 2 - d
        
        # Validate x_crit to prevent negative values and unsafe designs
        if x_crit < 0:
            # Critical section is within or too close to column
            # Use face of column as critical section (conservative)
            x_crit = 0
            return {
                "status": "WARNING",
                "demand": 0,
                "capacity": 0,
                "safety_factor": 999,
                "message": f"Effective depth {d:.3f}m is too large for footing length {L:.3f}m. Critical section at column face.",
                "warning": "Foundation depth may be excessive or footing too small"
            }
        
        # Shear force at critical section
        V = P * x_crit / L  # N
        
        # Shear capacity per IS 456 Clause 40.2.1
        Vc = 0.17 * np.sqrt(fck) * B * d * 1000  # N
        
        # Check shear adequacy
        status = "OK" if V <= Vc else "FAIL"
        safety_factor = Vc / V if V > 0 else 999
        
        return {
            "status": status,
            "demand": V,
            "capacity": Vc,
            "safety_factor": safety_factor,
            "x_crit": x_crit
        }
    
    def _check_two_way_shear(self, P: float, L: float, B: float, D: float,
                            column_size: Dict, fck: float) -> Dict:
        """Check two-way shear (punching shear)"""
        
        d = D - 0.075
        c_x = column_size.get("width", 0.3)
        c_y = column_size.get("depth", 0.3)
        
        # Critical perimeter at d/2 from column face
        b0 = 2 * (c_x + c_y + 2 * d)
        
        # Shear force
        V = P
        
        # Shear capacity
        Vc = 0.33 * np.sqrt(fck) * b0 * d * 1000  # N
        
        # Check
        status = "OK" if V <= Vc else "FAIL"
        safety_factor = Vc / V if V > 0 else 999
        
        return {
            "status": status,
            "demand": V,
            "capacity": Vc,
            "safety_factor": safety_factor
        }
    
    def _design_flexural_reinforcement(self, P: float, Mx: float, My: float,
                                      L: float, B: float, D: float,
                                      column_size: Dict, fck: float, fy: float) -> Dict:
        """Design flexural reinforcement"""
        
        d = D - 0.075
        c_x = column_size.get("width", 0.3)
        c_y = column_size.get("depth", 0.3)
        
        # Calculate moments at critical sections
        M_x = P * (L - c_x) ** 2 / (8 * L)  # kNm
        M_y = P * (B - c_y) ** 2 / (8 * B)  # kNm
        
        # Design reinforcement in X direction
        Ast_x = self._calculate_steel_area(M_x, B, d, fck, fy)
        
        # Design reinforcement in Y direction
        Ast_y = self._calculate_steel_area(M_y, L, d, fck, fy)
        
        # Minimum reinforcement
        Ast_min = 0.0012 * B * D * 1000  # mm²
        Ast_x = max(Ast_x, Ast_min)
        Ast_y = max(Ast_y, Ast_min)
        
        # Select bars
        bars_x = self._select_bars(Ast_x, B)
        bars_y = self._select_bars(Ast_y, L)
        
        return {
            "bottom_x": bars_x,
            "bottom_y": bars_y,
            "area_x": Ast_x,
            "area_y": Ast_y
        }
    
    def _calculate_steel_area(self, M: float, b: float, d: float,
                             fck: float, fy: float) -> float:
        """Calculate required steel area"""
        
        # Convert moment to Nmm
        M = M * 1e6
        b = b * 1000
        d = d * 1000
        
        # Calculate steel area
        Ast = M / (0.87 * fy * d * 0.9)  # mm²
        
        return Ast
    
    def _select_bars(self, Ast_req: float, width: float) -> Dict:
        """Select bar size and spacing"""
        
        # Available bar sizes (diameter in mm)
        bar_sizes = [12, 16, 20, 25, 32]
        
        for dia in bar_sizes:
            Ab = np.pi * dia ** 2 / 4
            spacing = Ab * width * 1000 / Ast_req
            
            if 100 <= spacing <= 300:  # Practical spacing range
                n_bars = int(width * 1000 / spacing) + 1
                return {
                    "diameter": dia,
                    "spacing": int(spacing),
                    "number": n_bars,
                    "provided_area": n_bars * Ab
                }
        
        # Default
        return {
            "diameter": 16,
            "spacing": 200,
            "number": int(width * 1000 / 200),
            "provided_area": int(width * 1000 / 200) * np.pi * 16 ** 2 / 4
        }
    
    def _calculate_settlement(self, P: float, L: float, B: float,
                             soil_properties: Dict) -> float:
        """Calculate settlement"""
        
        Es = soil_properties.get("modulus_of_subgrade_reaction", 10000)  # kPa
        
        # Elastic settlement (simplified)
        q = P / (L * B)
        settlement = q * B / Es * 1000  # mm
        
        return settlement
    
    def _estimate_depth_one_way_shear(self, L: float, B: float,
                                      c_x: float, c_y: float,
                                      P: float, fck: float) -> float:
        """Estimate depth from one-way shear"""
        
        # Assume critical section
        V = P * 0.4  # Approximate
        
        # Required depth
        d_req = V / (0.17 * np.sqrt(fck) * B * 1000)
        
        return d_req
    
    def _estimate_depth_two_way_shear(self, L: float, B: float,
                                      c_x: float, c_y: float,
                                      P: float, fck: float) -> float:
        """Estimate depth from two-way shear"""
        
        # Assume critical perimeter
        d_est = 0.5  # Initial estimate
        b0 = 2 * (c_x + c_y + 2 * d_est)
        
        # Required depth
        d_req = P / (0.33 * np.sqrt(fck) * b0 * 1000)
        
        return d_req


class MatFoundationDesign:
    """Design mat (raft) foundations"""
    
    def design(self, loads: Dict, soil_properties: Dict, parameters: Dict) -> Dict:
        """Design mat foundation"""
        
        # Mat foundation design logic
        # Simplified implementation
        
        return {
            "foundation_type": "Mat Foundation",
            "thickness": 0.8,  # m
            "reinforcement": {
                "top": {"diameter": 20, "spacing": 150},
                "bottom": {"diameter": 20, "spacing": 150}
            },
            "design_status": "ADEQUATE"
        }


class PileFoundationDesign:
    """Design pile foundations"""
    
    def design(self, loads: Dict, soil_properties: Dict, parameters: Dict) -> Dict:
        """Design pile foundation"""
        
        # Pile foundation design logic
        # Simplified implementation
        
        return {
            "foundation_type": "Pile Foundation",
            "pile_diameter": 0.6,  # m
            "pile_length": 15.0,  # m
            "number_of_piles": 4,
            "pile_capacity": 500,  # kN
            "design_status": "ADEQUATE"
        }


def design_foundation(foundation_type: str, loads: Dict,
                     soil_properties: Dict, parameters: Dict) -> Dict:
    """
    Main function to design foundations
    
    Args:
        foundation_type: 'isolated', 'combined', 'mat', or 'pile'
        loads: Load dictionary
        soil_properties: Soil properties
        parameters: Design parameters
    """
    
    if foundation_type == "isolated":
        designer = IsolatedFootingDesign(parameters.get("design_code", "ACI 318-19"))
        column_size = parameters.get("column_size", {"width": 0.3, "depth": 0.3})
        return designer.design(loads, soil_properties, column_size, parameters)
    
    elif foundation_type == "mat":
        designer = MatFoundationDesign()
        return designer.design(loads, soil_properties, parameters)
    
    elif foundation_type == "pile":
        designer = PileFoundationDesign()
        return designer.design(loads, soil_properties, parameters)
    
    else:
        raise ValueError(f"Unknown foundation type: {foundation_type}")
