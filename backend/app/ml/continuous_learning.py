import torch
import torch.optim as optim
from datetime import datetime
from typing import Dict, List
import json
from pathlib import Path

# SECURITY FIX: Use timezone-aware datetime
from app.core.datetime_utils import utc_now
class ContinuousLearningPipeline:
    """Manages continuous learning workflow for ML models"""
    def __init__(self, model_registry_path: str = "./ml_models"):
        self.registry_path = Path(model_registry_path)
        self.registry_path.mkdir(exist_ok=True)
        self.training_queue = []
        self.model_versions = {}
    
    def ingest_data(self, project_data: Dict, user_feedback: Dict):
        """Collect anonymized project data for training"""
        anonymized_data = self._anonymize_data(project_data)
        
        training_sample = {
            "data": anonymized_data,
            "feedback": user_feedback,
            "timestamp": utc_now().isoformat(),
            "approved": user_feedback.get("approved", False)
        }
        
        self.training_queue.append(training_sample)
        
        # Save to disk
        self._save_training_sample(training_sample)
    
    def retrain_model(self, model_type: str, model_class, epochs: int = 10):
        """Retrain model with accumulated data"""
        # Load training data
        approved_samples = [s for s in self.training_queue if s["approved"]]
        
        if len(approved_samples) < 10:
            return {"status": "insufficient_data", "samples": len(approved_samples)}
        
        # Initialize model
        model = model_class()
        optimizer = optim.Adam(model.parameters(), lr=0.001)
        criterion = torch.nn.MSELoss()
        
        # Training loop
        model.train()
        for epoch in range(epochs):
            total_loss = 0
            for sample in approved_samples:
                # Extract features and targets from sample
                input_features = sample.get('features', [])
                target_values = sample.get('targets', [])
                
                # Convert to tensors
                inputs = torch.tensor(input_features, dtype=torch.float32).unsqueeze(0)
                targets = torch.tensor(target_values, dtype=torch.float32).unsqueeze(0)
                
                # Ensure correct dimensions
                if inputs.shape[1] != 10:
                    # Pad or truncate to expected size
                    if inputs.shape[1] < 10:
                        padding = torch.zeros(1, 10 - inputs.shape[1])
                        inputs = torch.cat([inputs, padding], dim=1)
                    else:
                        inputs = inputs[:, :10]
                
                if targets.shape[1] != 6:
                    # Pad or truncate to expected size
                    if targets.shape[1] < 6:
                        padding = torch.zeros(1, 6 - targets.shape[1])
                        targets = torch.cat([targets, padding], dim=1)
                    else:
                        targets = targets[:, :6]
                
                optimizer.zero_grad()
                outputs = model(inputs)
                loss = criterion(outputs, targets)
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item()
        
        # Save new model version
        version = self._save_model_version(model, model_type)
        
        return {
            "status": "training_complete",
            "model_type": model_type,
            "version": version,
            "samples_used": len(approved_samples)
        }
    
    def get_model_version(self, model_type: str, version: str = "latest"):
        """Retrieve specific model version"""
        if version == "latest":
            versions = list(self.registry_path.glob(f"{model_type}_v*.pt"))
            if not versions:
                return None
            latest = max(versions, key=lambda p: p.stat().st_mtime)
            return str(latest)
        
        return str(self.registry_path / f"{model_type}_{version}.pt")
    
    def _anonymize_data(self, data: Dict) -> Dict:
        """Remove PII and sensitive information"""
        anonymized = data.copy()
        anonymized.pop("client_name", None)
        anonymized.pop("project_location", None)
        anonymized.pop("user_id", None)
        return anonymized
    
    def _save_training_sample(self, sample: Dict):
        """Save training sample to disk"""
        # SECURITY FIX: Sanitize timestamp to prevent path traversal
        timestamp = sample["timestamp"].replace(":", "-").replace("/", "-").replace("\\", "-")
        # Validate timestamp format
        if not timestamp.replace("-", "").replace("T", "").replace(".", "").isalnum():
            raise ValueError("Invalid timestamp format")
        
        # SECURITY FIX: Ensure filepath stays within registry_path
        filepath = self.registry_path / f"sample_{timestamp}.json"
        filepath = filepath.resolve()
        
        # Verify the resolved path is still within registry_path
        if not str(filepath).startswith(str(self.registry_path.resolve())):
            raise ValueError("Path traversal attempt detected")
        
        with open(filepath, 'w') as f:
            json.dump(sample, f)
    
    def _save_model_version(self, model, model_type: str) -> str:
        """Save model with version tracking"""
        # SECURITY FIX: Sanitize model_type to prevent path traversal
        # Only allow alphanumeric and underscore
        if not model_type.replace("_", "").isalnum():
            raise ValueError("Invalid model_type. Only alphanumeric and underscore allowed.")
        
        version = utc_now().strftime("%Y%m%d_%H%M%S")
        filepath = self.registry_path / f"{model_type}_v{version}.pt"
        
        # SECURITY FIX: Verify path is within registry_path
        filepath = filepath.resolve()
        if not str(filepath).startswith(str(self.registry_path.resolve())):
            raise ValueError("Path traversal attempt detected")
        
        torch.save(model.state_dict(), filepath)
        
        # Update version registry
        self.model_versions[model_type] = version
        
        return version
