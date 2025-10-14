from typing import Dict, List
import json

class VisualizationEngine:
    """Generate 3D visualization data for Three.js frontend"""
    
    def generate_threejs_scene(self, model_data: Dict) -> Dict:
        """Convert structural model to Three.js scene format"""
        scene = {
            "metadata": {
                "version": 4.5,
                "type": "Object",
                "generator": "StruMind"
            },
            "geometries": [],
            "materials": [],
            "objects": []
        }
        
        # Generate geometries
        scene["geometries"] = self._generate_geometries(model_data)
        
        # Generate materials
        scene["materials"] = self._generate_materials(model_data)
        
        # Generate objects
        scene["objects"] = self._generate_objects(model_data)
        
        return scene
    
    def generate_stress_visualization(self, analysis_results: Dict) -> Dict:
        """Generate stress contour visualization data"""
        return {
            "type": "stress_contour",
            "values": analysis_results.get('stresses', []),
            "colormap": "jet",
            "range": {
                "min": min(analysis_results.get('stresses', [0])),
                "max": max(analysis_results.get('stresses', [1]))
            }
        }
    
    def generate_deformation_visualization(self, analysis_results: Dict) -> Dict:
        """Generate deformed shape visualization"""
        return {
            "type": "deformed_shape",
            "displacements": analysis_results.get('displacements', []),
            "scale_factor": 10.0,
            "animation": True
        }
    
    def _generate_geometries(self, model_data: Dict) -> List[Dict]:
        """Generate Three.js geometries"""
        geometries = []
        
        # Box geometry for columns
        geometries.append({
            "uuid": "box-geometry-1",
            "type": "BoxGeometry",
            "width": 0.3,
            "height": 3.0,
            "depth": 0.3
        })
        
        # Box geometry for beams
        geometries.append({
            "uuid": "box-geometry-2",
            "type": "BoxGeometry",
            "width": 0.3,
            "height": 0.45,
            "depth": 5.0
        })
        
        return geometries
    
    def _generate_materials(self, model_data: Dict) -> List[Dict]:
        """Generate Three.js materials"""
        return [
            {
                "uuid": "material-concrete",
                "type": "MeshStandardMaterial",
                "color": 0xcccccc,
                "roughness": 0.7,
                "metalness": 0.0
            },
            {
                "uuid": "material-steel",
                "type": "MeshStandardMaterial",
                "color": 0x888888,
                "roughness": 0.3,
                "metalness": 0.8
            }
        ]
    
    def _generate_objects(self, model_data: Dict) -> List[Dict]:
        """Generate Three.js objects"""
        objects = []
        
        # Generate columns
        for i, col in enumerate(model_data.get('columns', [])):
            objects.append({
                "uuid": f"column-{i}",
                "type": "Mesh",
                "geometry": "box-geometry-1",
                "material": "material-concrete",
                "position": [col.get('x', 0), col.get('y', 0), col.get('z', 0)]
            })
        
        # Generate beams
        for i, beam in enumerate(model_data.get('beams', [])):
            objects.append({
                "uuid": f"beam-{i}",
                "type": "Mesh",
                "geometry": "box-geometry-2",
                "material": "material-concrete",
                "position": [beam.get('x', 0), beam.get('y', 0), beam.get('z', 0)]
            })
        
        return objects
