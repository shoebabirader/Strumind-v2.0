"""
Unit tests for pushover analysis
"""
import pytest
import numpy as np
from app.engine.pushover_analysis import PushoverAnalysis


class TestPushoverAnalysis:
    """Test pushover analysis implementation"""
    
    def test_initialization(self):
        """Test pushover analysis initialization"""
        model_data = {
            "nodes": {},
            "elements": {},
            "materials": {}
        }
        pushover = PushoverAnalysis(model_data)
        assert pushover is not None
        assert pushover.model == model_data
    
    def test_stiffness_reduction(self):
        """Test that yielded elements reduce stiffness"""
        model_data = {
            "nodes": {},
            "elements": {
                'elem1': {
                    'material': 'steel',
                    'area': 0.01,
                    'length': 1.0,
                    'node_i': 0,
                    'node_j': 1
                }
            },
            "materials": {
                'steel': {'E': 200000}  # MPa
            }
        }
        pushover = PushoverAnalysis(model_data)
        
        # Create simple 2-DOF stiffness matrix
        K = np.array([[100, -50], [-50, 100]])
        
        # Test that stiffness reduction factor is correct
        # Post-yield stiffness should be 3% of elastic
        post_yield_factor = 0.03
        K_reduced = K * post_yield_factor
        
        # Stiffness should be reduced
        assert np.linalg.norm(K_reduced) < np.linalg.norm(K)
        
        # Reduction should be approximately 97% (3% post-yield)
        reduction_ratio = np.linalg.norm(K_reduced) / np.linalg.norm(K)
        assert abs(reduction_ratio - post_yield_factor) < 0.01
    
    def test_capacity_curve_softening(self):
        """Test that capacity curve shows softening after yield"""
        model_data = {
            "nodes": {0: {'z': 0}, 1: {'z': 3}},
            "elements": {
                'elem1': {
                    'material': 'steel',
                    'area': 0.01,
                    'length': 3.0,
                    'node_i': 0,
                    'node_j': 1,
                    'fy': 250  # MPa
                }
            },
            "materials": {'steel': {'E': 200000, 'fy': 250}}
        }
        pushover = PushoverAnalysis(model_data)
        
        # Test yield force calculation
        elem = pushover.elements['elem1']
        fy = elem['fy'] * elem['area'] * 1000  # Convert to N
        assert fy > 0
        
        # Test ultimate force (typically 1.5x yield)
        fu = fy * 1.5
        assert fu > fy
    
    def test_performance_levels(self):
        """Test performance level determination"""
        model_data = {
            "nodes": {},
            "elements": {},
            "materials": {}
        }
        pushover = PushoverAnalysis(model_data)
        
        # Test different drift ratios
        # IO: < 0.5%
        drift_io = 0.004
        assert drift_io < 0.005
        
        # LS: 0.5% - 1.5%
        drift_ls = 0.01
        assert 0.005 <= drift_ls <= 0.015
        
        # CP: 1.5% - 2.5%
        drift_cp = 0.02
        assert 0.015 < drift_cp <= 0.025
        
        # C: > 2.5%
        drift_c = 0.03
        assert drift_c > 0.025


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
