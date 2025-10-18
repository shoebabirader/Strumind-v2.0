"""
Nonlinear Analysis Features
Material nonlinearity, plasticity, and iterative solvers
"""
import numpy as np
from scipy.linalg import lu_factor, lu_solve
from typing import Dict, Tuple, Optional, Callable
import logging

logger = logging.getLogger(__name__)


class MaterialNonlinearity:
    """Material nonlinearity models"""
    
    @staticmethod
    def bilinear_stress_strain(strain: float, fy: float, E: float, 
                               H: float = None) -> Tuple[float, float]:
        """
        Bilinear stress-strain relationship
        
        Args:
            strain: Strain value
            fy: Yield stress
            E: Young's modulus
            H: Hardening modulus (default: E/100)
        
        Returns:
            (stress, tangent_modulus)
        """
        if H is None:
            H = E / 100  # Typical hardening modulus
        
        epsilon_y = fy / E
        
        if abs(strain) <= epsilon_y:
            # Elastic range
            stress = E * strain
            Et = E
        else:
            # Plastic range
            sign = np.sign(strain)
            stress = sign * (fy + H * (abs(strain) - epsilon_y))
            Et = H
        
        return stress, Et
    
    @staticmethod
    def multilinear_stress_strain(strain: float, 
                                  stress_points: list, 
                                  strain_points: list) -> Tuple[float, float]:
        """
        Multilinear stress-strain relationship
        
        Args:
            strain: Strain value
            stress_points: List of stress values
            strain_points: List of strain values
        
        Returns:
            (stress, tangent_modulus)
        """
        strain = abs(strain)
        sign = np.sign(strain) if strain != 0 else 1
        
        # Find segment
        for i in range(len(strain_points) - 1):
            if strain_points[i] <= strain <= strain_points[i+1]:
                # Linear interpolation
                epsilon1, epsilon2 = strain_points[i], strain_points[i+1]
                sigma1, sigma2 = stress_points[i], stress_points[i+1]
                
                stress = sigma1 + (sigma2 - sigma1) * (strain - epsilon1) / (epsilon2 - epsilon1)
                Et = (sigma2 - sigma1) / (epsilon2 - epsilon1)
                
                return sign * stress, Et
        
        # Beyond last point - use last tangent
        Et = (stress_points[-1] - stress_points[-2]) / (strain_points[-1] - strain_points[-2])
        stress = stress_points[-1] + Et * (strain - strain_points[-1])
        
        return sign * stress, Et
    
    @staticmethod
    def concrete_compression_curve(strain: float, fck: float) -> Tuple[float, float]:
        """
        Concrete compression stress-strain curve (Hognestad parabola)
        
        Args:
            strain: Compressive strain (positive)
            fck: Characteristic compressive strength
        
        Returns:
            (stress, tangent_modulus)
        """
        epsilon_0 = 0.002  # Strain at peak stress
        epsilon_cu = 0.0035  # Ultimate strain
        
        if strain <= 0:
            return 0.0, 0.0
        
        if strain <= epsilon_0:
            # Ascending branch (parabola)
            stress = fck * (2 * strain / epsilon_0 - (strain / epsilon_0)**2)
            Et = fck * (2 / epsilon_0 - 2 * strain / epsilon_0**2)
        elif strain <= epsilon_cu:
            # Descending branch (linear)
            stress = fck * (1 - 0.15 * (strain - epsilon_0) / (epsilon_cu - epsilon_0))
            Et = -0.15 * fck / (epsilon_cu - epsilon_0)
        else:
            # Crushed
            stress = 0.0
            Et = 0.0
        
        return stress, Et
    
    @staticmethod
    def steel_tension_curve(strain: float, fy: float, fu: float, 
                           E: float = 200000) -> Tuple[float, float]:
        """
        Steel tension stress-strain curve
        
        Args:
            strain: Tensile strain
            fy: Yield strength
            fu: Ultimate strength
            E: Young's modulus
        
        Returns:
            (stress, tangent_modulus)
        """
        epsilon_y = fy / E
        epsilon_sh = 0.01  # Strain hardening starts
        epsilon_u = 0.15  # Ultimate strain
        
        if strain < 0:
            # Compression (simplified - same as tension)
            return MaterialNonlinearity.steel_tension_curve(-strain, fy, fu, E)
        
        if strain <= epsilon_y:
            # Elastic
            stress = E * strain
            Et = E
        elif strain <= epsilon_sh:
            # Yield plateau
            stress = fy
            Et = 0.0
        elif strain <= epsilon_u:
            # Strain hardening
            stress = fy + (fu - fy) * (strain - epsilon_sh) / (epsilon_u - epsilon_sh)
            Et = (fu - fy) / (epsilon_u - epsilon_sh)
        else:
            # Fracture
            stress = 0.0
            Et = 0.0
        
        return stress, Et


class NewtonRaphsonSolver:
    """Newton-Raphson iterative solver for nonlinear analysis"""
    
    def __init__(self, max_iterations: int = 50, tolerance: float = 1e-4):
        """
        Initialize solver
        
        Args:
            max_iterations: Maximum iterations
            tolerance: Convergence tolerance
        """
        self.max_iterations = max_iterations
        self.tolerance = tolerance
    
    def solve(self, K_func: Callable, F_ext: np.ndarray, 
             u0: np.ndarray = None) -> Dict:
        """
        Solve nonlinear system using Newton-Raphson
        
        K(u) * Δu = F_ext - F_int(u)
        
        Args:
            K_func: Function that returns (K_tangent, F_internal) given u
            F_ext: External force vector
            u0: Initial displacement guess
        
        Returns:
            Dict with solution and convergence info
        """
        n_dof = len(F_ext)
        
        if u0 is None:
            u = np.zeros(n_dof)
        else:
            u = u0.copy()
        
        converged = False
        iteration = 0
        residual_history = []
        
        logger.info("Starting Newton-Raphson iteration")
        
        while not converged and iteration < self.max_iterations:
            iteration += 1
            
            # Get tangent stiffness and internal forces
            K_t, F_int = K_func(u)
            
            # Calculate residual
            R = F_ext - F_int
            residual_norm = np.linalg.norm(R)
            residual_history.append(residual_norm)
            
            # Check convergence
            if iteration > 1:
                force_norm = np.linalg.norm(F_ext)
                if force_norm > 1e-10:
                    relative_residual = residual_norm / force_norm
                else:
                    relative_residual = residual_norm
                
                if relative_residual < self.tolerance:
                    converged = True
                    logger.info(f"Newton-Raphson converged in {iteration} iterations")
                    break
            
            # Solve for displacement increment
            try:
                du = np.linalg.solve(K_t, R)
            except np.linalg.LinAlgError:
                logger.error("Singular tangent stiffness matrix")
                break
            
            # Update displacement
            u = u + du
            
            logger.debug(f"Iteration {iteration}: residual = {residual_norm:.6e}")
        
        if not converged:
            logger.warning(f"Newton-Raphson did not converge after {self.max_iterations} iterations")
        
        return {
            'displacement': u,
            'converged': converged,
            'iterations': iteration,
            'residual_history': residual_history,
            'final_residual': residual_history[-1] if residual_history else 0.0
        }


class ArcLengthSolver:
    """Arc-length method for snap-through and snap-back problems"""
    
    def __init__(self, max_iterations: int = 50, tolerance: float = 1e-4):
        """
        Initialize arc-length solver
        
        Args:
            max_iterations: Maximum iterations per load step
            tolerance: Convergence tolerance
        """
        self.max_iterations = max_iterations
        self.tolerance = tolerance
    
    def solve(self, K_func: Callable, F_ref: np.ndarray,
             n_steps: int = 10, arc_length: float = 1.0) -> Dict:
        """
        Solve using arc-length method
        
        Args:
            K_func: Function returning (K_tangent, F_internal)
            F_ref: Reference load vector
            n_steps: Number of load steps
            arc_length: Arc length parameter
        
        Returns:
            Dict with load-displacement history
        """
        n_dof = len(F_ref)
        
        # Storage
        u_history = [np.zeros(n_dof)]
        lambda_history = [0.0]
        
        u = np.zeros(n_dof)
        lambda_total = 0.0
        
        logger.info(f"Starting arc-length method: {n_steps} steps")
        
        for step in range(n_steps):
            # Predictor step
            K_t, F_int = K_func(u)
            
            # Solve for predictor
            du_bar = np.linalg.solve(K_t, F_ref)
            
            # Calculate load increment
            dlambda = arc_length / np.sqrt(np.dot(du_bar, du_bar))
            
            # Predictor displacement
            du_pred = dlambda * du_bar
            u_pred = u + du_pred
            lambda_pred = lambda_total + dlambda
            
            # Corrector iterations
            converged = False
            for iteration in range(self.max_iterations):
                K_t, F_int = K_func(u_pred)
                
                # Residual
                R = lambda_pred * F_ref - F_int
                
                # Check convergence
                if np.linalg.norm(R) < self.tolerance * np.linalg.norm(F_ref):
                    converged = True
                    break
                
                # Correction
                du_corr = np.linalg.solve(K_t, R)
                u_pred = u_pred + du_corr
            
            if converged:
                u = u_pred
                lambda_total = lambda_pred
                u_history.append(u.copy())
                lambda_history.append(lambda_total)
                logger.debug(f"Step {step+1}/{n_steps}: λ = {lambda_total:.4f}")
            else:
                logger.warning(f"Step {step+1} did not converge")
                break
        
        return {
            'displacement_history': np.array(u_history),
            'load_factor_history': np.array(lambda_history),
            'n_steps_completed': len(u_history) - 1
        }


class PlasticHingeModel:
    """Plastic hinge model for beam-column elements"""
    
    def __init__(self, My: float, Mp: float, theta_y: float, theta_p: float):
        """
        Initialize plastic hinge
        
        Args:
            My: Yield moment
            Mp: Plastic moment capacity
            theta_y: Yield rotation
            theta_p: Plastic rotation capacity
        """
        self.My = My
        self.Mp = Mp
        self.theta_y = theta_y
        self.theta_p = theta_p
        self.state = 'elastic'  # elastic, yielding, plastic, failed
    
    def get_moment_rotation(self, theta: float) -> Tuple[float, float]:
        """
        Get moment and rotational stiffness for given rotation
        
        Args:
            theta: Rotation
        
        Returns:
            (moment, rotational_stiffness)
        """
        theta_abs = abs(theta)
        sign = np.sign(theta) if theta != 0 else 1
        
        if theta_abs <= self.theta_y:
            # Elastic
            M = (self.My / self.theta_y) * theta
            K_r = self.My / self.theta_y
            self.state = 'elastic'
        elif theta_abs <= self.theta_y + self.theta_p:
            # Plastic
            M = sign * (self.My + (self.Mp - self.My) * 
                       (theta_abs - self.theta_y) / self.theta_p)
            K_r = (self.Mp - self.My) / self.theta_p
            self.state = 'plastic'
        else:
            # Failed
            M = 0.0
            K_r = 0.0
            self.state = 'failed'
        
        return M, K_r
