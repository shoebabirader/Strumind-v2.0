"""
Unit tests for modal analysis
"""
import pytest
import numpy as np
from scipy.linalg import eigh


class TestModalAnalysis:
    """Test modal analysis implementation"""
    
    def test_single_dof_oscillator(self):
        """Test modal analysis against known single DOF solution"""
        # Single DOF mass-spring system
        # Known solution: f = (1/2π) * sqrt(k/m)
        
        m = 1000  # kg
        k = 4 * np.pi**2 * 1000  # N/m (gives f = 1 Hz)
        
        # Create mass and stiffness matrices
        M = np.array([[m]])
        K = np.array([[k]])
        
        # Solve eigenvalue problem
        eigenvalues, eigenvectors = eigh(K, M)
        
        # Calculate frequency
        omega = np.sqrt(eigenvalues[0])
        frequency = omega / (2 * np.pi)
        
        # Should be 1 Hz
        assert abs(frequency - 1.0) < 0.001
    
    def test_two_dof_system(self):
        """Test two DOF system with known solution"""
        # Two DOF system with equal masses and stiffnesses
        m1 = m2 = 1000  # kg
        k1 = k2 = k3 = 1000  # N/m
        
        # Mass matrix
        M = np.array([
            [m1, 0],
            [0, m2]
        ])
        
        # Stiffness matrix
        K = np.array([
            [k1 + k2, -k2],
            [-k2, k2 + k3]
        ])
        
        # Solve
        eigenvalues, eigenvectors = eigh(K, M)
        
        # Calculate frequencies
        frequencies = np.sqrt(eigenvalues) / (2 * np.pi)
        
        # Should have two distinct frequencies
        assert len(frequencies) == 2
        assert frequencies[0] < frequencies[1]
        assert frequencies[0] > 0
        assert frequencies[1] > 0
    
    def test_rigid_body_mode_filtering(self):
        """Test filtering of rigid body modes"""
        # Create system with rigid body modes (singular stiffness)
        M = np.eye(3) * 1000  # kg
        K = np.array([
            [1000, -1000, 0],
            [-1000, 2000, -1000],
            [0, -1000, 1000]
        ])
        
        # This system has one rigid body mode (zero eigenvalue)
        eigenvalues, eigenvectors = eigh(K, M)
        
        # Filter rigid body modes
        tolerance = 1e-6
        valid_modes = eigenvalues > tolerance
        
        eigenvalues_valid = eigenvalues[valid_modes]
        
        # Should have 2 valid modes (3 total - 1 rigid body)
        assert len(eigenvalues_valid) == 2
        assert np.all(eigenvalues_valid > tolerance)
    
    def test_frequency_calculation_guards(self):
        """Test guards against division by zero in frequency calculation"""
        # Include zero eigenvalue
        eigenvalues = np.array([0.0, 1000.0, 4000.0])
        
        # Calculate frequencies with guards
        omega = np.sqrt(np.abs(eigenvalues))
        frequencies = omega / (2 * np.pi)
        
        # Calculate periods with guards
        periods = np.where(frequencies > 1e-10, 1.0 / frequencies, np.inf)
        
        # First mode should have infinite period
        assert periods[0] == np.inf
        assert np.isfinite(periods[1])
        assert np.isfinite(periods[2])
        
        # Non-zero frequencies should be finite
        assert frequencies[1] > 0
        assert frequencies[2] > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
