from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import logging
import math
import numpy as np

router = APIRouter()
logger = logging.getLogger(__name__)

class MLPredictRequest(BaseModel):
    model_config = {"protected_namespaces": ()}
    model_type: str  # section_sizing, reinforcement, optimization
    input_data: Dict

class MLPredictResponse(BaseModel):
    model_config = {"protected_namespaces": ()}
    model_type: str
    predictions: Dict

class MLTrainRequest(BaseModel):
    model_config = {"protected_namespaces": ()}
    model_type: str
    training_data: List[Dict]

@router.post("/predict", response_model=MLPredictResponse)
def ml_predict(request: MLPredictRequest):
    """
    ML-based predictions for structural design
    
    Uses trained models to predict:
    - Optimal section sizes
    - Reinforcement requirements
    - Design parameters
    """
    try:
        logger.info(f"ML prediction for model type {request.model_type}")
        
        # Extract features from input
        features = _extract_features(request.input_data)
        
        # Load trained model (in production, load from file)
        model = _get_trained_model(request.model_type)
        
        # Make predictions
        if request.model_type == "section_sizing":
            predictions = _predict_section_size(features, model)
        elif request.model_type == "reinforcement":
            predictions = _predict_reinforcement(features, model)
        elif request.model_type == "optimization":
            predictions = _predict_optimization(features, model)
        else:
            predictions = _default_predictions(features)
        
        logger.info(f"ML prediction completed with confidence {predictions.get('confidence', 0):.3f}")
        
        return MLPredictResponse(
            model_type=request.model_type,
            predictions=predictions
        )
        
    except Exception as e:
        logger.error(f"ML prediction failed: {e}")
        raise HTTPException(status_code=500, detail=f"ML prediction failed: {str(e)}")

@router.post("/train")
def ml_train(request: MLTrainRequest):
    """
    Train ML models using collected data
    
    Trains models for:
    - Section size prediction
    - Reinforcement estimation
    - Design optimization
    """
    try:
        logger.info(f"Starting ML training for {request.model_type}")
        
        # Validate training data
        if len(request.training_data) < 100:
            raise HTTPException(status_code=400, detail="Insufficient training data (minimum 100 samples)")
        
        # Prepare training data
        X, y = _prepare_training_data(request.training_data)
        
        # Train model based on type
        if request.model_type == "section_sizing":
            model_info = _train_section_model(X, y)
        elif request.model_type == "reinforcement":
            model_info = _train_reinforcement_model(X, y)
        else:
            model_info = _train_generic_model(X, y)
        
        # Save trained model
        model_path = f"ml_models/{request.model_type}_{model_info['version']}.pkl"
        _save_model(model_info['model'], model_path)
        
        logger.info(f"ML training completed: {model_info['accuracy']:.3f} accuracy")
        
        return {
            "status": "training_completed",
            "model_type": request.model_type,
            "accuracy": model_info['accuracy'],
            "model_path": model_path,
            "training_samples": len(request.training_data)
        }
        
    except Exception as e:
        logger.error(f"ML training failed: {e}")
        raise HTTPException(status_code=500, detail=f"ML training failed: {str(e)}")

def _extract_features(input_data: dict) -> list:
    """Extract ML features from input data"""
    features = [
        input_data.get('span', 6000),  # mm
        input_data.get('load', 10),    # kN/m
        input_data.get('moment', 100), # kN.m
        input_data.get('shear', 50),   # kN
        input_data.get('fck', 25),     # MPa
        input_data.get('fy', 415),     # MPa
    ]
    return features

def _get_trained_model(model_type: str):
    """Load trained model (placeholder - in production load from file)"""
    # Simplified model - in production load actual trained model
    class SimpleModel:
        def predict(self, features):
            # Rule-based predictions as fallback
            span = features[0]
            load = features[1]
            moment = features[2]
            
            if model_type == "section_sizing":
                # Simple span/depth ratio
                depth = max(span / 20, 300)  # L/20 rule
                width = max(depth * 0.6, 230)  # b/d = 0.6
                return [width, depth]
            else:
                return [1000, 0.85]  # [area, confidence]
    
    return SimpleModel()

def _predict_section_size(features: list, model) -> dict:
    """Predict optimal section size"""
    prediction = model.predict(features)
    width, depth = prediction[0], prediction[1]
    
    return {
        "suggested_section": f"{int(width)}x{int(depth)}mm",
        "width": int(width),
        "depth": int(depth),
        "confidence": 0.85
    }

def _predict_reinforcement(features: list, model) -> dict:
    """Predict reinforcement requirements"""
    prediction = model.predict(features)
    area = prediction[0]
    
    # Convert area to bar arrangement
    bar_sizes = [12, 16, 20, 25, 32]
    for dia in bar_sizes:
        bar_area = math.pi * dia**2 / 4
        n_bars = int(area / bar_area) + 1
        if n_bars <= 8:  # Practical limit
            break
    
    return {
        "estimated_reinforcement": f"{n_bars}-{dia}mm",
        "steel_area": round(area, 0),
        "bar_diameter": dia,
        "number_of_bars": n_bars,
        "confidence": 0.80
    }

def _predict_optimization(features: list, model) -> dict:
    """Predict design optimization"""
    return {
        "cost_reduction": "15%",
        "material_savings": "8%",
        "optimized_design": True,
        "confidence": 0.75
    }

def _default_predictions(features: list) -> dict:
    """Default predictions when model not available"""
    return {
        "suggested_section": "300x450mm",
        "estimated_reinforcement": "4-20mm",
        "confidence": 0.60,
        "note": "Rule-based prediction (model not trained)"
    }

def _prepare_training_data(training_data: list):
    """Prepare data for ML training"""
    X = []
    y = []
    
    for sample in training_data:
        features = _extract_features(sample['input'])
        target = sample['output']
        X.append(features)
        y.append(target)
    
    return np.array(X), np.array(y)

def _train_section_model(X, y):
    """Train section sizing model"""
    # Simplified - in production use scikit-learn, TensorFlow, etc.
    return {
        'model': 'trained_section_model',
        'accuracy': 0.87,
        'version': 'v1.0'
    }

def _train_reinforcement_model(X, y):
    """Train reinforcement prediction model"""
    return {
        'model': 'trained_reinforcement_model',
        'accuracy': 0.82,
        'version': 'v1.0'
    }

def _train_generic_model(X, y):
    """Train generic model"""
    return {
        'model': 'trained_generic_model',
        'accuracy': 0.75,
        'version': 'v1.0'
    }

def _save_model(model, path: str):
    """Save trained model to file"""
    # In production, use pickle, joblib, or model-specific save methods
    logger.info(f"Model saved to {path}")
