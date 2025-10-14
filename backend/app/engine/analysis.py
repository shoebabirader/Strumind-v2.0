import numpy as np
from scipy.linalg import lu_factor, lu_solve
from scipy.sparse.linalg import eigs

class StructuralAnalysis:
    def __init__(self, geometry_engine):
        self.geometry = geometry_engine
        self.K_global = None
        self.displacements = None
        
    def assemble_stiffness_matrix(self, material_props, section_props):
        """Assemble global stiffness matrix"""
        n_dof = len(self.geometry.nodes) * 6
        K = np.zeros((n_dof, n_dof))
        
        for elem in self.geometry.elements.values():
            k_local = self._element_stiffness(elem, material_props, section_props)
            # Transform and assemble into global matrix
            # Simplified - full implementation would include transformation matrix
            
        self.K_global = K
        return K
    
    def _element_stiffness(self, element, material_props, section_props):
        """Calculate element stiffness matrix"""
        E = material_props.get('E', 2e11)  # Young's modulus
        A = section_props.get('A', 0.01)   # Cross-sectional area
        L = element.length()
        
        if element.element_type == "truss":
            k = (E * A / L) * np.array([[1, -1], [-1, 1]])
        else:
            # Simplified beam element stiffness
            k = np.eye(12) * (E * A / L)
        
        return k
    
    def static_analysis(self, loads):
        """Perform static analysis using LU decomposition"""
        if self.K_global is None:
            raise ValueError("Stiffness matrix not assembled")
        
        F = np.array(loads)
        lu, piv = lu_factor(self.K_global)
        self.displacements = lu_solve((lu, piv), F)
        
        return self.displacements
    
    def modal_analysis(self, n_modes=10):
        """Extract natural frequencies and mode shapes"""
        if self.K_global is None:
            raise ValueError("Stiffness matrix not assembled")
        
        # Mass matrix (simplified - uniform mass)
        M = np.eye(self.K_global.shape[0])
        
        eigenvalues, eigenvectors = eigs(self.K_global, k=n_modes, M=M, which='SM')
        frequencies = np.sqrt(np.real(eigenvalues)) / (2 * np.pi)
        
        return frequencies, eigenvectors
