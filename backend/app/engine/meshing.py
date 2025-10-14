"""
Auto-Meshing Module
Mesh generation, refinement, and quality checks
"""
import numpy as np
from typing import Dict, List, Tuple

class AutoMesher:
    """Automatic mesh generation for FEM"""
    
    def __init__(self):
        self.mesh = {
            'nodes': {},
            'elements': {}
        }
        self.node_counter = 1
        self.element_counter = 1
        
    def mesh_rectangle(self, width: float, height: float,
                      nx: int, ny: int, element_type: str = "quad4") -> Dict:
        """
        Generate structured mesh for rectangular domain
        
        Args:
            width: Width of rectangle (mm)
            height: Height of rectangle (mm)
            nx: Number of elements in x-direction
            ny: Number of elements in y-direction
            element_type: 'quad4', 'quad8', 'tri3', 'tri6'
        """
        nodes = {}
        elements = {}
        
        # Generate nodes
        dx = width / nx
        dy = height / ny
        
        node_id = 1
        for j in range(ny + 1):
            for i in range(nx + 1):
                x = i * dx
                y = j * dy
                nodes[node_id] = {'x': x, 'y': y, 'z': 0}
                node_id += 1
        
        # Generate elements
        element_id = 1
        
        if element_type == "quad4":
            for j in range(ny):
                for i in range(nx):
                    n1 = j * (nx + 1) + i + 1
                    n2 = n1 + 1
                    n3 = n2 + (nx + 1)
                    n4 = n1 + (nx + 1)
                    
                    elements[element_id] = {
                        'type': 'quad4',
                        'nodes': [n1, n2, n3, n4]
                    }
                    element_id += 1
                    
        elif element_type == "tri3":
            # Split each quad into 2 triangles
            for j in range(ny):
                for i in range(nx):
                    n1 = j * (nx + 1) + i + 1
                    n2 = n1 + 1
                    n3 = n2 + (nx + 1)
                    n4 = n1 + (nx + 1)
                    
                    # Triangle 1
                    elements[element_id] = {
                        'type': 'tri3',
                        'nodes': [n1, n2, n3]
                    }
                    element_id += 1
                    
                    # Triangle 2
                    elements[element_id] = {
                        'type': 'tri3',
                        'nodes': [n1, n3, n4]
                    }
                    element_id += 1
        
        return {
            'nodes': nodes,
            'elements': elements,
            'n_nodes': len(nodes),
            'n_elements': len(elements),
            'element_type': element_type
        }
    
    def mesh_circle(self, radius: float, n_radial: int, n_circumferential: int,
                   element_type: str = "quad4") -> Dict:
        """
        Generate structured mesh for circular domain
        
        Args:
            radius: Radius of circle (mm)
            n_radial: Number of elements in radial direction
            n_circumferential: Number of elements in circumferential direction
            element_type: Element type
        """
        nodes = {}
        elements = {}
        
        # Generate nodes
        node_id = 1
        
        # Center node
        nodes[node_id] = {'x': 0, 'y': 0, 'z': 0}
        node_id += 1
        
        # Radial layers
        for i in range(1, n_radial + 1):
            r = radius * i / n_radial
            
            for j in range(n_circumferential):
                theta = 2 * np.pi * j / n_circumferential
                x = r * np.cos(theta)
                y = r * np.sin(theta)
                
                nodes[node_id] = {'x': x, 'y': y, 'z': 0}
                node_id += 1
        
        # Generate elements (simplified - triangular elements from center)
        element_id = 1
        
        for j in range(n_circumferential):
            n1 = 1  # Center
            n2 = 2 + j
            n3 = 2 + (j + 1) % n_circumferential
            
            elements[element_id] = {
                'type': 'tri3',
                'nodes': [n1, n2, n3]
            }
            element_id += 1
        
        return {
            'nodes': nodes,
            'elements': elements,
            'n_nodes': len(nodes),
            'n_elements': len(elements),
            'element_type': 'tri3'
        }
    
    def refine_mesh(self, mesh: Dict, refinement_factor: int = 2) -> Dict:
        """
        Refine existing mesh by subdividing elements
        
        Args:
            mesh: Existing mesh dictionary
            refinement_factor: Factor by which to refine (2 = split each element into 4)
        """
        nodes = mesh['nodes'].copy()
        elements = mesh['elements']
        
        new_elements = {}
        element_id = 1
        node_id = max(nodes.keys()) + 1
        
        for elem_id, elem_data in elements.items():
            elem_type = elem_data['type']
            elem_nodes = elem_data['nodes']
            
            if elem_type == "quad4" and refinement_factor == 2:
                # Get corner nodes
                n1, n2, n3, n4 = elem_nodes
                
                # Get coordinates
                x1, y1 = nodes[n1]['x'], nodes[n1]['y']
                x2, y2 = nodes[n2]['x'], nodes[n2]['y']
                x3, y3 = nodes[n3]['x'], nodes[n3]['y']
                x4, y4 = nodes[n4]['x'], nodes[n4]['y']
                
                # Create midpoint nodes
                n12 = node_id
                nodes[n12] = {'x': (x1+x2)/2, 'y': (y1+y2)/2, 'z': 0}
                node_id += 1
                
                n23 = node_id
                nodes[n23] = {'x': (x2+x3)/2, 'y': (y2+y3)/2, 'z': 0}
                node_id += 1
                
                n34 = node_id
                nodes[n34] = {'x': (x3+x4)/2, 'y': (y3+y4)/2, 'z': 0}
                node_id += 1
                
                n41 = node_id
                nodes[n41] = {'x': (x4+x1)/2, 'y': (y4+y1)/2, 'z': 0}
                node_id += 1
                
                n_center = node_id
                nodes[n_center] = {'x': (x1+x2+x3+x4)/4, 'y': (y1+y2+y3+y4)/4, 'z': 0}
                node_id += 1
                
                # Create 4 new elements
                new_elements[element_id] = {'type': 'quad4', 'nodes': [n1, n12, n_center, n41]}
                element_id += 1
                
                new_elements[element_id] = {'type': 'quad4', 'nodes': [n12, n2, n23, n_center]}
                element_id += 1
                
                new_elements[element_id] = {'type': 'quad4', 'nodes': [n_center, n23, n3, n34]}
                element_id += 1
                
                new_elements[element_id] = {'type': 'quad4', 'nodes': [n41, n_center, n34, n4]}
                element_id += 1
        
        return {
            'nodes': nodes,
            'elements': new_elements,
            'n_nodes': len(nodes),
            'n_elements': len(new_elements),
            'element_type': 'quad4'
        }
    
    def check_mesh_quality(self, mesh: Dict) -> Dict:
        """
        Check mesh quality metrics
        
        Args:
            mesh: Mesh dictionary
        """
        nodes = mesh['nodes']
        elements = mesh['elements']
        
        quality_metrics = {
            'aspect_ratios': [],
            'skewness': [],
            'jacobian': []
        }
        
        for elem_id, elem_data in elements.items():
            elem_type = elem_data['type']
            elem_nodes = elem_data['nodes']
            
            if elem_type == "quad4":
                # Get node coordinates
                coords = [nodes[n] for n in elem_nodes]
                
                # Calculate aspect ratio
                # Distance between opposite sides
                d1 = np.sqrt((coords[0]['x'] - coords[1]['x'])**2 + 
                           (coords[0]['y'] - coords[1]['y'])**2)
                d2 = np.sqrt((coords[1]['x'] - coords[2]['x'])**2 + 
                           (coords[1]['y'] - coords[2]['y'])**2)
                
                aspect_ratio = max(d1, d2) / min(d1, d2) if min(d1, d2) > 0 else 999
                quality_metrics['aspect_ratios'].append(aspect_ratio)
                
                # Calculate skewness (angle deviation from 90 degrees)
                # Simplified: check one corner angle
                v1 = np.array([coords[1]['x'] - coords[0]['x'], 
                              coords[1]['y'] - coords[0]['y']])
                v2 = np.array([coords[3]['x'] - coords[0]['x'], 
                              coords[3]['y'] - coords[0]['y']])
                
                if np.linalg.norm(v1) > 0 and np.linalg.norm(v2) > 0:
                    cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
                    angle = np.degrees(np.arccos(np.clip(cos_angle, -1, 1)))
                    skewness = abs(90 - angle)
                    quality_metrics['skewness'].append(skewness)
        
        # Summary statistics
        if quality_metrics['aspect_ratios']:
            avg_aspect_ratio = np.mean(quality_metrics['aspect_ratios'])
            max_aspect_ratio = np.max(quality_metrics['aspect_ratios'])
        else:
            avg_aspect_ratio = 0
            max_aspect_ratio = 0
        
        if quality_metrics['skewness']:
            avg_skewness = np.mean(quality_metrics['skewness'])
            max_skewness = np.max(quality_metrics['skewness'])
        else:
            avg_skewness = 0
            max_skewness = 0
        
        # Quality assessment
        quality_status = "EXCELLENT"
        if max_aspect_ratio > 5 or max_skewness > 45:
            quality_status = "POOR"
        elif max_aspect_ratio > 3 or max_skewness > 30:
            quality_status = "FAIR"
        elif max_aspect_ratio > 2 or max_skewness > 15:
            quality_status = "GOOD"
        
        return {
            'n_elements_checked': len(elements),
            'aspect_ratio': {
                'average': avg_aspect_ratio,
                'maximum': max_aspect_ratio,
                'acceptable_limit': 3.0
            },
            'skewness': {
                'average': avg_skewness,
                'maximum': max_skewness,
                'acceptable_limit': 30.0
            },
            'overall_quality': quality_status,
            'recommendations': self._get_quality_recommendations(max_aspect_ratio, max_skewness)
        }
    
    def _get_quality_recommendations(self, max_aspect_ratio: float, max_skewness: float) -> List[str]:
        """Generate recommendations based on quality metrics"""
        recommendations = []
        
        if max_aspect_ratio > 5:
            recommendations.append("High aspect ratio detected. Consider refining mesh or adjusting element sizes.")
        
        if max_skewness > 45:
            recommendations.append("High skewness detected. Improve element angles for better accuracy.")
        
        if not recommendations:
            recommendations.append("Mesh quality is acceptable.")
        
        return recommendations
    
    def adaptive_refinement(self, mesh: Dict, stress_results: Dict,
                           threshold: float = 0.8) -> Dict:
        """
        Adaptive mesh refinement based on stress gradients
        
        Args:
            mesh: Current mesh
            stress_results: Stress results for each element
            threshold: Refinement threshold (0-1)
        """
        # Identify elements with high stress gradients
        elements_to_refine = []
        
        if stress_results:
            stresses = list(stress_results.values())
            max_stress = max(stresses)
            
            for elem_id, stress in stress_results.items():
                if stress > threshold * max_stress:
                    elements_to_refine.append(elem_id)
        
        return {
            'elements_to_refine': elements_to_refine,
            'n_elements_to_refine': len(elements_to_refine),
            'refinement_criterion': f"Stress > {threshold * 100}% of maximum"
        }
