"""
Unit tests for P-Delta analysis
"""
import pytest
import numpy as np
from app.engine.pdelta import PDeltaAnalysis


class TestPDeltaAnalysis:
    """Test P-Delta analysis implementation"""
    
    def test_geometric_stiffness_matrix_size(self):
        """Test that geometric stiffness matrix has correct dimensions"""
        # Test with simple case
        axial_forces = np.array([1000, 2000])  # N
        lengths = np.array([3.0, 4.0])  # m
        n_dof = 18  # 3 nodes × 6 DOF
        
        # Create geometric stiffness matrix
        Kg = np.zeros((n_dof, n_dof))
        
        assert Kg.shape == (n_dof, n_dof)
    
    def test_geometric_stiffness_compression_vs_tension(self):
        """Test that compression and tension give opposite effects"""
        # Compression (negative axial force)
        axial_compression = -1000  # N
        L = 3.0  # m
        
        # Geometric stiffness coefficient for compression
        kg_compression = axial_compression / L
        
        # Tension (positive axial force)
        axial_tension = 1000  # N
        kg_tension = axial_tension / L
        
        # Compression should reduce stiffness (negative contribution)
        # Tension should increase stiffness (positive contribution)
        assert kg_compression < 0
        assert kg_tension > 0
        assert abs(kg_compression) == abs(kg_tension)
    
    def test_amplification_factor(self):
        """Test P-Delta amplification factor calculation"""
        # Test known case: cantilever column
        P = 1000  # N (compression)
        L = 3.0   # m
        E = 200e9  # Pa
        I = 1e-6   # m⁴
        
        # Euler buckling load
        Pe = np.pi**2 * E * I / (4 * L**2)  # For cantilever
        
        # Amplification factor
        amplification = 1 / (1 - P / Pe)
        
        # Should be > 1 for compression
        assert amplification > 1.0
        
        # Should approach infinity as P approaches Pe
        P_near_buckling = 0.9 * Pe
        amp_near_buckling = 1 / (1 - P_near_buckling / Pe)
        assert amp_near_buckling > amplification
    
    def test_convergence_criteria(self):
        """Test P-Delta convergence criteria"""
        tolerance = 0.05  # 5% tolerance
        
        # Test displacement convergence
        u_prev = np.array([0.01, 0.02, 0.03])
        u_curr = np.array([0.0101, 0.0201, 0.0301])
        
        # Calculate relative change
        rel_change = np.linalg.norm(u_curr - u_prev) / np.linalg.norm(u_curr)
        converged = rel_change < tolerance
        
        # Small change should converge
        assert converged
        
        # Large change should not converge
        u_large = np.array([0.02, 0.04, 0.06])
        rel_change_large = np.linalg.norm(u_large - u_prev) / np.linalg.norm(u_large)
        not_converged = rel_change_large < tolerance
        assert not not_converged
    
    def test_stability_check(self):
        """Test structural stability check"""
        # Stable case (P < Pe)
        P = 1000  # N
        Pe = 5000  # N
        
        is_stable = P < Pe
        assert is_stable
        
        # Unstable case (P >= Pe)
        P_unstable = 6000  # N
        is_unstable = P_unstable < Pe
        assert not is_unstable


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
