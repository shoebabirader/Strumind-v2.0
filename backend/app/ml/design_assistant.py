import torch
import torch.nn as nn
import numpy as np
from typing import Dict, Tuple

class DesignAssistantNN(nn.Module):
    """Neural network for suggesting optimal sections and reinforcement"""
    def __init__(self, input_dim: int = 10, hidden_dim: int = 128):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 6)  # Output: width, depth, main_bar_dia, main_bar_count, stirrup_dia, stirrup_spacing
        )
    
    def forward(self, x):
        return self.network(x)

class DesignAssistant:
    def __init__(self, model_path: str = None):
        self.model = DesignAssistantNN()
        if model_path:
            self.model.load_state_dict(torch.load(model_path))
        self.model.eval()
    
    def suggest_design(self, forces: Dict, span: float, design_code: str) -> Dict:
        """Suggest optimal section and reinforcement based on forces"""
        # Prepare input features
        features = self._prepare_features(forces, span, design_code)
        
        with torch.no_grad():
            tensor = torch.from_numpy(features).float().unsqueeze(0)
            predictions = self.model(tensor)
        
        return self._parse_predictions(predictions[0].numpy())
    
    def _prepare_features(self, forces: Dict, span: float, design_code: str) -> np.ndarray:
        """Convert input data to feature vector"""
        code_encoding = {"IS456": 0, "ACI318": 1, "IS800": 2, "AISC": 3}.get(design_code, 0)
        
        features = np.array([
            forces.get('M', 0) / 1e6,  # Moment in kNm
            forces.get('V', 0) / 1e3,  # Shear in kN
            forces.get('P', 0) / 1e3,  # Axial in kN
            span / 1000,  # Span in m
            code_encoding,
            forces.get('T', 0) / 1e6,  # Torsion in kNm
            0, 0, 0, 0  # Padding
        ])
        return features
    
    def _parse_predictions(self, predictions: np.ndarray) -> Dict:
        """Parse neural network output to design parameters"""
        width = int(np.clip(predictions[0] * 100, 200, 600))
        depth = int(np.clip(predictions[1] * 100, 300, 900))
        main_bar_dia = int(np.clip(predictions[2] * 10, 12, 32))
        main_bar_count = int(np.clip(predictions[3] * 2, 2, 12))
        stirrup_dia = int(np.clip(predictions[4] * 5, 8, 16))
        stirrup_spacing = int(np.clip(predictions[5] * 50, 100, 300))
        
        return {
            "section": {"width": width, "depth": depth},
            "main_reinforcement": f"{main_bar_count}-{main_bar_dia}mm",
            "stirrups": f"{stirrup_dia}mm @ {stirrup_spacing}mm c/c",
            "confidence": 0.85
        }
