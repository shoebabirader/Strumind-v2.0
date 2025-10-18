"""
Dynamic Analysis Features
Time-history integration, response spectrum, and damping models
"""
import numpy as np
from scipy.linalg import eigh
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class DampingModel:
    """Damping models for dynamic analysis"""
    
    @staticmethod
    def rayleigh_damping(M: np.ndarray, K: np.ndarray, 
                        omega1: float, omega2: float, 
                        zeta: float = 0.05) -> Tuple[np.ndarray, float, float]:
        """
        Calculate Rayleigh damping matrix using standard formulation
        
        C = α*M + β*K
        
        where α and β are solved from the system:
        zeta_i = (α / (2*omega_i)) + (β * omega_i / 2)
        
        for two modes with frequencies omega1 and omega2
        
        Args:
            M: Mass matrix
            K: Stiffness matrix
            omega1: First frequency (rad/s)
            omega2: Second frequency (rad/s)
            zeta: Damping ratio (typically 0.02-0.05)
        
        Returns:
            Tuple of (C, alpha, beta) where C is damping matrix
        """
        # Standard Rayleigh damping coefficients
        # Solve the linear system:
        # [1/(2*omega1)  omega1/2] [alpha] = [zeta]
        # [1/(2*omega2)  omega2/2] [beta ]   [zeta]
        
        A = np.array([
            [1/(2*omega1), omega1/2],
            [1/(2*omega2), omega2/2]
        ])
        b = np.array([zeta, zeta])
        
        # Solve for alpha and beta
        alpha, beta = np.linalg.solve(A, b)
        
        # Construct damping matrix
        C = alpha * M + beta * K
        
        return C, alpha, beta
    
    @staticmethod
    def modal_damping(mode_shapes: np.ndarray, M: np.ndarray, 
                     damping_ratios: List[float]) -> np.ndarray:
        """
        Calculate damping matrix using modal damping
        
        Args:
            mode_shapes: Modal matrix (eigenvectors)
            M: Mass matrix
            damping_ratios: Damping ratio for each mode
        
        Returns:
            Damping matrix C
        """
        n_modes = len(damping_ratios)
        phi = mode_shapes[:, :n_modes]
        
        # Modal damping matrix
        C_modal = np.diag(2 * np.array(damping_ratios))
        
        # Transform to physical coordinates
        C = phi @ C_modal @ phi.T @ M
        return C


class TimeHistoryAnalysis:
    """Time-history integration for dynamic analysis"""
    
    def __init__(self, M: np.ndarray, C: np.ndarray, K: np.ndarray):
        """
        Initialize time-history analysis
        
        Args:
            M: Mass matrix
            C: Damping matrix
            K: Stiffness matrix
        """
        self.M = M
        self.C = C
        self.K = K
        self.n_dof = M.shape[0]
    
    def newmark_beta(self, F_t: np.ndarray, dt: float, 
                    u0: np.ndarray = None, v0: np.ndarray = None, a0: np.ndarray = None,
                    beta: float = 0.25, gamma: float = 0.5) -> Dict:
        """
        Newmark-β time integration method
        
        Unconditionally stable for β ≥ 0.25 and γ ≥ 0.5
        
        Args:
            F_t: Force time history (n_steps x n_dof)
            dt: Time step
            u0: Initial displacement
            v0: Initial velocity
            a0: Initial acceleration
            beta: Newmark beta parameter (0.25 for constant average acceleration)
            gamma: Newmark gamma parameter (0.5 for constant average acceleration)
        
        Returns:
            Dict with displacement, velocity, acceleration time histories
        """
        n_steps = F_t.shape[0]
        
        # Initialize arrays
        if u0 is None:
            u0 = np.zeros(self.n_dof)
        if v0 is None:
            v0 = np.zeros(self.n_dof)
        if a0 is None:
            # Calculate initial acceleration: M*a0 = F0 - C*v0 - K*u0
            a0 = np.linalg.solve(self.M, F_t[0] - self.C @ v0 - self.K @ u0)
        
        # Storage
        u = np.zeros((n_steps, self.n_dof))
        v = np.zeros((n_steps, self.n_dof))
        a = np.zeros((n_steps, self.n_dof))
        
        u[0] = u0
        v[0] = v0
        a[0] = a0
        
        # Newmark constants
        a0_const = 1.0 / (beta * dt**2)
        a1 = gamma / (beta * dt)
        a2 = 1.0 / (beta * dt)
        a3 = 1.0 / (2 * beta) - 1.0
        a4 = gamma / beta - 1.0
        a5 = dt / 2 * (gamma / beta - 2.0)
        a6 = dt * (1.0 - gamma)
        a7 = gamma * dt
        
        # Effective stiffness matrix
        K_eff = self.K + a0_const * self.M + a1 * self.C
        
        # Time integration loop
        for i in range(n_steps - 1):
            # Effective force
            F_eff = (F_t[i+1] + 
                    self.M @ (a0_const * u[i] + a2 * v[i] + a3 * a[i]) +
                    self.C @ (a1 * u[i] + a4 * v[i] + a5 * a[i]))
            
            # Solve for displacement
            u[i+1] = np.linalg.solve(K_eff, F_eff)
            
            # Update velocity and acceleration
            a[i+1] = a0_const * (u[i+1] - u[i]) - a2 * v[i] - a3 * a[i]
            v[i+1] = v[i] + a6 * a[i] + a7 * a[i+1]
        
        logger.info(f"Newmark-β integration completed: {n_steps} steps, dt={dt}s")
        
        return {
            'displacement': u,
            'velocity': v,
            'acceleration': a,
            'time': np.arange(n_steps) * dt,
            'max_displacement': np.max(np.abs(u), axis=0),
            'max_velocity': np.max(np.abs(v), axis=0),
            'max_acceleration': np.max(np.abs(a), axis=0)
        }
    
    def wilson_theta(self, F_t: np.ndarray, dt: float,
                    u0: np.ndarray = None, v0: np.ndarray = None, a0: np.ndarray = None,
                    theta: float = 1.4) -> Dict:
        """
        Wilson-θ time integration method
        
        Unconditionally stable for θ ≥ 1.37
        
        Args:
            F_t: Force time history
            dt: Time step
            u0, v0, a0: Initial conditions
            theta: Wilson theta parameter (typically 1.4)
        
        Returns:
            Dict with time histories
        """
        n_steps = F_t.shape[0]
        tau = theta * dt
        
        # Initialize
        if u0 is None:
            u0 = np.zeros(self.n_dof)
        if v0 is None:
            v0 = np.zeros(self.n_dof)
        if a0 is None:
            a0 = np.linalg.solve(self.M, F_t[0] - self.C @ v0 - self.K @ u0)
        
        # Storage
        u = np.zeros((n_steps, self.n_dof))
        v = np.zeros((n_steps, self.n_dof))
        a = np.zeros((n_steps, self.n_dof))
        
        u[0] = u0
        v[0] = v0
        a[0] = a0
        
        # Wilson-θ constants
        a0_const = 6.0 / tau**2
        a1 = 3.0 / tau
        a2 = 2.0 * a1
        a3 = tau / 2.0
        
        # Effective stiffness
        K_eff = self.K + a0_const * self.M + a1 * self.C
        
        # Time integration
        for i in range(n_steps - 1):
            # Incremental force
            dF = F_t[i+1] - F_t[i]
            dF_tau = theta * dF
            
            # Effective force
            F_eff = (F_t[i] + dF_tau +
                    self.M @ (a0_const * u[i] + a2 * v[i] + 2.0 * a[i]) +
                    self.C @ (a1 * u[i] + 2.0 * v[i] + a3 * a[i]))
            
            # Solve for displacement at t + τ
            u_tau = np.linalg.solve(K_eff, F_eff)
            
            # Acceleration at t + τ
            a_tau = a0_const * (u_tau - u[i]) - a2 * v[i] - 2.0 * a[i]
            
            # Interpolate to t + dt
            a[i+1] = a[i] + (a_tau - a[i]) / theta
            v[i+1] = v[i] + dt * (a[i] + a[i+1]) / 2.0
            u[i+1] = u[i] + dt * v[i] + dt**2 * (a[i] + a[i+1]) / 6.0
        
        logger.info(f"Wilson-θ integration completed: {n_steps} steps, dt={dt}s")
        
        return {
            'displacement': u,
            'velocity': v,
            'acceleration': a,
            'time': np.arange(n_steps) * dt,
            'max_displacement': np.max(np.abs(u), axis=0),
            'max_velocity': np.max(np.abs(v), axis=0),
            'max_acceleration': np.max(np.abs(a), axis=0)
        }


class ResponseSpectrumAnalysis:
    """Response spectrum analysis"""
    
    @staticmethod
    def generate_design_spectrum(code: str, zone: str, soil_type: str,
                                 damping: float = 0.05) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate design response spectrum per code
        
        Args:
            code: Design code (IS1893, ASCE7, EC8)
            zone: Seismic zone
            soil_type: Soil type (I, II, III)
            damping: Damping ratio
        
        Returns:
            (periods, spectral_accelerations)
        """
        if code == "IS1893":
            return ResponseSpectrumAnalysis._is1893_spectrum(zone, soil_type, damping)
        elif code == "ASCE7":
            return ResponseSpectrumAnalysis._asce7_spectrum(zone, soil_type, damping)
        else:
            # Default spectrum
            T = np.linspace(0, 4, 100)
            Sa = 2.5 * np.ones_like(T)  # Simplified
            return T, Sa
    
    @staticmethod
    def _is1893_spectrum(zone: str, soil_type: str, damping: float) -> Tuple[np.ndarray, np.ndarray]:
        """Generate IS 1893:2016 design spectrum"""
        # Zone factors
        Z_map = {'II': 0.10, 'III': 0.16, 'IV': 0.24, 'V': 0.36}
        Z = Z_map.get(zone, 0.16)
        
        # Soil factors
        if soil_type == 'I':  # Rock/Hard soil
            T_corners = [0.0, 0.10, 0.40, 4.0]
            Sa_factors = [1.0, 2.5, 2.5, 1.0]
        elif soil_type == 'II':  # Medium soil
            T_corners = [0.0, 0.10, 0.55, 4.0]
            Sa_factors = [1.0, 2.5, 2.5, 1.36]
        else:  # Soft soil
            T_corners = [0.0, 0.10, 0.67, 4.0]
            Sa_factors = [1.0, 2.5, 2.5, 1.67]
        
        # Generate spectrum
        T = np.linspace(0, 4, 200)
        Sa = np.zeros_like(T)
        
        for i, t in enumerate(T):
            if t <= T_corners[1]:
                Sa[i] = Sa_factors[0] + (Sa_factors[1] - Sa_factors[0]) * t / T_corners[1]
            elif t <= T_corners[2]:
                Sa[i] = Sa_factors[2]
            else:
                Sa[i] = Sa_factors[2] * T_corners[2] / t
        
        # Apply zone factor
        Sa = (Z / 2) * Sa
        
        # Damping correction (if not 5%)
        if damping != 0.05:
            damping_factor = np.sqrt(0.05 / damping)
            Sa = Sa * damping_factor
        
        return T, Sa
    
    @staticmethod
    def _asce7_spectrum(zone: str, soil_type: str, damping: float) -> Tuple[np.ndarray, np.ndarray]:
        """Generate ASCE 7 design spectrum"""
        # ASCE 7 spectral parameters (simplified for common locations)
        # In production, use actual USGS hazard maps
        
        # Mapped spectral acceleration parameters
        if zone.upper() == "HIGH":
            Ss = 1.5  # Short period spectral acceleration
            S1 = 0.6  # 1-second spectral acceleration
        elif zone.upper() == "MODERATE":
            Ss = 0.75
            S1 = 0.3
        else:  # LOW
            Ss = 0.25
            S1 = 0.1
        
        # Site coefficients
        if soil_type.upper() == "A":  # Hard rock
            Fa, Fv = 0.8, 0.8
        elif soil_type.upper() == "B":  # Rock
            Fa, Fv = 1.0, 1.0
        elif soil_type.upper() == "C":  # Very dense soil
            Fa, Fv = 1.2, 1.8
        elif soil_type.upper() == "D":  # Stiff soil
            Fa, Fv = 1.6, 2.4
        else:  # E - Soft clay
            Fa, Fv = 2.5, 3.5
        
        # Design spectral parameters
        SMS = Fa * Ss
        SM1 = Fv * S1
        SDS = (2/3) * SMS
        SD1 = (2/3) * SM1
        
        # Transition periods
        TS = SD1 / SDS
        TL = 8.0  # Long-period transition (simplified)
        T0 = 0.2 * TS
        
        # Generate spectrum
        T = np.linspace(0, 4, 200)
        Sa = np.zeros_like(T)
        
        for i, t in enumerate(T):
            if t <= T0:
                Sa[i] = SDS * (0.4 + 0.6 * t / T0)
            elif t <= TS:
                Sa[i] = SDS
            elif t <= TL:
                Sa[i] = SD1 / t
            else:
                Sa[i] = SD1 * TL / (t**2)
        
        # Apply damping modification if not 5%
        if damping != 0.05:
            B = 4 / (5.6 - np.log(100 * damping))  # ASCE 7 damping factor
            Sa = Sa * B
        
        return T, Sa
    
    @staticmethod
    def modal_combination_srss(modal_responses: List[np.ndarray]) -> np.ndarray:
        """
        Square Root of Sum of Squares (SRSS) modal combination
        
        Args:
            modal_responses: List of modal response vectors
        
        Returns:
            Combined response
        """
        combined = np.zeros_like(modal_responses[0])
        
        for response in modal_responses:
            combined += response**2
        
        return np.sqrt(combined)
    
    @staticmethod
    def modal_combination_cqc(modal_responses: List[np.ndarray],
                              frequencies: List[float],
                              damping: float = 0.05) -> np.ndarray:
        """
        Complete Quadratic Combination (CQC) modal combination
        
        Accounts for closely spaced modes
        
        Args:
            modal_responses: List of modal response vectors
            frequencies: Natural frequencies (Hz)
            damping: Damping ratio
        
        Returns:
            Combined response
        """
        n_modes = len(modal_responses)
        combined = np.zeros_like(modal_responses[0])
        
        # Calculate correlation coefficients
        for i in range(n_modes):
            for j in range(n_modes):
                omega_i = 2 * np.pi * frequencies[i]
                omega_j = 2 * np.pi * frequencies[j]
                
                # Frequency ratio
                beta = omega_j / omega_i if omega_i > 0 else 1.0
                
                # Correlation coefficient
                rho_ij = (8 * damping**2 * (1 + beta) * beta**(3/2)) / \
                        ((1 - beta**2)**2 + 4 * damping**2 * beta * (1 + beta)**2)
                
                combined += rho_ij * modal_responses[i] * modal_responses[j]
        
        return np.sqrt(np.abs(combined))
