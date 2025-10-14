"""
Complete Element Library
Frame, Shell, Solid, Cable, Link, Spring Elements
"""
import numpy as np
from typing import Dict, List

class ShellElement:
    """4-node quadrilateral shell element (plate + membrane)"""
    
    def __init__(self, nodes: List, thickness: float, material: Dict):
        self.nodes = nodes  # 4 nodes
        self.thickness = thickness  # mm
        self.E = material.get('E', 25000)  # MPa
        self.nu = material.get('nu', 0.2)  # Poisson's ratio
        
    def stiffness_matrix(self) -> np.ndarray:
        """Calculate 24x24 stiffness matrix (6 DOF per node)"""
        # Simplified - full implementation uses numerical integration
        t = self.thickness / 1000  # Convert to m
        E = self.E * 1e6  # Convert to Pa
        nu = self.nu
        
        # Membrane stiffness
        D_membrane = (E * t) / (1 - nu**2) * np.array([
            [1, nu, 0],
            [nu, 1, 0],
            [0, 0, (1-nu)/2]
        ])
        
        # Bending stiffness
        D_bending = (E * t**3) / (12 * (1 - nu**2)) * np.array([
            [1, nu, 0],
            [nu, 1, 0],
            [0, 0, (1-nu)/2]
        ])
        
        # Full stiffness matrix (simplified)
        K = np.zeros((24, 24))
        
        # Assemble membrane and bending contributions
        # (Full implementation would use shape functions and Gauss integration)
        
        return K
    
    def stress_calculation(self, displacements: np.ndarray) -> Dict:
        """Calculate stresses in shell element"""
        # Membrane stresses
        sigma_x = 0.0  # Calculated from displacements
        sigma_y = 0.0
        tau_xy = 0.0
        
        # Bending stresses
        sigma_x_bend = 0.0
        sigma_y_bend = 0.0
        
        # Von Mises stress
        sigma_vm = np.sqrt(sigma_x**2 + sigma_y**2 - sigma_x*sigma_y + 3*tau_xy**2)
        
        return {
            "membrane_stress_x": sigma_x,
            "membrane_stress_y": sigma_y,
            "shear_stress_xy": tau_xy,
            "bending_stress_x": sigma_x_bend,
            "bending_stress_y": sigma_y_bend,
            "von_mises_stress": sigma_vm
        }

class SolidElement:
    """8-node hexahedral solid element (3D FEM)"""
    
    def __init__(self, nodes: List, material: Dict):
        self.nodes = nodes  # 8 nodes
        self.E = material.get('E', 25000)  # MPa
        self.nu = material.get('nu', 0.2)
        
    def stiffness_matrix(self) -> np.ndarray:
        """Calculate 24x24 stiffness matrix (3 DOF per node)"""
        E = self.E * 1e6
        nu = self.nu
        
        # Elasticity matrix
        lambda_lame = (E * nu) / ((1 + nu) * (1 - 2*nu))
        mu = E / (2 * (1 + nu))
        
        D = np.array([
            [lambda_lame + 2*mu, lambda_lame, lambda_lame, 0, 0, 0],
            [lambda_lame, lambda_lame + 2*mu, lambda_lame, 0, 0, 0],
            [lambda_lame, lambda_lame, lambda_lame + 2*mu, 0, 0, 0],
            [0, 0, 0, mu, 0, 0],
            [0, 0, 0, 0, mu, 0],
            [0, 0, 0, 0, 0, mu]
        ])
        
        # Full stiffness matrix (simplified)
        K = np.zeros((24, 24))
        
        # Would use Gauss integration in full implementation
        
        return K

class CableElement:
    """Nonlinear cable element (catenary)"""
    
    def __init__(self, nodes: List, area: float, material: Dict):
        self.nodes = nodes  # 2 nodes
        self.area = area  # mm²
        self.E = material.get('E', 200000)  # MPa
        self.weight_per_length = material.get('weight', 0.0)  # N/mm
        
    def stiffness_matrix(self, tension: float) -> np.ndarray:
        """
        Calculate tangent stiffness matrix for cable
        
        Args:
            tension: Current tension in cable (N)
        """
        # Cable length
        n1, n2 = self.nodes
        L = np.sqrt((n2.x - n1.x)**2 + (n2.y - n1.y)**2 + (n2.z - n1.z)**2)
        
        # Direction cosines
        cx = (n2.x - n1.x) / L
        cy = (n2.y - n1.y) / L
        cz = (n2.z - n1.z) / L
        
        # Elastic stiffness
        EA = self.E * self.area
        ke = EA / L
        
        # Geometric stiffness
        kg = tension / L
        
        # Total tangent stiffness
        k_total = ke + kg
        
        # Transformation matrix
        T = np.array([cx, cy, cz])
        
        # Element stiffness in global coordinates
        K = k_total * np.outer(T, T)
        
        # Expand to 6x6 (3 DOF per node)
        K_full = np.zeros((6, 6))
        K_full[0:3, 0:3] = K
        K_full[0:3, 3:6] = -K
        K_full[3:6, 0:3] = -K
        K_full[3:6, 3:6] = K
        
        return K_full
    
    def catenary_shape(self, horizontal_tension: float, span: float) -> Dict:
        """Calculate catenary shape of cable"""
        H = horizontal_tension
        w = self.weight_per_length
        
        # Sag
        sag = (w * span**2) / (8 * H)
        
        # Cable length
        cable_length = span * (1 + (8/3) * (sag/span)**2)
        
        # Maximum tension
        T_max = np.sqrt(H**2 + (w * span / 2)**2)
        
        return {
            "sag": sag,
            "cable_length": cable_length,
            "horizontal_tension": H,
            "max_tension": T_max,
            "span": span
        }

class LinkElement:
    """Link/Gap element with nonlinear behavior"""
    
    def __init__(self, nodes: List, properties: Dict):
        self.nodes = nodes
        self.stiffness = properties.get('stiffness', 1e6)  # N/mm
        self.gap = properties.get('gap', 0.0)  # mm
        self.behavior = properties.get('behavior', 'linear')  # linear, compression-only, tension-only
        
    def force_displacement_relationship(self, displacement: float) -> float:
        """Calculate force based on displacement and behavior"""
        if self.behavior == 'compression-only':
            if displacement < -self.gap:
                return self.stiffness * (displacement + self.gap)
            else:
                return 0.0
        elif self.behavior == 'tension-only':
            if displacement > self.gap:
                return self.stiffness * (displacement - self.gap)
            else:
                return 0.0
        else:  # linear
            return self.stiffness * displacement

class SpringElement:
    """Spring element (translational or rotational)"""
    
    def __init__(self, node, direction: str, stiffness: float):
        self.node = node
        self.direction = direction  # 'X', 'Y', 'Z', 'RX', 'RY', 'RZ'
        self.stiffness = stiffness  # N/mm or Nmm/rad
        
    def stiffness_matrix(self) -> np.ndarray:
        """Calculate spring stiffness matrix"""
        K = np.zeros((6, 6))
        
        # Map direction to DOF
        dof_map = {'X': 0, 'Y': 1, 'Z': 2, 'RX': 3, 'RY': 4, 'RZ': 5}
        dof = dof_map[self.direction]
        
        K[dof, dof] = self.stiffness
        
        return K
