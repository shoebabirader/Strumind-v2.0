"""
Unit tests for Rayleigh damping
"""
import pytest
import numpy as np


class TestRayleighDamping:
    """Test Rayleigh damping implementation"""
    
    def test_damping_coefficients(self):
        """Test Rayleigh damping coefficient calculation"""
        omega1 = 10.0  # rad/s
        omega2 = 30.0  # rad/s
        zeta = 0.05    # 5% damping
        
        # Solve for coefficients manually
        A = np.array([
            [1/(2*omega1), omega1/2],
            [1/(2*omega2), omega2/2]
        ])
        b = np.array([zeta, zeta])
        alpha, beta = np.linalg.solve(A, b)
        
        # Check coefficients are positive
        assert alpha > 0
        assert beta > 0
    
    def test_damping_matrix_construction(self):
        """Test Rayleigh damping matrix construction"""
        # Simple 2-DOF system
        M = np.array([[1000, 0], [0, 1000]])  # kg
        K = np.array([[2000, -1000], [-1000, 2000]])  # N/m
        
        # Frequencies
        omega1 = 10.0  # rad/s
        omega2 = 20.0  # rad/s
        zeta = 0.05    # 5% damping
        
        # Calculate coefficients
        A = np.array([
            [1/(2*omega1), omega1/2],
            [1/(2*omega2), omega2/2]
        ])
        b = np.array([zeta, zeta])
        alpha, beta = np.linalg.solve(A, b)
        
        # Calculate damping matrix
        C = alpha * M + beta * K
        
        # Check dimensions
        assert C.shape == M.shape
        assert C.shape == K.shape
    
    def test_damping_ratio_verification(self):
        """Test that specified damping ratios are achieved"""
        omega1 = 5.0   # rad/s
        omega2 = 25.0  # rad/s
        zeta = 0.03    # 3% damping
        
        # Calculate coefficients
        A = np.array([
            [1/(2*omega1), omega1/2],
            [1/(2*omega2), omega2/2]
        ])
        b = np.array([zeta, zeta])
        alpha, beta = np.linalg.solve(A, b)
        
        # Calculate damping ratios at specified frequencies
        zeta1_calc = (alpha / (2*omega1)) + (beta * omega1 / 2)
        zeta2_calc = (alpha / (2*omega2)) + (beta * omega2 / 2)
        
        # Should match specified damping ratio
        assert abs(zeta1_calc - zeta) < 1e-10
        assert abs(zeta2_calc - zeta) < 1e-10
    
    def test_symmetry(self):
        """Test that damping matrix is symmetric"""
        M = np.array([[1000, 200], [200, 800]])  # kg (symmetric)
        K = np.array([[2500, -800], [-800, 1800]])  # N/m (symmetric)
        
        omega1 = 12.0
        omega2 = 35.0
        zeta = 0.06
        
        # Calculate coefficients
        A = np.array([
            [1/(2*omega1), omega1/2],
            [1/(2*omega2), omega2/2]
        ])
        b = np.array([zeta, zeta])
        alpha, beta = np.linalg.solve(A, b)
        
        C = alpha * M + beta * K
        
        # Should be symmetric
        assert np.allclose(C, C.T)
    
    def test_zero_damping(self):
        """Test behavior with zero damping"""
        M = np.eye(2)
        K = np.eye(2)
        
        omega1 = 10.0
        omega2 = 20.0
        zeta = 0.0  # Zero damping
        
        # Calculate coefficients
        A = np.array([
            [1/(2*omega1), omega1/2],
            [1/(2*omega2), omega2/2]
        ])
        b = np.array([zeta, zeta])
        alpha, beta = np.linalg.solve(A, b)
        
        C = alpha * M + beta * K
        
        # Should result in zero damping matrix
        assert np.allclose(C, np.zeros_like(C))
        assert abs(alpha) < 1e-15
        assert abs(beta) < 1e-15


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
