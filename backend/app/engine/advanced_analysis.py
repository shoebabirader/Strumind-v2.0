"""
Advanced Analysis Module
Time-History, Buckling, Load Combinations, Envelope Results
"""
import numpy as np
from typing import Dict, List, Tuple
from scipy.linalg import eigh
from scipy.integrate import odeint

class TimeHistoryAnalysis:
    """Time-History Analysis using Newmark-Beta Method"""
    
    def __init__(self, beta: float = 0.25, gamma: float = 0.5):
        self.beta = beta  # Newmark parameter
        self.gamma = gamma  # Newmark parameter
        
    def newmark_beta(self, M: np.ndarray, C: np.ndarray, K: np.ndarray,
                     F_t: np.ndarray, dt: float, damping_ratio: float = 0.05) -> Dict:
        """
        Newmark-Beta time integration
        
        Args:
            M: Mass matrix
            C: Damping matrix
            K: Stiffness matrix
            F_t: Force time history (n_steps x n_dof)
            dt: Time step
            damping_ratio: Damping ratio
        """
        n_dof = M.shape[0]
        n_steps = F_t.shape[0]
        
        # Initialize arrays
        u = np.zeros((n_steps, n_dof))
        v = np.zeros((n_steps, n_dof))
        a = np.zeros((n_steps, n_dof))
        
        # Initial acceleration
        a[0] = np.linalg.solve(M, F_t[0] - C @ v[0] - K @ u[0])
        
        # Newmark constants
        a0 = 1.0 / (self.beta * dt**2)
        a1 = self.gamma / (self.beta * dt)
        a2 = 1.0 / (self.beta * dt)
        a3 = 1.0 / (2.0 * self.beta) - 1.0
        a4 = self.gamma / self.beta - 1.0
        a5 = dt / 2.0 * (self.gamma / self.beta - 2.0)
        a6 = dt * (1.0 - self.gamma)
        a7 = self.gamma * dt
        
        # Effective stiffness matrix
        K_eff = K + a0 * M + a1 * C
        
        # Time integration loop
        for i in range(n_steps - 1):
            # Effective force
            F_eff = (F_t[i+1] + 
                    M @ (a0 * u[i] + a2 * v[i] + a3 * a[i]) +
                    C @ (a1 * u[i] + a4 * v[i] + a5 * a[i]))
            
            # Solve for displacement
            u[i+1] = np.linalg.solve(K_eff, F_eff)
            
            # Update velocity and acceleration
            a[i+1] = a0 * (u[i+1] - u[i]) - a2 * v[i] - a3 * a[i]
            v[i+1] = v[i] + a6 * a[i] + a7 * a[i+1]
        
        # Calculate max responses
        max_displacement = np.max(np.abs(u), axis=0)
        max_velocity = np.max(np.abs(v), axis=0)
        max_acceleration = np.max(np.abs(a), axis=0)
        
        return {
            "displacements": u.tolist(),
            "velocities": v.tolist(),
            "accelerations": a.tolist(),
            "max_displacement": max_displacement.tolist(),
            "max_velocity": max_velocity.tolist(),
            "max_acceleration": max_acceleration.tolist(),
            "time_step": dt,
            "n_steps": n_steps,
            "method": "Newmark-Beta"
        }

class BucklingAnalysis:
    """Linear and Nonlinear Buckling Analysis"""
    
    def linear_buckling(self, K: np.ndarray, Kg: np.ndarray, 
                       n_modes: int = 10) -> Dict:
        """
        Linear buckling analysis (eigenvalue problem)
        
        K * phi = lambda * Kg * phi
        
        Args:
            K: Elastic stiffness matrix
            Kg: Geometric stiffness matrix
            n_modes: Number of buckling modes
        """
        # Solve generalized eigenvalue problem
        eigenvalues, eigenvectors = eigh(K, Kg)
        
        # Sort by eigenvalue
        idx = np.argsort(eigenvalues)
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
        
        # Critical load factors
        load_factors = eigenvalues[:n_modes]
        mode_shapes = eigenvectors[:, :n_modes]
        
        return {
            "load_factors": load_factors.tolist(),
            "mode_shapes": mode_shapes.tolist(),
            "critical_load_factor": load_factors[0],
            "n_modes": n_modes,
            "analysis_type": "Linear Buckling"
        }
    
    def lateral_torsional_buckling(self, M: float, L: float, 
                                   E: float, G: float,
                                   Iy: float, Iw: float, J: float) -> Dict:
        """
        Lateral-torsional buckling of beams
        
        Args:
            M: Applied moment
            L: Unbraced length
            E: Young's modulus
            G: Shear modulus
            Iy: Weak axis moment of inertia
            Iw: Warping constant
            J: Torsional constant
        """
        # Critical moment (simplified)
        C1 = 1.0  # Moment gradient factor
        
        Mcr = (C1 * np.pi / L) * np.sqrt(
            E * Iy * G * J * (1 + (np.pi**2 * E * Iw) / (L**2 * G * J))
        )
        
        # Safety factor
        safety_factor = Mcr / M if M > 0 else float('inf')
        
        status = "OK" if safety_factor >= 1.0 else "FAIL"
        
        return {
            "critical_moment": Mcr,
            "applied_moment": M,
            "safety_factor": safety_factor,
            "status": status,
            "analysis_type": "Lateral-Torsional Buckling"
        }

class LoadCombinations:
    """Automatic Load Combination Generation"""
    
    def __init__(self, code: str = "IS875"):
        self.code = code
        
    def generate_combinations(self, load_cases: Dict[str, float]) -> Dict:
        """
        Generate load combinations per code
        
        Args:
            load_cases: Dictionary of load case names and factors
                       e.g., {"DL": 1.0, "LL": 1.0, "EQX": 1.0, "WX": 1.0}
        """
        if self.code == "IS875":
            return self._is875_combinations(load_cases)
        elif self.code == "ACI318":
            return self._aci318_combinations(load_cases)
        elif self.code == "ASCE7":
            return self._asce7_combinations(load_cases)
        else:
            return self._is875_combinations(load_cases)
    
    def _is875_combinations(self, lc: Dict[str, float]) -> Dict:
        """IS 875 load combinations"""
        combinations = {}
        
        # Basic combinations
        if "DL" in lc:
            combinations["1.5 DL"] = {"DL": 1.5}
        
        if "DL" in lc and "LL" in lc:
            combinations["1.5 (DL + LL)"] = {"DL": 1.5, "LL": 1.5}
        
        if "DL" in lc and "LL" in lc and "WX" in lc:
            combinations["1.2 (DL + LL + WX)"] = {"DL": 1.2, "LL": 1.2, "WX": 1.2}
            combinations["1.5 (DL + WX)"] = {"DL": 1.5, "WX": 1.5}
            combinations["0.9 DL + 1.5 WX"] = {"DL": 0.9, "WX": 1.5}
        
        if "DL" in lc and "LL" in lc and "EQX" in lc:
            combinations["1.2 (DL + LL + EQX)"] = {"DL": 1.2, "LL": 1.2, "EQX": 1.2}
            combinations["1.5 (DL + EQX)"] = {"DL": 1.5, "EQX": 1.5}
            combinations["0.9 DL + 1.5 EQX"] = {"DL": 0.9, "EQX": 1.5}
        
        return {
            "combinations": combinations,
            "n_combinations": len(combinations),
            "code": "IS 875"
        }
    
    def _aci318_combinations(self, lc: Dict[str, float]) -> Dict:
        """ACI 318 load combinations"""
        combinations = {}
        
        if "DL" in lc and "LL" in lc:
            combinations["1.4 D"] = {"DL": 1.4}
            combinations["1.2 D + 1.6 L"] = {"DL": 1.2, "LL": 1.6}
        
        if "DL" in lc and "LL" in lc and "WX" in lc:
            combinations["1.2 D + 1.0 W + 0.5 L"] = {"DL": 1.2, "WX": 1.0, "LL": 0.5}
            combinations["0.9 D + 1.0 W"] = {"DL": 0.9, "WX": 1.0}
        
        if "DL" in lc and "LL" in lc and "EQX" in lc:
            combinations["1.2 D + 1.0 E + 0.5 L"] = {"DL": 1.2, "EQX": 1.0, "LL": 0.5}
            combinations["0.9 D + 1.0 E"] = {"DL": 0.9, "EQX": 1.0}
        
        return {
            "combinations": combinations,
            "n_combinations": len(combinations),
            "code": "ACI 318"
        }
    
    def _asce7_combinations(self, lc: Dict[str, float]) -> Dict:
        """ASCE 7 load combinations"""
        combinations = {}
        
        if "DL" in lc and "LL" in lc:
            combinations["1.4 D"] = {"DL": 1.4}
            combinations["1.2 D + 1.6 L"] = {"DL": 1.2, "LL": 1.6}
        
        if "DL" in lc and "LL" in lc and "WX" in lc:
            combinations["1.2 D + 1.0 W + 0.5 L"] = {"DL": 1.2, "WX": 1.0, "LL": 0.5}
            combinations["0.9 D + 1.0 W"] = {"DL": 0.9, "WX": 1.0}
        
        if "DL" in lc and "LL" in lc and "EQX" in lc:
            combinations["1.2 D + 1.0 E + 0.5 L"] = {"DL": 1.2, "EQX": 1.0, "LL": 0.5}
            combinations["0.9 D + 1.0 E"] = {"DL": 0.9, "EQX": 1.0}
        
        return {
            "combinations": combinations,
            "n_combinations": len(combinations),
            "code": "ASCE 7"
        }

class EnvelopeResults:
    """Calculate envelope (max/min) results from multiple load combinations"""
    
    def calculate_envelope(self, results: Dict[str, np.ndarray]) -> Dict:
        """
        Calculate envelope results
        
        Args:
            results: Dictionary of load combination results
                    {"Combo1": array, "Combo2": array, ...}
        """
        # Stack all results
        all_results = np.array(list(results.values()))
        
        # Calculate envelopes
        max_values = np.max(all_results, axis=0)
        min_values = np.min(all_results, axis=0)
        abs_max = np.maximum(np.abs(max_values), np.abs(min_values))
        
        # Find governing combinations
        max_combo_idx = np.argmax(all_results, axis=0)
        min_combo_idx = np.argmin(all_results, axis=0)
        
        combo_names = list(results.keys())
        
        return {
            "max_values": max_values.tolist(),
            "min_values": min_values.tolist(),
            "abs_max_values": abs_max.tolist(),
            "governing_max_combo": [combo_names[i] for i in max_combo_idx],
            "governing_min_combo": [combo_names[i] for i in min_combo_idx],
            "n_combinations": len(results)
        }
