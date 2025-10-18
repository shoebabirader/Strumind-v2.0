"""
P-Delta and Geometric Nonlinear Analysis Module
"""
import numpy as np
from typing import Dict, List, Tuple
from scipy.linalg import solve

class PDeltaAnalysis:
    """P-Delta and geometric nonlinearity analysis"""
    
    def __init__(self, tolerance: float = 1e-6, max_iterations: int = 50):
        self.tolerance = tolerance
        self.max_iterations = max_iterations
        self.convergence_history = []
        
    def pdelta_analysis(self, K: np.ndarray, M: np.ndarray, 
                       P: np.ndarray, axial_forces: np.ndarray,
                       element_lengths: np.ndarray) -> Dict:
        """
        Perform P-Delta analysis using iterative method
        
        Args:
            K: Initial stiffness matrix
            M: Mass matrix
            P: Applied loads
            axial_forces: Initial axial forces in members
            element_lengths: Length of each element
        """
        n_dof = K.shape[0]
        
        # Initial displacement
        u = solve(K, P)
        
        iteration = 0
        converged = False
        
        while iteration < self.max_iterations and not converged:
            # Calculate geometric stiffness matrix
            Kg = self._geometric_stiffness_matrix(
                axial_forces, element_lengths, n_dof
            )
            
            # Modified stiffness matrix
            K_modified = K - Kg
            
            # Solve for new displacements
            u_new = solve(K_modified, P)
            
            # Check convergence
            error = np.linalg.norm(u_new - u) / np.linalg.norm(u_new)
            self.convergence_history.append(error)
            
            if error < self.tolerance:
                converged = True
            
            # Update for next iteration
            u = u_new
            axial_forces = self._update_axial_forces(K, u)
            iteration += 1
        
        # Calculate amplification factor
        u_first_order = solve(K, P)
        amplification = np.linalg.norm(u) / np.linalg.norm(u_first_order)
        
        return {
            "displacements": u.tolist(),
            "first_order_displacements": u_first_order.tolist(),
            "amplification_factor": amplification,
            "iterations": iteration,
            "converged": converged,
            "final_error": error if converged else None,
            "convergence_history": self.convergence_history
        }
    
    def _geometric_stiffness_matrix(self, axial_forces: np.ndarray,
                                   lengths: np.ndarray, n_dof: int) -> np.ndarray:
        """
        Calculate 12x12 geometric stiffness matrix for 3D frame elements
        
        Based on stability functions for beam-columns under axial load.
        Properly accounts for all 6 DOFs per node.
        
        Args:
            axial_forces: Axial force in each element (N, positive = tension)
            lengths: Length of each element (m)
            n_dof: Total number of DOFs in system
        
        Returns:
            Global geometric stiffness matrix
        """
        Kg = np.zeros((n_dof, n_dof))
        
        for i, (P, L) in enumerate(zip(axial_forces, lengths)):
            if L <= 0:
                continue
            
            # 12x12 geometric stiffness matrix in local coordinates
            # Based on stability functions for beam-columns
            kg_local = np.zeros((12, 12))
            
            # Coefficient for geometric stiffness
            coeff = P / L
            
            # Axial DOFs (0, 6) - no geometric stiffness
            # kg_local[0, 0] = kg_local[6, 6] = 0
            
            # Bending about local y-axis (DOFs: 2, 5, 8, 11)
            # Transverse displacements and rotations
            kg_local[2, 2] = kg_local[8, 8] = 6/5 * coeff
            kg_local[2, 8] = kg_local[8, 2] = -6/5 * coeff
            kg_local[5, 5] = kg_local[11, 11] = 2*L/15 * coeff
            kg_local[5, 11] = kg_local[11, 5] = -L/30 * coeff
            kg_local[2, 5] = kg_local[5, 2] = L/10 * coeff
            kg_local[2, 11] = kg_local[11, 2] = -L/10 * coeff
            kg_local[8, 5] = kg_local[5, 8] = -L/10 * coeff
            kg_local[8, 11] = kg_local[11, 8] = L/10 * coeff
            
            # Bending about local z-axis (DOFs: 1, 4, 7, 10)
            # Transverse displacements and rotations
            kg_local[1, 1] = kg_local[7, 7] = 6/5 * coeff
            kg_local[1, 7] = kg_local[7, 1] = -6/5 * coeff
            kg_local[4, 4] = kg_local[10, 10] = 2*L/15 * coeff
            kg_local[4, 10] = kg_local[10, 4] = -L/30 * coeff
            kg_local[1, 4] = kg_local[4, 1] = -L/10 * coeff
            kg_local[1, 10] = kg_local[10, 1] = L/10 * coeff
            kg_local[7, 4] = kg_local[4, 7] = L/10 * coeff
            kg_local[7, 10] = kg_local[10, 7] = -L/10 * coeff
            
            # Transform to global coordinates (would need transformation matrix)
            # For now, assume local = global (simplified)
            # In full implementation: Kg_global = T.T @ kg_local @ T
            
            # Assemble into global matrix using proper DOF mapping
            # Assuming 6 DOFs per node and element i connects nodes i and i+1
            start_dof_i = i * 6
            start_dof_j = (i + 1) * 6
            
            if start_dof_j + 6 <= n_dof:
                # Node i DOFs
                for local_i in range(6):
                    global_i = start_dof_i + local_i
                    for local_j in range(6):
                        global_j = start_dof_i + local_j
                        Kg[global_i, global_j] += kg_local[local_i, local_j]
                
                # Node j DOFs
                for local_i in range(6):
                    global_i = start_dof_j + local_i
                    for local_j in range(6):
                        global_j = start_dof_j + local_j
                        Kg[global_i, global_j] += kg_local[local_i + 6, local_j + 6]
                
                # Coupling terms
                for local_i in range(6):
                    global_i = start_dof_i + local_i
                    for local_j in range(6):
                        global_j = start_dof_j + local_j
                        Kg[global_i, global_j] += kg_local[local_i, local_j + 6]
                        Kg[global_j, global_i] += kg_local[local_j + 6, local_i]
        
        return Kg
    
    def _update_axial_forces(self, K: np.ndarray, u: np.ndarray) -> np.ndarray:
        """Update axial forces based on current displacements"""
        # Simplified - calculate forces from K*u
        forces = K @ u
        n_elements = len(forces) // 2
        axial_forces = np.zeros(n_elements)
        
        for i in range(n_elements):
            axial_forces[i] = forces[i * 2]
        
        return axial_forces
    
    def stability_index(self, story_shear: float, story_weight: float,
                       story_drift: float, story_height: float) -> Dict:
        """
        Calculate stability index (theta) per AISC/ACI
        
        θ = (P × Δ) / (V × h)
        
        If θ > 0.1, P-Delta effects are significant
        """
        theta = (story_weight * story_drift) / (story_shear * story_height)
        
        if theta <= 0.1:
            status = "P-Delta effects negligible"
            recommendation = "First-order analysis acceptable"
        elif theta <= 0.2:
            status = "P-Delta effects moderate"
            recommendation = "Second-order analysis recommended"
        else:
            status = "P-Delta effects significant"
            recommendation = "Second-order analysis required, check stability"
        
        return {
            "stability_index": theta,
            "status": status,
            "recommendation": recommendation,
            "story_shear": story_shear,
            "story_weight": story_weight,
            "story_drift": story_drift,
            "story_height": story_height
        }
    
    def moment_amplification_factor(self, Pu: float, Pc: float,
                                    Cm: float = 1.0) -> Dict:
        """
        Calculate moment amplification factor per ACI 318
        
        δ = Cm / (1 - Pu/Pc) ≥ 1.0
        """
        if Pu >= Pc:
            return {
                "amplification_factor": None,
                "status": "UNSTABLE",
                "message": "Applied load exceeds critical load"
            }
        
        delta = Cm / (1 - Pu / Pc)
        delta = max(delta, 1.0)
        
        return {
            "amplification_factor": delta,
            "applied_load": Pu,
            "critical_load": Pc,
            "load_ratio": Pu / Pc,
            "Cm_factor": Cm,
            "status": "OK"
        }
    
    def critical_load_euler(self, E: float, I: float, L: float,
                           K_factor: float = 1.0) -> float:
        """
        Calculate Euler critical load
        
        Pcr = π² × E × I / (K × L)²
        """
        Pcr = (np.pi ** 2 * E * I) / ((K_factor * L) ** 2)
        return Pcr
    
    def effective_length_factor(self, end_condition: str) -> float:
        """Get effective length factor based on end conditions"""
        factors = {
            "pinned-pinned": 1.0,
            "fixed-fixed": 0.5,
            "fixed-pinned": 0.7,
            "fixed-free": 2.0,
            "fixed-guided": 1.0
        }
        return factors.get(end_condition, 1.0)
    
    def large_deformation_analysis(self, K: np.ndarray, P: np.ndarray,
                                   load_steps: int = 10) -> Dict:
        """
        Incremental-iterative analysis for large deformations
        """
        n_dof = K.shape[0]
        P_increment = P / load_steps
        
        u_total = np.zeros(n_dof)
        load_history = []
        displacement_history = []
        
        for step in range(load_steps):
            P_current = P_increment * (step + 1)
            
            # Newton-Raphson iteration
            u_step = np.zeros(n_dof)
            for iteration in range(self.max_iterations):
                # Residual force
                R = P_current - K @ (u_total + u_step)
                
                # Check convergence
                if np.linalg.norm(R) < self.tolerance:
                    break
                
                # Update displacement
                du = solve(K, R)
                u_step += du
            
            u_total += u_step
            load_history.append(np.linalg.norm(P_current))
            displacement_history.append(np.linalg.norm(u_total))
        
        return {
            "final_displacement": u_total.tolist(),
            "load_history": load_history,
            "displacement_history": displacement_history,
            "load_steps": load_steps
        }
