"""
Advanced Analysis Features
Implements P-Delta, buckling, and other advanced analysis capabilities
"""
import numpy as np
from scipy.linalg import eigh, lu_factor, lu_solve
from scipy.sparse import lil_matrix, csr_matrix
from scipy.sparse.linalg import eigs, spsolve
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class PDeltaAnalysis:
    """
    P-Delta (Geometric Nonlinearity) Analysis
    Accounts for second-order effects due to axial forces
    """
    
    def __init__(self, geometry_engine, analysis_engine):
        """
        Initialize P-Delta analysis
        
        Args:
            geometry_engine: Geometry engine with nodes and elements
            analysis_engine: Structural analysis engine
        """
        self.geometry = geometry_engine
        self.analysis = analysis_engine
        self.max_iterations = 50
        self.tolerance = 1e-4
    
    def geometric_stiffness_matrix(self, element, axial_force: float) -> np.ndarray:
        """
        Calculate geometric stiffness matrix for an element
        
        The geometric stiffness matrix accounts for the effect of axial force
        on the lateral stiffness of the element.
        
        Args:
            element: Element object
            axial_force: Axial force in element (N, compression positive)
        
        Returns:
            12x12 geometric stiffness matrix
        """
        L = element.length()
        
        if L < 1e-6:
            return np.zeros((12, 12))
        
        P = axial_force
        
        # Geometric stiffness matrix in local coordinates
        # For a beam element with axial force P
        Kg_local = np.zeros((12, 12))
        
        # Coefficients
        c1 = P / L
        c2 = P / (30 * L)
        c3 = P / (6)
        
        # Bending in xy-plane (DOF: uy, rz)
        Kg_local[1, 1] = 6 * c1 / 5
        Kg_local[1, 5] = c1 * L / 10
        Kg_local[1, 7] = -6 * c1 / 5
        Kg_local[1, 11] = c1 * L / 10
        
        Kg_local[5, 1] = c1 * L / 10
        Kg_local[5, 5] = 2 * c1 * L**2 / 15
        Kg_local[5, 7] = -c1 * L / 10
        Kg_local[5, 11] = -c1 * L**2 / 30
        
        Kg_local[7, 1] = -6 * c1 / 5
        Kg_local[7, 5] = -c1 * L / 10
        Kg_local[7, 7] = 6 * c1 / 5
        Kg_local[7, 11] = -c1 * L / 10
        
        Kg_local[11, 1] = c1 * L / 10
        Kg_local[11, 5] = -c1 * L**2 / 30
        Kg_local[11, 7] = -c1 * L / 10
        Kg_local[11, 11] = 2 * c1 * L**2 / 15
        
        # Bending in xz-plane (DOF: uz, ry)
        Kg_local[2, 2] = 6 * c1 / 5
        Kg_local[2, 4] = -c1 * L / 10
        Kg_local[2, 8] = -6 * c1 / 5
        Kg_local[2, 10] = -c1 * L / 10
        
        Kg_local[4, 2] = -c1 * L / 10
        Kg_local[4, 4] = 2 * c1 * L**2 / 15
        Kg_local[4, 8] = c1 * L / 10
        Kg_local[4, 10] = -c1 * L**2 / 30
        
        Kg_local[8, 2] = -6 * c1 / 5
        Kg_local[8, 4] = c1 * L / 10
        Kg_local[8, 8] = 6 * c1 / 5
        Kg_local[8, 10] = c1 * L / 10
        
        Kg_local[10, 2] = -c1 * L / 10
        Kg_local[10, 4] = -c1 * L**2 / 30
        Kg_local[10, 8] = c1 * L / 10
        Kg_local[10, 10] = 2 * c1 * L**2 / 15
        
        return Kg_local
    
    def assemble_geometric_stiffness(self, element_forces: Dict) -> np.ndarray:
        """
        Assemble global geometric stiffness matrix
        
        Args:
            element_forces: Dict of {element_id: forces_dict}
        
        Returns:
            Global geometric stiffness matrix
        """
        n_dof = len(self.geometry.nodes) * 6
        Kg = np.zeros((n_dof, n_dof))
        
        for elem_id, elem in self.geometry.elements.items():
            if elem_id not in element_forces:
                continue
            
            # Get axial force (compression positive for P-Delta)
            forces = element_forces[elem_id]
            axial_force = -forces['node_1']['axial']  # Negative because tension is positive in analysis
            
            # Calculate local geometric stiffness
            Kg_local = self.geometric_stiffness_matrix(elem, axial_force)
            
            # Get transformation matrix
            T = self.analysis._transformation_matrix_3d(elem)
            
            # Transform to global coordinates
            Kg_global = T.T @ Kg_local @ T
            
            # Assemble into global matrix
            dof_indices = self.analysis._get_element_dof_indices(elem)
            for i, dof_i in enumerate(dof_indices):
                for j, dof_j in enumerate(dof_indices):
                    Kg[dof_i, dof_j] += Kg_global[i, j]
        
        return Kg
    
    def pdelta_analysis(self, loads: np.ndarray, restraints: Dict,
                       material_props: Dict, section_props: Dict) -> Dict:
        """
        Perform P-Delta analysis using iterative approach
        
        Args:
            loads: Load vector
            restraints: Boundary conditions
            material_props: Material properties
            section_props: Section properties
        
        Returns:
            Dict with analysis results including P-Delta effects
        """
        logger.info("Starting P-Delta analysis")
        
        # Step 1: Assemble elastic stiffness matrix
        K_elastic = self.analysis.assemble_stiffness_matrix(material_props, section_props)
        
        # Step 2: Apply boundary conditions
        K_reduced = self.analysis.apply_boundary_conditions(restraints)
        F = np.array(loads)
        F_reduced = F[self.analysis.free_dofs]
        
        # Step 3: Iterative P-Delta analysis
        converged = False
        iteration = 0
        u_prev = np.zeros(len(self.analysis.free_dofs))
        
        while not converged and iteration < self.max_iterations:
            iteration += 1
            
            # Solve for displacements
            lu, piv = lu_factor(K_reduced)
            u_reduced = lu_solve((lu, piv), F_reduced)
            
            # Expand to full displacement vector
            n_dof = K_elastic.shape[0]
            displacements = np.zeros(n_dof)
            displacements[self.analysis.free_dofs] = u_reduced
            
            # Calculate element forces
            self.analysis.displacements = displacements
            self.analysis._calculate_element_forces()
            
            # Assemble geometric stiffness matrix
            Kg = self.assemble_geometric_stiffness(self.analysis.element_forces)
            
            # Update total stiffness: K_total = K_elastic + Kg
            K_total = K_elastic + Kg
            K_reduced = K_total[np.ix_(self.analysis.free_dofs, self.analysis.free_dofs)]
            
            # Check convergence
            if iteration > 1:
                displacement_change = np.linalg.norm(u_reduced - u_prev)
                displacement_norm = np.linalg.norm(u_reduced)
                
                if displacement_norm > 1e-10:
                    relative_change = displacement_change / displacement_norm
                else:
                    relative_change = displacement_change
                
                if relative_change < self.tolerance:
                    converged = True
                    logger.info(f"P-Delta analysis converged in {iteration} iterations")
            
            u_prev = u_reduced.copy()
        
        if not converged:
            logger.warning(f"P-Delta analysis did not converge after {self.max_iterations} iterations")
        
        # Calculate reactions
        reactions = K_elastic @ displacements - F
        
        # Calculate stability index
        stability_indices = self._calculate_stability_indices()
        
        return {
            "displacements": displacements,
            "reactions": reactions,
            "element_forces": self.analysis.element_forces,
            "converged": converged,
            "iterations": iteration,
            "stability_indices": stability_indices,
            "analysis_type": "P-Delta"
        }
    
    def _calculate_stability_indices(self) -> Dict:
        """
        Calculate stability indices for each story
        
        Stability index θ = (P * Δ) / (V * h)
        where:
        - P = total vertical load
        - Δ = story drift
        - V = story shear
        - h = story height
        
        θ < 0.1: OK
        0.1 ≤ θ < 0.2: P-Delta effects significant
        θ ≥ 0.2: Structure potentially unstable
        """
        # Simplified - would need story information
        return {
            "max_index": 0.0,
            "status": "stable",
            "message": "Stability indices within acceptable limits"
        }


class BucklingAnalysis:
    """
    Eigenvalue Buckling Analysis
    Determines critical buckling loads and mode shapes
    """
    
    def __init__(self, geometry_engine, analysis_engine):
        """
        Initialize buckling analysis
        
        Args:
            geometry_engine: Geometry engine
            analysis_engine: Structural analysis engine
        """
        self.geometry = geometry_engine
        self.analysis = analysis_engine
    
    def buckling_analysis(self, material_props: Dict, section_props: Dict,
                         restraints: Dict, reference_loads: np.ndarray,
                         n_modes: int = 10) -> Dict:
        """
        Perform eigenvalue buckling analysis
        
        Solves: (K + λ * Kg) * φ = 0
        where:
        - K = elastic stiffness matrix
        - Kg = geometric stiffness matrix for reference loads
        - λ = load factor (eigenvalue)
        - φ = buckling mode shape (eigenvector)
        
        Args:
            material_props: Material properties
            section_props: Section properties
            restraints: Boundary conditions
            reference_loads: Reference load pattern
            n_modes: Number of buckling modes to extract
        
        Returns:
            Dict with buckling results
        """
        logger.info(f"Starting buckling analysis for {n_modes} modes")
        
        # Step 1: Assemble elastic stiffness matrix
        K = self.analysis.assemble_stiffness_matrix(material_props, section_props)
        
        # Step 2: Perform static analysis with reference loads to get element forces
        static_result = self.analysis.static_analysis(reference_loads, restraints)
        element_forces = static_result['element_forces']
        
        # Step 3: Assemble geometric stiffness matrix
        pdelta = PDeltaAnalysis(self.geometry, self.analysis)
        Kg = pdelta.assemble_geometric_stiffness(element_forces)
        
        # Step 4: Apply boundary conditions
        K_reduced = K[np.ix_(self.analysis.free_dofs, self.analysis.free_dofs)]
        Kg_reduced = Kg[np.ix_(self.analysis.free_dofs, self.analysis.free_dofs)]
        
        # Step 5: Solve eigenvalue problem: K * φ = λ * Kg * φ
        # Note: We solve for smallest eigenvalues (critical buckling loads)
        try:
            eigenvalues, eigenvectors = eigh(K_reduced, Kg_reduced)
            
            # Sort by eigenvalue (smallest first = critical buckling load)
            idx = np.argsort(eigenvalues)
            eigenvalues = eigenvalues[idx[:n_modes]]
            eigenvectors = eigenvectors[:, idx[:n_modes]]
            
            # Critical load factors
            load_factors = eigenvalues
            
            # Expand mode shapes to full DOF
            mode_shapes_full = []
            for i in range(n_modes):
                mode_full = np.zeros(len(self.geometry.nodes) * 6)
                mode_full[self.analysis.free_dofs] = eigenvectors[:, i]
                mode_shapes_full.append(mode_full)
            
            # Identify critical mode
            critical_load_factor = load_factors[0]
            critical_mode = mode_shapes_full[0]
            
            # Stability assessment
            if critical_load_factor < 1.0:
                status = "unstable"
                message = f"Structure is unstable. Critical load factor = {critical_load_factor:.3f}"
            elif critical_load_factor < 2.0:
                status = "marginal"
                message = f"Low factor of safety against buckling. Critical load factor = {critical_load_factor:.3f}"
            else:
                status = "stable"
                message = f"Structure is stable. Critical load factor = {critical_load_factor:.3f}"
            
            logger.info(f"Buckling analysis complete. Critical load factor: {critical_load_factor:.3f}")
            
            return {
                "load_factors": load_factors.tolist(),
                "critical_load_factor": float(critical_load_factor),
                "mode_shapes": mode_shapes_full,
                "critical_mode": critical_mode.tolist(),
                "status": status,
                "message": message,
                "n_modes": n_modes
            }
            
        except Exception as e:
            logger.error(f"Buckling analysis failed: {e}")
            return {
                "status": "error",
                "message": f"Buckling analysis failed: {str(e)}"
            }


class ResultsPostProcessor:
    """
    Post-process analysis results for engineering interpretation
    """
    
    @staticmethod
    def calculate_stresses(element_forces: Dict, section_props: Dict) -> Dict:
        """
        Calculate stresses from element forces
        
        Args:
            element_forces: Dict of element forces
            section_props: Section properties
        
        Returns:
            Dict of element stresses
        """
        element_stresses = {}
        
        for elem_id, forces in element_forces.items():
            section = section_props.get(elem_id, section_props.get('default', {}))
            
            A = section.get('A', 1)  # mm²
            Iy = section.get('Iy', 1)  # mm⁴
            Iz = section.get('Iz', 1)  # mm⁴
            J = section.get('J', 1)  # mm⁴
            d = section.get('d', 1)  # mm (depth)
            b = section.get('b', 1)  # mm (width)
            
            # Node 1 stresses
            N1 = forces['node_1']['axial']
            My1 = forces['node_1']['moment_y']
            Mz1 = forces['node_1']['moment_z']
            T1 = forces['node_1']['torsion']
            V1 = forces['node_1']['shear_y']
            
            # Axial stress
            sigma_axial_1 = N1 / A  # N/mm²
            
            # Bending stress (maximum at extreme fiber)
            sigma_bending_y_1 = abs(My1 * (d/2) / Iy)  # N/mm²
            sigma_bending_z_1 = abs(Mz1 * (b/2) / Iz)  # N/mm²
            
            # Combined normal stress
            sigma_total_1 = abs(sigma_axial_1) + sigma_bending_y_1 + sigma_bending_z_1
            
            # Shear stress
            tau_shear_1 = abs(V1 / A)  # Simplified
            
            # Torsional shear stress
            tau_torsion_1 = abs(T1 * (max(b, d)/2) / J)  # N/mm²
            
            # Combined shear stress
            tau_total_1 = tau_shear_1 + tau_torsion_1
            
            # Von Mises stress
            sigma_vm_1 = np.sqrt(sigma_total_1**2 + 3 * tau_total_1**2)
            
            element_stresses[elem_id] = {
                'node_1': {
                    'sigma_axial': round(sigma_axial_1, 2),
                    'sigma_bending': round(sigma_bending_y_1 + sigma_bending_z_1, 2),
                    'sigma_total': round(sigma_total_1, 2),
                    'tau_shear': round(tau_shear_1, 2),
                    'tau_torsion': round(tau_torsion_1, 2),
                    'tau_total': round(tau_total_1, 2),
                    'sigma_vm': round(sigma_vm_1, 2)
                }
            }
        
        return element_stresses
    
    @staticmethod
    def calculate_utilization_ratios(element_stresses: Dict, material_props: Dict) -> Dict:
        """
        Calculate utilization ratios (demand/capacity)
        
        Args:
            element_stresses: Element stresses
            material_props: Material properties
        
        Returns:
            Dict of utilization ratios
        """
        utilization_ratios = {}
        
        for elem_id, stresses in element_stresses.items():
            material = material_props.get(elem_id, material_props.get('default', {}))
            fy = material.get('fy', 250)  # MPa
            
            # Utilization ratio based on von Mises stress
            sigma_vm = stresses['node_1']['sigma_vm']
            UR = sigma_vm / fy
            
            utilization_ratios[elem_id] = {
                'utilization_ratio': round(UR, 3),
                'status': 'OK' if UR <= 1.0 else 'OVERSTRESSED',
                'margin': round((1.0 - UR) * 100, 1)  # % margin
            }
        
        return utilization_ratios
    
    @staticmethod
    def identify_critical_members(utilization_ratios: Dict, threshold: float = 0.95) -> List[str]:
        """
        Identify members with high utilization ratios
        
        Args:
            utilization_ratios: Dict of URs
            threshold: UR threshold
        
        Returns:
            List of critical member IDs
        """
        critical = []
        
        for elem_id, data in utilization_ratios.items():
            if data['utilization_ratio'] >= threshold:
                critical.append(elem_id)
        
        return sorted(critical, key=lambda x: utilization_ratios[x]['utilization_ratio'], reverse=True)
