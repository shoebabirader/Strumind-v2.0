"""
Unit tests for DOF Manager
"""
import pytest
import numpy as np
from app.engine.dof_manager import DOFManager


class MockNode:
    """Mock node for testing"""
    def __init__(self, node_id):
        self.id = node_id


class TestDOFManager:
    """Test DOF management system"""
    
    def test_initialization(self):
        """Test DOF manager initialization"""
        nodes = [MockNode(i) for i in range(5)]
        dof_mgr = DOFManager(nodes)
        
        assert dof_mgr.num_nodes == 5
        assert dof_mgr.dofs_per_node == 6
        assert dof_mgr.total_dofs == 30
    
    def test_node_index_mapping(self):
        """Test node ID to index mapping"""
        nodes = [MockNode(10), MockNode(20), MockNode(30)]
        dof_mgr = DOFManager(nodes)
        
        assert dof_mgr.get_node_index(10) == 0
        assert dof_mgr.get_node_index(20) == 1
        assert dof_mgr.get_node_index(30) == 2
        
        assert dof_mgr.get_node_id(0) == 10
        assert dof_mgr.get_node_id(1) == 20
        assert dof_mgr.get_node_id(2) == 30
    
    def test_get_node_dofs(self):
        """Test getting DOF indices for a node"""
        nodes = [MockNode(i) for i in range(3)]
        dof_mgr = DOFManager(nodes)
        
        # Node 0 should have DOFs 0-5
        dofs_0 = dof_mgr.get_node_dofs(0)
        assert dofs_0 == [0, 1, 2, 3, 4, 5]
        
        # Node 1 should have DOFs 6-11
        dofs_1 = dof_mgr.get_node_dofs(1)
        assert dofs_1 == [6, 7, 8, 9, 10, 11]
        
        # Node 2 should have DOFs 12-17
        dofs_2 = dof_mgr.get_node_dofs(2)
        assert dofs_2 == [12, 13, 14, 15, 16, 17]
    
    def test_get_element_dofs(self):
        """Test getting DOF indices for an element"""
        nodes = [MockNode(i) for i in range(3)]
        dof_mgr = DOFManager(nodes)
        
        # Element connecting nodes 0 and 1
        elem_dofs = dof_mgr.get_element_dofs(0, 1)
        assert elem_dofs == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        assert len(elem_dofs) == 12
    
    def test_translation_rotation_dofs(self):
        """Test getting translation and rotation DOFs"""
        nodes = [MockNode(i) for i in range(2)]
        dof_mgr = DOFManager(nodes)
        
        # Translation DOFs (ux, uy, uz)
        trans_dofs = dof_mgr.get_translation_dofs(0)
        assert trans_dofs == [0, 1, 2]
        
        # Rotation DOFs (rx, ry, rz)
        rot_dofs = dof_mgr.get_rotation_dofs(0)
        assert rot_dofs == [3, 4, 5]
    
    def test_create_dof_map(self):
        """Test creating free and restrained DOF lists"""
        nodes = [MockNode(i) for i in range(2)]
        dof_mgr = DOFManager(nodes)
        
        # Restrain all DOFs of node 0
        restraints = {
            0: [True, True, True, True, True, True],
            1: [False, False, False, False, False, False]
        }
        
        free_dofs, restrained_dofs = dof_mgr.create_dof_map(restraints)
        
        assert restrained_dofs == [0, 1, 2, 3, 4, 5]
        assert free_dofs == [6, 7, 8, 9, 10, 11]
    
    def test_expand_reduce_vector(self):
        """Test vector expansion and reduction"""
        nodes = [MockNode(i) for i in range(2)]
        dof_mgr = DOFManager(nodes)
        
        free_dofs = [6, 7, 8, 9, 10, 11]
        
        # Create reduced vector
        reduced = np.array([1, 2, 3, 4, 5, 6])
        
        # Expand to full
        full = dof_mgr.expand_vector(reduced, free_dofs)
        assert full.shape == (12,)
        assert np.allclose(full[:6], 0)
        assert np.allclose(full[6:], reduced)
        
        # Reduce back
        reduced_back = dof_mgr.reduce_vector(full, free_dofs)
        assert np.allclose(reduced_back, reduced)
    
    def test_reduce_matrix(self):
        """Test matrix reduction"""
        nodes = [MockNode(i) for i in range(2)]
        dof_mgr = DOFManager(nodes)
        
        free_dofs = [6, 7, 8]
        
        # Create full matrix
        full_matrix = np.random.rand(12, 12)
        
        # Reduce
        reduced = dof_mgr.reduce_matrix(full_matrix, free_dofs)
        assert reduced.shape == (3, 3)
        
        # Check values match
        for i, dof_i in enumerate(free_dofs):
            for j, dof_j in enumerate(free_dofs):
                assert reduced[i, j] == full_matrix[dof_i, dof_j]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
