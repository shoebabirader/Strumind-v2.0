"""
Degree of Freedom (DOF) Management System
Handles mapping between node IDs and contiguous DOF indices
"""
import numpy as np
from typing import Dict, List, Tuple


class DOFManager:
    """
    Manage DOF indexing for structural analysis
    
    Provides consistent mapping between node IDs (which may be non-contiguous)
    and zero-based DOF indices for matrix assembly.
    """
    
    def __init__(self, nodes: List):
        """
        Initialize DOF manager with node list
        
        Args:
            nodes: List of node objects with .id attribute
        """
        # Create contiguous node index mapping
        self.node_id_to_index = {}
        self.node_index_to_id = {}
        
        for i, node in enumerate(nodes):
            node_id = node.id if hasattr(node, 'id') else node.get('id', i)
            self.node_id_to_index[node_id] = i
            self.node_index_to_id[i] = node_id
        
        self.num_nodes = len(nodes)
        self.dofs_per_node = 6  # 3 translations + 3 rotations
        self.total_dofs = self.num_nodes * self.dofs_per_node
    
    def get_node_index(self, node_id) -> int:
        """Get contiguous index for a node ID"""
        return self.node_id_to_index[node_id]
    
    def get_node_id(self, node_index: int):
        """Get node ID from contiguous index"""
        return self.node_index_to_id[node_index]
    
    def get_node_dofs(self, node_id) -> List[int]:
        """
        Get DOF indices for a node
        
        Args:
            node_id: Node identifier
        
        Returns:
            List of 6 DOF indices [ux, uy, uz, rx, ry, rz]
        """
        node_index = self.node_id_to_index[node_id]
        start_dof = node_index * self.dofs_per_node
        return list(range(start_dof, start_dof + self.dofs_per_node))
    
    def get_element_dofs(self, node_i_id, node_j_id) -> List[int]:
        """
        Get DOF indices for a 2-node element
        
        Args:
            node_i_id: Start node identifier
            node_j_id: End node identifier
        
        Returns:
            List of 12 DOF indices (6 per node)
        """
        dofs_i = self.get_node_dofs(node_i_id)
        dofs_j = self.get_node_dofs(node_j_id)
        return dofs_i + dofs_j
    
    def get_translation_dofs(self, node_id) -> List[int]:
        """Get translation DOF indices for a node [ux, uy, uz]"""
        dofs = self.get_node_dofs(node_id)
        return dofs[:3]
    
    def get_rotation_dofs(self, node_id) -> List[int]:
        """Get rotation DOF indices for a node [rx, ry, rz]"""
        dofs = self.get_node_dofs(node_id)
        return dofs[3:6]
    
    def create_dof_map(self, restraints: Dict) -> Tuple[List[int], List[int]]:
        """
        Create free and restrained DOF lists
        
        Args:
            restraints: Dict mapping node_id to list of 6 booleans
                       True = restrained, False = free
        
        Returns:
            Tuple of (free_dofs, restrained_dofs)
        """
        all_dofs = set(range(self.total_dofs))
        restrained_dofs = set()
        
        for node_id, restraint_list in restraints.items():
            if node_id not in self.node_id_to_index:
                continue
            
            node_dofs = self.get_node_dofs(node_id)
            for i, is_restrained in enumerate(restraint_list):
                if is_restrained:
                    restrained_dofs.add(node_dofs[i])
        
        free_dofs = sorted(list(all_dofs - restrained_dofs))
        restrained_dofs = sorted(list(restrained_dofs))
        
        return free_dofs, restrained_dofs
    
    def expand_vector(self, reduced_vector: np.ndarray, 
                     free_dofs: List[int]) -> np.ndarray:
        """
        Expand reduced vector to full DOF space
        
        Args:
            reduced_vector: Vector with only free DOFs
            free_dofs: List of free DOF indices
        
        Returns:
            Full vector with zeros at restrained DOFs
        """
        full_vector = np.zeros(self.total_dofs)
        full_vector[free_dofs] = reduced_vector
        return full_vector
    
    def reduce_vector(self, full_vector: np.ndarray, 
                     free_dofs: List[int]) -> np.ndarray:
        """
        Reduce full vector to free DOFs only
        
        Args:
            full_vector: Vector with all DOFs
            free_dofs: List of free DOF indices
        
        Returns:
            Reduced vector with only free DOFs
        """
        return full_vector[free_dofs]
    
    def reduce_matrix(self, full_matrix: np.ndarray, 
                     free_dofs: List[int]) -> np.ndarray:
        """
        Reduce full matrix to free DOFs only
        
        Args:
            full_matrix: Matrix with all DOFs
            free_dofs: List of free DOF indices
        
        Returns:
            Reduced matrix with only free DOFs
        """
        return full_matrix[np.ix_(free_dofs, free_dofs)]
