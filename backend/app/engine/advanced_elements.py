"""
Advanced Element Types
Shell elements, solid elements, and special elements
"""
import numpy as np
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


class ShellElement:
    """4-node quadrilateral shell element (24 DOF)"""
    
    def __init__(self, nodes: List, thickness: float, material_props: Dict):
        """
        Initialize shell element
        
        Args:
            nodes: List of 4 nodes
            thickness: Shell thickness (mm)
            material_props: Material properties (E, nu, density)
        """
        self.nodes = nodes
        self.thickness = thickness
        self.E = material_props.get('E', 200000)
        self.nu = material_props.get('nu', 0.3)
        self.density = material_props.get('density', 7850)
        
    def stiffness_matrix(self) -> np.ndarray:
        """
        Calculate 24x24 stiffness matrix
        
        Combines membrane and plate bending behavior
        """
        # Membrane stiffness (in-plane)
        K_membrane = self._membrane_stiffness()
        
        # Plate bending stiffness (out-of-plane)
        K_bending = self._bending_stiffness()
        
        # Combine
        K = np.zeros((24, 24))
        
        # Membrane DOF: ux, uy (indices 0,1,6,7,12,13,18,19)
        membrane_dof = [0,1, 6,7, 12,13, 18,19]
        for i, dof_i in enumerate(membrane_dof):
            for j, dof_j in enumerate(membrane_dof):
                K[dof_i, dof_j] = K_membrane[i, j]
        
        # Bending DOF: uz, rx, ry (indices 2,3,4, 8,9,10, 14,15,16, 20,21,22)
        bending_dof = [2,3,4, 8,9,10, 14,15,16, 20,21,22]
        for i, dof_i in enumerate(bending_dof):
            for j, dof_j in enumerate(bending_dof):
                K[dof_i, dof_j] = K_bending[i, j]
        
        return K
    
    def _membrane_stiffness(self) -> np.ndarray:
        """Calculate membrane stiffness (8x8)"""
        # Simplified - constant strain triangle approach
        # In production, use numerical integration (Gauss quadrature)
        
        # Material matrix for plane stress
        D = (self.E / (1 - self.nu**2)) * np.array([
            [1, self.nu, 0],
            [self.nu, 1, 0],
            [0, 0, (1-self.nu)/2]
        ])
        
        # Element area (approximate)
        area = self._calculate_area()
        
        # Simplified stiffness
        K_m = np.zeros((8, 8))
        factor = self.E * self.thickness * area / (1 - self.nu**2)
        
        # Diagonal terms (simplified)
        for i in range(8):
            K_m[i, i] = factor * 0.5
        
        return K_m
    
    def _bending_stiffness(self) -> np.ndarray:
        """Calculate bending stiffness (12x12)"""
        # Plate bending stiffness
        D = (self.E * self.thickness**3) / (12 * (1 - self.nu**2))
        
        # Simplified stiffness
        K_b = np.zeros((12, 12))
        area = self._calculate_area()
        
        # Diagonal terms (simplified)
        for i in range(12):
            K_b[i, i] = D * area * 0.1
        
        return K_b
    
    def _calculate_area(self) -> float:
        """Calculate element area"""
        # Approximate as two triangles
        n1, n2, n3, n4 = self.nodes
        
        # Triangle 1-2-3
        v1 = np.array([n2.x - n1.x, n2.y - n1.y, n2.z - n1.z])
        v2 = np.array([n3.x - n1.x, n3.y - n1.y, n3.z - n1.z])
        area1 = 0.5 * np.linalg.norm(np.cross(v1, v2))
        
        # Triangle 1-3-4
        v3 = np.array([n4.x - n1.x, n4.y - n1.y, n4.z - n1.z])
        area2 = 0.5 * np.linalg.norm(np.cross(v2, v3))
        
        return area1 + area2


class SolidElement:
    """8-node hexahedral solid element (24 DOF)"""
    
    def __init__(self, nodes: List, material_props: Dict):
        """
        Initialize solid element
        
        Args:
            nodes: List of 8 nodes
            material_props: Material properties
        """
        self.nodes = nodes
        self.E = material_props.get('E', 200000)
        self.nu = material_props.get('nu', 0.3)
        self.density = material_props.get('density', 7850)
    
    def stiffness_matrix(self) -> np.ndarray:
        """
        Calculate 24x24 stiffness matrix using numerical integration
        """
        # Material matrix for 3D elasticity
        D = self._material_matrix_3d()
        
        # Initialize stiffness
        K = np.zeros((24, 24))
        
        # Gauss integration points (2x2x2)
        gauss_points = [-1/np.sqrt(3), 1/np.sqrt(3)]
        
        for xi in gauss_points:
            for eta in gauss_points:
                for zeta in gauss_points:
                    # Shape function derivatives
                    dN, J = self._shape_derivatives(xi, eta, zeta)
                    
                    # B matrix (strain-displacement)
                    B = self._b_matrix(dN)
                    
                    # Stiffness contribution
                    det_J = np.linalg.det(J)
                    K += B.T @ D @ B * det_J
        
        return K
    
    def _material_matrix_3d(self) -> np.ndarray:
        """3D elasticity matrix (6x6)"""
        E = self.E
        nu = self.nu
        
        factor = E / ((1 + nu) * (1 - 2*nu))
        
        D = factor * np.array([
            [1-nu, nu, nu, 0, 0, 0],
            [nu, 1-nu, nu, 0, 0, 0],
            [nu, nu, 1-nu, 0, 0, 0],
            [0, 0, 0, (1-2*nu)/2, 0, 0],
            [0, 0, 0, 0, (1-2*nu)/2, 0],
            [0, 0, 0, 0, 0, (1-2*nu)/2]
        ])
        
        return D
    
    def _shape_derivatives(self, xi: float, eta: float, zeta: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate shape function derivatives and Jacobian for 8-node hexahedral element
        
        Node numbering (standard):
        Bottom face (zeta = -1): 1,2,3,4
        Top face (zeta = +1): 5,6,7,8
        
        Args:
            xi, eta, zeta: Natural coordinates (-1 to +1)
            
        Returns:
            dN_dxyz: Shape function derivatives w.r.t. global coordinates (3x8)
            J: Jacobian matrix (3x3)
        """
        # Shape function derivatives w.r.t. natural coordinates
        # dN/dxi, dN/deta, dN/dzeta for each of 8 nodes
        dN_dxi = np.array([
            -(1-eta)*(1-zeta)/8,  # Node 1
             (1-eta)*(1-zeta)/8,  # Node 2
             (1+eta)*(1-zeta)/8,  # Node 3
            -(1+eta)*(1-zeta)/8,  # Node 4
            -(1-eta)*(1+zeta)/8,  # Node 5
             (1-eta)*(1+zeta)/8,  # Node 6
             (1+eta)*(1+zeta)/8,  # Node 7
            -(1+eta)*(1+zeta)/8   # Node 8
        ])
        
        dN_deta = np.array([
            -(1-xi)*(1-zeta)/8,   # Node 1
            -(1+xi)*(1-zeta)/8,   # Node 2
             (1+xi)*(1-zeta)/8,   # Node 3
             (1-xi)*(1-zeta)/8,   # Node 4
            -(1-xi)*(1+zeta)/8,   # Node 5
            -(1+xi)*(1+zeta)/8,   # Node 6
             (1+xi)*(1+zeta)/8,   # Node 7
             (1-xi)*(1+zeta)/8    # Node 8
        ])
        
        dN_dzeta = np.array([
            -(1-xi)*(1-eta)/8,    # Node 1
            -(1+xi)*(1-eta)/8,    # Node 2
            -(1+xi)*(1+eta)/8,    # Node 3
            -(1-xi)*(1+eta)/8,    # Node 4
             (1-xi)*(1-eta)/8,    # Node 5
             (1+xi)*(1-eta)/8,    # Node 6
             (1+xi)*(1+eta)/8,    # Node 7
             (1-xi)*(1+eta)/8     # Node 8
        ])
        
        # Assemble derivatives matrix (3x8)
        dN_dnat = np.array([dN_dxi, dN_deta, dN_dzeta])
        
        # Get nodal coordinates
        coords = np.zeros((8, 3))
        for i, node in enumerate(self.nodes):
            coords[i] = [node.x, node.y, node.z]
        
        # Calculate Jacobian matrix: J = dN/dnat * coords
        # J[i,j] = sum over nodes of (dN_i/dnat_j * coord_i)
        J = dN_dnat @ coords  # (3x8) @ (8x3) = (3x3)
        
        # Invert Jacobian
        try:
            J_inv = np.linalg.inv(J)
        except np.linalg.LinAlgError:
            logger.warning("Singular Jacobian detected, using pseudo-inverse")
            J_inv = np.linalg.pinv(J)
        
        # Calculate derivatives w.r.t. global coordinates
        # dN/dx = J^-1 * dN/dnat
        dN_dxyz = J_inv @ dN_dnat  # (3x3) @ (3x8) = (3x8)
        
        return dN_dxyz, J
    
    def _b_matrix(self, dN_dxyz: np.ndarray) -> np.ndarray:
        """
        Calculate strain-displacement matrix (B-matrix) for 8-node hexahedral element
        
        Relates nodal displacements to strains:
        {strain} = [B] {displacement}
        
        where:
        {strain} = {εxx, εyy, εzz, γxy, γyz, γzx}^T  (6x1)
        {displacement} = {u1,v1,w1, u2,v2,w2, ..., u8,v8,w8}^T  (24x1)
        
        Args:
            dN_dxyz: Shape function derivatives w.r.t. global coords (3x8)
                     [dN/dx; dN/dy; dN/dz]
        
        Returns:
            B: Strain-displacement matrix (6x24)
        """
        B = np.zeros((6, 24))
        
        # Extract derivatives for convenience
        dN_dx = dN_dxyz[0, :]  # (8,)
        dN_dy = dN_dxyz[1, :]  # (8,)
        dN_dz = dN_dxyz[2, :]  # (8,)
        
        # Fill B-matrix for each node
        for i in range(8):
            # Columns for node i: 3*i, 3*i+1, 3*i+2 (u, v, w)
            col_u = 3 * i
            col_v = 3 * i + 1
            col_w = 3 * i + 2
            
            # Normal strains
            # εxx = du/dx
            B[0, col_u] = dN_dx[i]
            
            # εyy = dv/dy
            B[1, col_v] = dN_dy[i]
            
            # εzz = dw/dz
            B[2, col_w] = dN_dz[i]
            
            # Shear strains (engineering shear strain = 2 * tensor shear strain)
            # γxy = du/dy + dv/dx
            B[3, col_u] = dN_dy[i]
            B[3, col_v] = dN_dx[i]
            
            # γyz = dv/dz + dw/dy
            B[4, col_v] = dN_dz[i]
            B[4, col_w] = dN_dy[i]
            
            # γzx = dw/dx + du/dz
            B[5, col_w] = dN_dx[i]
            B[5, col_u] = dN_dz[i]
        
        return B


class SpringElement:
    """Spring element for boundary conditions"""
    
    def __init__(self, node_id: int, direction: str, stiffness: float):
        """
        Initialize spring element
        
        Args:
            node_id: Node ID
            direction: Direction ('x', 'y', 'z', 'rx', 'ry', 'rz')
            stiffness: Spring stiffness
        """
        self.node_id = node_id
        self.direction = direction
        self.stiffness = stiffness
    
    def stiffness_matrix(self) -> np.ndarray:
        """1x1 stiffness matrix"""
        return np.array([[self.stiffness]])


class RigidElement:
    """Rigid element for diaphragm modeling"""
    
    def __init__(self, master_node: int, slave_nodes: List[int]):
        """
        Initialize rigid element
        
        Args:
            master_node: Master node ID
            slave_nodes: List of slave node IDs
        """
        self.master_node = master_node
        self.slave_nodes = slave_nodes
    
    def constraint_equations(self) -> List[Dict]:
        """
        Generate constraint equations
        
        Returns:
            List of constraint equations
        """
        constraints = []
        
        for slave in self.slave_nodes:
            # Slave DOF = Master DOF (rigid connection)
            for dof in range(6):
                constraints.append({
                    'slave_node': slave,
                    'slave_dof': dof,
                    'master_node': self.master_node,
                    'master_dof': dof,
                    'coefficient': 1.0
                })
        
        return constraints


# Helper functions
def create_shell_mesh(width: float, height: float, nx: int, ny: int) -> Dict:
    """
    Create shell element mesh
    
    Args:
        width: Width (mm)
        height: Height (mm)
        nx: Number of elements in x
        ny: Number of elements in y
    
    Returns:
        Dict with nodes and elements
    """
    nodes = []
    elements = []
    
    # Generate nodes
    node_id = 0
    for j in range(ny + 1):
        for i in range(nx + 1):
            x = i * width / nx
            y = j * height / ny
            z = 0.0
            nodes.append({'id': node_id, 'x': x, 'y': y, 'z': z})
            node_id += 1
    
    # Generate elements
    elem_id = 0
    for j in range(ny):
        for i in range(nx):
            n1 = j * (nx + 1) + i
            n2 = n1 + 1
            n3 = n1 + (nx + 1) + 1
            n4 = n1 + (nx + 1)
            
            elements.append({
                'id': elem_id,
                'nodes': [n1, n2, n3, n4],
                'type': 'shell'
            })
            elem_id += 1
    
    return {'nodes': nodes, 'elements': elements}
