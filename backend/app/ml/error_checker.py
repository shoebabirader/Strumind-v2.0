import numpy as np
from sklearn.ensemble import IsolationForest
from typing import Dict, List

class ErrorChecker:
    """Anomaly detection for modeling errors and code violations"""
    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.is_trained = False
    
    def train(self, training_data: List[Dict]):
        """Train anomaly detection model on historical data"""
        features = [self._extract_features(data) for data in training_data]
        X = np.array(features)
        self.model.fit(X)
        self.is_trained = True
    
    def check_model(self, model_data: Dict) -> Dict:
        """Check for modeling errors and code violations"""
        errors = []
        warnings = []
        
        # Geometry checks
        if 'nodes' in model_data:
            geom_errors = self._check_geometry(model_data['nodes'], model_data.get('elements', []))
            errors.extend(geom_errors)
        
        # Load application checks
        if 'loads' in model_data:
            load_errors = self._check_loads(model_data['loads'])
            warnings.extend(load_errors)
        
        # Code compliance checks
        if 'design' in model_data:
            code_errors = self._check_code_compliance(model_data['design'])
            errors.extend(code_errors)
        
        # Anomaly detection
        if self.is_trained:
            features = self._extract_features(model_data)
            anomaly_score = self.model.score_samples([features])[0]
            if anomaly_score < -0.5:
                warnings.append({
                    "type": "anomaly",
                    "message": "Model parameters are unusual compared to typical designs",
                    "severity": "warning"
                })
        
        return {
            "errors": errors,
            "warnings": warnings,
            "status": "failed" if errors else "passed"
        }
    
    def _check_geometry(self, nodes: List, elements: List) -> List[Dict]:
        """Check for geometry issues"""
        errors = []
        
        # Check for duplicate nodes
        node_coords = [(n['x'], n['y'], n['z']) for n in nodes]
        if len(node_coords) != len(set(node_coords)):
            errors.append({
                "type": "geometry",
                "message": "Duplicate nodes detected",
                "severity": "error"
            })
        
        # Check for zero-length elements
        for elem in elements:
            if elem.get('length', 1) < 1e-6:
                errors.append({
                    "type": "geometry",
                    "message": f"Zero-length element detected: {elem.get('id')}",
                    "severity": "error"
                })
        
        return errors
    
    def _check_loads(self, loads: List) -> List[Dict]:
        """Check for load application issues"""
        warnings = []
        
        for load in loads:
            magnitude = abs(load.get('magnitude', 0))
            if magnitude > 1e6:  # Unreasonably large load
                warnings.append({
                    "type": "load",
                    "message": f"Unusually large load magnitude: {magnitude}",
                    "severity": "warning"
                })
        
        return warnings
    
    def _check_code_compliance(self, design: Dict) -> List[Dict]:
        """Check for code violations"""
        errors = []
        
        # Check minimum reinforcement
        if 'reinforcement_ratio' in design:
            ratio = design['reinforcement_ratio']
            if ratio < 0.002:  # Minimum for IS 456
                errors.append({
                    "type": "code",
                    "message": f"Reinforcement ratio {ratio} below minimum (0.002)",
                    "severity": "error"
                })
        
        return errors
    
    def _extract_features(self, data: Dict) -> np.ndarray:
        """Extract features for anomaly detection"""
        return np.array([
            len(data.get('nodes', [])),
            len(data.get('elements', [])),
            len(data.get('loads', [])),
            data.get('max_displacement', 0),
            data.get('max_stress', 0),
            0, 0, 0, 0, 0  # Padding
        ])
