from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Dict, List
from app.ml.continuous_learning import ContinuousLearningPipeline
from app.ml.design_assistant import DesignAssistantNN

router = APIRouter()
learning_pipeline = ContinuousLearningPipeline()

class FeedbackSubmission(BaseModel):
    model_config = {"protected_namespaces": ()}
    project_id: int
    model_data: Dict
    user_feedback: Dict
    approved: bool

class RetrainingRequest(BaseModel):
    model_config = {"protected_namespaces": ()}
    model_type: str
    epochs: int = 10

@router.post("/feedback/submit")
def submit_feedback(feedback: FeedbackSubmission):
    """Submit user feedback for continuous learning"""
    learning_pipeline.ingest_data(
        feedback.model_data,
        {**feedback.user_feedback, "approved": feedback.approved}
    )
    return {"status": "feedback_received"}

@router.post("/retrain")
def trigger_retraining(request: RetrainingRequest):
    """Trigger model retraining"""
    result = learning_pipeline.retrain_model(
        request.model_type,
        DesignAssistantNN,
        request.epochs
    )
    return result

@router.get("/models/versions")
def list_model_versions():
    """List all model versions"""
    return {"versions": learning_pipeline.model_versions}

@router.get("/models/{model_type}/latest")
def get_latest_model(model_type: str):
    """Get latest model version path"""
    path = learning_pipeline.get_model_version(model_type, "latest")
    return {"model_type": model_type, "path": path}
