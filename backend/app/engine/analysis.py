import numpy as np
from scipy.linalg import lu_factor, lu_solve
from scipy.sparse.linalg import eigs

class StructuralAnalysis:
    def __init__(self, geometry_engine):
        self.geometry = geometry_engine
        self.K_global = None
        self.displacements = None
        self.element_forces = {}
        
    def assemble_stiffness_matrix(self, material_props, section_props):
        """Assemble global stiffness matrix with proper transformation"""
        n_dof = len(self.geometry.nodes) * 6
        K = np.zeros((n_dof, n_dof))
        
        for elem_id, elem in self.geometry.elements.items():
            # Get element properties
            mat = material_props.get(elem_id, material_props.get('default', {}))
            sec = section_props.get(elem_id, section_props.get('default', {}))
            
            # Calculate local stiffness matrix
            k_local = self._element_stiffness_3d(elem, mat, sec)
            
            # Get transformation matrix
            T = self._transformation_matrix_3d(elem)
            
            # Transform to global coordinates
            k_global = T.T @ k_local @ T
            
            # Assemble into global matrix
            dof_indices = self._get_element_dof_indices(elem)
            for i, dof_i in enumerate(dof_indices):
                for j, dof_j in enumerate(dof_indices):
                    K[dof_i, dof_j] += k_global[i, j]
            
        self.K_global = K
        return K
    
    def _element_stiffness_3d(self, element, material_props, section_props):
        """
        Calculate 3D beam element stiffness matrix (12x12)
        
        DOF per node: [ux, uy, uz, rx, ry, rz]
        Total DOF: 12 (2 nodes × 6 DOF)
        
        Includes:
        - Axial deformation
        - Bending in two planes
        - Torsion
        - Shear deformation (optional)
        """
        # Material properties
        E = material_props.get('E', 200000)  # MPa (steel default)
        G = material_props.get('G', E / (2 * (1 + 0.3)))  # Shear modulus
        
        # Section properties
        A = section_props.get('A', 10000)    # mm²
        Iy = section_props.get('Iy', 1e7)    # mm⁴ (about z-axis)
        Iz = section_props.get('Iz', 1e7)    # mm⁴ (about y-axis)
        J = section_props.get('J', 1e6)      # mm⁴ (torsion constant)
        
        # Element length
        L = element.length()
        
        if L < 1e-6:
            raise ValueError(f"Element {element.id} has zero length")
        
        # Initialize stiffness matrix
        k = np.zeros((12, 12))
        
        # Axial stiffness (DOF 1, 7)
        EA_L = E * A / L
        k[0, 0] = EA_L
        k[0, 6] = -EA_L
        k[6, 0] = -EA_L
        k[6, 6] = EA_L
        
        # Torsional stiffness (DOF 4, 10)
        GJ_L = G * J / L
        k[3, 3] = GJ_L
        k[3, 9] = -GJ_L
        k[9, 3] = -GJ_L
        k[9, 9] = GJ_L
        
        # Bending about z-axis (in xy-plane)
        # DOF: uy (2, 8), rz (6, 12)
        EIz_L3 = E * Iz / (L ** 3)
        k[1, 1] = 12 * EIz_L3
        k[1, 5] = 6 * EIz_L3 * L
        k[1, 7] = -12 * EIz_L3
        k[1, 11] = 6 * EIz_L3 * L
        
        k[5, 1] = 6 * EIz_L3 * L
        k[5, 5] = 4 * EIz_L3 * L * L
        k[5, 7] = -6 * EIz_L3 * L
        k[5, 11] = 2 * EIz_L3 * L * L
        
        k[7, 1] = -12 * EIz_L3
        k[7, 5] = -6 * EIz_L3 * L
        k[7, 7] = 12 * EIz_L3
        k[7, 11] = -6 * EIz_L3 * L
        
        k[11, 1] = 6 * EIz_L3 * L
        k[11, 5] = 2 * EIz_L3 * L * L
        k[11, 7] = -6 * EIz_L3 * L
        k[11, 11] = 4 * EIz_L3 * L * L
        
        # Bending about y-axis (in xz-plane)
        # DOF: uz (3, 9), ry (5, 11)
        EIy_L3 = E * Iy / (L ** 3)
        k[2, 2] = 12 * EIy_L3
        k[2, 4] = -6 * EIy_L3 * L
        k[2, 8] = -12 * EIy_L3
        k[2, 10] = -6 * EIy_L3 * L
        
        k[4, 2] = -6 * EIy_L3 * L
        k[4, 4] = 4 * EIy_L3 * L * L
        k[4, 8] = 6 * EIy_L3 * L
        k[4, 10] = 2 * EIy_L3 * L * L
        
        k[8, 2] = -12 * EIy_L3
        k[8, 4] = 6 * EIy_L3 * L
        k[8, 8] = 12 * EIy_L3
        k[8, 10] = 6 * EIy_L3 * L
        
        k[10, 2] = -6 * EIy_L3 * L
        k[10, 4] = 2 * EIy_L3 * L * L
        k[10, 8] = 6 * EIy_L3 * L
        k[10, 10] = 4 * EIy_L3 * L * L
        
        return k
    
    def _transformation_matrix_3d(self, element):
        """
        Calculate 3D transformation matrix from local to global coordinates
        
        Returns 12x12 transformation matrix
        """
        if len(element.nodes) != 2:
            raise ValueError("Transformation only implemented for 2-node elements")
        
        n1, n2 = element.nodes
        
        # Element vector
        dx = n2.x - n1.x
        dy = n2.y - n1.y
        dz = n2.z - n1.z
        L = np.sqrt(dx**2 + dy**2 + dz**2)
        
        if L < 1e-6:
            raise ValueError(f"Element {element.id} has zero length")
        
        # Direction cosines of local x-axis (along element)
        cx = dx / L
        cy = dy / L
        cz = dz / L
        
        # Local y-axis (perpendicular to element)
        # Choose based on element orientation
        if abs(cz) > 0.9:  # Nearly vertical element
            # Use global x-axis as reference
            v = np.array([1.0, 0.0, 0.0])
        else:
            # Use global z-axis as reference
            v = np.array([0.0, 0.0, 1.0])
        
        # Local x-axis
        x_local = np.array([cx, cy, cz])
        
        # Local y-axis (perpendicular to x and v)
        y_local = np.cross(x_local, v)
        y_local = y_local / np.linalg.norm(y_local)
        
        # Local z-axis (perpendicular to x and y)
        z_local = np.cross(x_local, y_local)
        
        # 3x3 rotation matrix
        R = np.array([
            [x_local[0], y_local[0], z_local[0]],
            [x_local[1], y_local[1], z_local[1]],
            [x_local[2], y_local[2], z_local[2]]
        ])
        
        # 12x12 transformation matrix (block diagonal)
        T = np.zeros((12, 12))
        T[0:3, 0:3] = R
        T[3:6, 3:6] = R
        T[6:9, 6:9] = R
        T[9:12, 9:12] = R
        
        return T
    
    def _get_element_dof_indices(self, element):
        """Get global DOF indices for element"""
        dof_indices = []
        for node in element.nodes:
            node_id = node.id
            # 6 DOF per node: [ux, uy, uz, rx, ry, rz]
            for i in range(6):
                dof_indices.append(node_id * 6 + i)
        return dof_indices
    
    def apply_boundary_conditions(self, restraints):
        """
        Apply boundary conditions by modifying stiffness matrix
        
        Args:
            restraints: Dict of {node_id: [ux, uy, uz, rx, ry, rz]}
                       True = restrained, False = free
        """
        if self.K_global is None:
            raise ValueError("Stiffness matrix not assembled")
        
        # Identify restrained DOFs
        restrained_dofs = []
        for node_id, dof_restraints in restraints.items():
            for i, is_restrained in enumerate(dof_restraints):
                if is_restrained:
                    restrained_dofs.append(node_id * 6 + i)
        
        # Create reduced system (remove restrained DOFs)
        n_dof = self.K_global.shape[0]
        free_dofs = [i for i in range(n_dof) if i not in restrained_dofs]
        
        self.free_dofs = free_dofs
        self.restrained_dofs = restrained_dofs
        
        # Extract reduced stiffness matrix
        K_reduced = self.K_global[np.ix_(free_dofs, free_dofs)]
        
        return K_reduced
    
    def static_analysis(self, loads, restraints):
        """
        Perform static analysis using LU decomposition
        
        Args:
            loads: Load vector (full size)
            restraints: Boundary conditions
        """
        if self.K_global is None:
            raise ValueError("Stiffness matrix not assembled")
        
        # Apply boundary conditions
        K_reduced = self.apply_boundary_conditions(restraints)
        
        # Extract free DOF loads
        F = np.array(loads)
        F_reduced = F[self.free_dofs]
        
        # Solve reduced system
        lu, piv = lu_factor(K_reduced)
        u_reduced = lu_solve((lu, piv), F_reduced)
        
        # Expand to full displacement vector
        n_dof = self.K_global.shape[0]
        self.displacements = np.zeros(n_dof)
        self.displacements[self.free_dofs] = u_reduced
        
        # Calculate reactions at supports
        reactions = self.K_global @ self.displacements - F
        
        # Calculate element forces
        self._calculate_element_forces()
        
        return {
            "displacements": self.displacements,
            "reactions": reactions,
            "element_forces": self.element_forces
        }
    
    def _calculate_element_forces(self):
        """Calculate internal forces in each element"""
        for elem_id, elem in self.geometry.elements.items():
            # Get element displacements
            dof_indices = self._get_element_dof_indices(elem)
            u_global = self.displacements[dof_indices]
            
            # Transform to local coordinates
            T = self._transformation_matrix_3d(elem)
            u_local = T @ u_global
            
            # Get local stiffness
            mat = {'E': 200000, 'G': 80000}  # Default
            sec = {'A': 10000, 'Iy': 1e7, 'Iz': 1e7, 'J': 1e6}  # Default
            k_local = self._element_stiffness_3d(elem, mat, sec)
            
            # Calculate local forces
            f_local = k_local @ u_local
            
            # Extract member forces
            # Node 1 forces
            N1 = f_local[0]      # Axial
            Vy1 = f_local[1]     # Shear y
            Vz1 = f_local[2]     # Shear z
            T1 = f_local[3]      # Torsion
            My1 = f_local[4]     # Moment about y
            Mz1 = f_local[5]     # Moment about z
            
            # Node 2 forces
            N2 = f_local[6]
            Vy2 = f_local[7]
            Vz2 = f_local[8]
            T2 = f_local[9]
            My2 = f_local[10]
            Mz2 = f_local[11]
            
            self.element_forces[elem_id] = {
                "node_1": {
                    "axial": N1,
                    "shear_y": Vy1,
                    "shear_z": Vz1,
                    "torsion": T1,
                    "moment_y": My1,
                    "moment_z": Mz1
                },
                "node_2": {
                    "axial": N2,
                    "shear_y": Vy2,
                    "shear_z": Vz2,
                    "torsion": T2,
                    "moment_y": My2,
                    "moment_z": Mz2
                }
            }
    
    def assemble_mass_matrix(self, material_props, section_props):
        """
        Assemble consistent mass matrix
        
        Uses consistent mass formulation (not lumped)
        """
        n_dof = len(self.geometry.nodes) * 6
        M = np.zeros((n_dof, n_dof))
        
        for elem_id, elem in self.geometry.elements.items():
            # Get element properties
            mat = material_props.get(elem_id, material_props.get('default', {}))
            sec = section_props.get(elem_id, section_props.get('default', {}))
            
            # Calculate local mass matrix
            m_local = self._element_mass_matrix_3d(elem, mat, sec)
            
            # Get transformation matrix
            T = self._transformation_matrix_3d(elem)
            
            # Transform to global coordinates
            m_global = T.T @ m_local @ T
            
            # Assemble into global matrix
            dof_indices = self._get_element_dof_indices(elem)
            for i, dof_i in enumerate(dof_indices):
                for j, dof_j in enumerate(dof_indices):
                    M[dof_i, dof_j] += m_global[i, j]
        
        return M
    
    def _element_mass_matrix_3d(self, element, material_props, section_props):
        """
        Calculate consistent mass matrix for 3D beam element
        
        Includes translational and rotational inertia
        """
        # Material properties
        rho = material_props.get('density', 7850)  # kg/m³ (steel default)
        
        # Section properties
        A = section_props.get('A', 10000) / 1e6  # Convert mm² to m²
        Iy = section_props.get('Iy', 1e7) / 1e12  # Convert mm⁴ to m⁴
        Iz = section_props.get('Iz', 1e7) / 1e12
        J = section_props.get('J', 1e6) / 1e12
        
        # Element length
        L = element.length() / 1000  # Convert mm to m
        
        # Mass per unit length
        m = rho * A
        
        # Rotational inertia per unit length
        Ip = rho * J  # Polar moment
        Iy_mass = rho * Iy
        Iz_mass = rho * Iz
        
        # Consistent mass matrix (12x12)
        M = np.zeros((12, 12))
        
        # Axial mass (DOF 1, 7)
        M[0, 0] = (m * L) / 3
        M[0, 6] = (m * L) / 6
        M[6, 0] = (m * L) / 6
        M[6, 6] = (m * L) / 3
        
        # Transverse mass in y-direction (DOF 2, 8)
        M[1, 1] = (13 * m * L) / 35
        M[1, 5] = (11 * m * L**2) / 210
        M[1, 7] = (9 * m * L) / 70
        M[1, 11] = -(13 * m * L**2) / 420
        
        M[5, 1] = (11 * m * L**2) / 210
        M[5, 5] = (m * L**3) / 105
        M[5, 7] = (13 * m * L**2) / 420
        M[5, 11] = -(m * L**3) / 140
        
        M[7, 1] = (9 * m * L) / 70
        M[7, 5] = (13 * m * L**2) / 420
        M[7, 7] = (13 * m * L) / 35
        M[7, 11] = -(11 * m * L**2) / 210
        
        M[11, 1] = -(13 * m * L**2) / 420
        M[11, 5] = -(m * L**3) / 140
        M[11, 7] = -(11 * m * L**2) / 210
        M[11, 11] = (m * L**3) / 105
        
        # Transverse mass in z-direction (DOF 3, 9)
        M[2, 2] = (13 * m * L) / 35
        M[2, 4] = -(11 * m * L**2) / 210
        M[2, 8] = (9 * m * L) / 70
        M[2, 10] = (13 * m * L**2) / 420
        
        M[4, 2] = -(11 * m * L**2) / 210
        M[4, 4] = (m * L**3) / 105
        M[4, 8] = -(13 * m * L**2) / 420
        M[4, 10] = -(m * L**3) / 140
        
        M[8, 2] = (9 * m * L) / 70
        M[8, 4] = -(13 * m * L**2) / 420
        M[8, 8] = (13 * m * L) / 35
        M[8, 10] = (11 * m * L**2) / 210
        
        M[10, 2] = (13 * m * L**2) / 420
        M[10, 4] = -(m * L**3) / 140
        M[10, 8] = (11 * m * L**2) / 210
        M[10, 10] = (m * L**3) / 105
        
        # Torsional mass (DOF 4, 10)
        M[3, 3] = (Ip * L) / 3
        M[3, 9] = (Ip * L) / 6
        M[9, 3] = (Ip * L) / 6
        M[9, 9] = (Ip * L) / 3
        
        return M
    
    def modal_analysis(self, material_props, section_props, restraints, n_modes=10):
        """
        Extract natural frequencies and mode shapes
        
        Solves: K * phi = omega^2 * M * phi
        """
        if self.K_global is None:
            raise ValueError("Stiffness matrix not assembled")
        
        # Assemble mass matrix
        M_global = self.assemble_mass_matrix(material_props, section_props)
        
        # Apply boundary conditions
        K_reduced = self.apply_boundary_conditions(restraints)
        M_reduced = M_global[np.ix_(self.free_dofs, self.free_dofs)]
        
        # Solve eigenvalue problem
        from scipy.linalg import eigh
        eigenvalues, eigenvectors = eigh(K_reduced, M_reduced)
        
        # Sort by eigenvalue
        idx = np.argsort(eigenvalues)
        eigenvalues = eigenvalues[idx[:n_modes]]
        eigenvectors = eigenvectors[:, idx[:n_modes]]
        
        # Calculate frequencies
        omega = np.sqrt(np.abs(eigenvalues))
        frequencies = omega / (2 * np.pi)  # Hz
        periods = 1 / frequencies  # seconds
        
        # Expand mode shapes to full DOF
        mode_shapes_full = []
        for i in range(n_modes):
            mode_full = np.zeros(len(self.geometry.nodes) * 6)
            mode_full[self.free_dofs] = eigenvectors[:, i]
            mode_shapes_full.append(mode_full)
        
        # Calculate modal participation factors
        participation_factors = self._calculate_participation_factors(
            M_global, mode_shapes_full
        )
        
        return {
            "frequencies": frequencies.tolist(),
            "periods": periods.tolist(),
            "mode_shapes": mode_shapes_full,
            "participation_factors": participation_factors,
            "eigenvalues": eigenvalues.tolist()
        }
    
    def _calculate_participation_factors(self, M, mode_shapes):
        """Calculate modal participation factors"""
        n_dof = M.shape[0]
        influence_vector = np.zeros(n_dof)
        
        # Set influence vector (1 for translational DOFs)
        for i in range(0, n_dof, 6):
            influence_vector[i:i+3] = 1.0  # ux, uy, uz
        
        participation_factors = []
        for mode in mode_shapes:
            phi = np.array(mode)
            gamma = (phi.T @ M @ influence_vector) / (phi.T @ M @ phi)
            participation_factors.append(gamma)
        
        return participation_factors
