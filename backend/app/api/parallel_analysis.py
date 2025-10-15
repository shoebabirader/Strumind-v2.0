"""
Parallel analysis endpoints
"""
from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any
from app.core.parallel_executor import executor
from app.core.security import get_current_active_user, TokenData
from app.core.websocket_manager import manager

router = APIRouter()


class BatchAnalysisRequest(BaseModel):
    model_data: Dict[Any, Any]
    load_cases: List[Dict[Any, Any]]
    project_id: int


class ParametricStudyRequest(BaseModel):
    base_model: Dict[Any, Any]
    parameter_variations: List[Dict[Any, Any]]
    project_id: int


@router.post("/batch-analysis")
async def run_batch_analysis(
    request: BatchAnalysisRequest,
    background_tasks: BackgroundTasks,
    current_user: TokenData = Depends(get_current_active_user)
):
    """
    Run multiple load cases in parallel
    Utilizes all available CPU cores for faster analysis
    """
    
    # Send initial progress
    await manager.send_analysis_progress(request.project_id, {
        "status": "started",
        "total_cases": len(request.load_cases),
        "completed": 0
    })
    
    # Execute batch analysis
    results = await executor.execute_batch_analysis(
        request.model_data,
        request.load_cases
    )
    
    # Send completion progress
    await manager.send_analysis_progress(request.project_id, {
        "status": "completed",
        "total_cases": len(request.load_cases),
        "completed": len(request.load_cases)
    })
    
    return {
        "message": "Batch analysis completed",
        "load_cases_analyzed": len(request.load_cases),
        "results": results,
        "execution_info": {
            "parallel_workers": executor.max_workers,
            "execution_mode": "parallel"
        }
    }


@router.post("/parametric-study")
async def run_parametric_study(
    request: ParametricStudyRequest,
    current_user: TokenData = Depends(get_current_active_user)
):
    """
    Run parametric study with multiple parameter variations
    Executes all variations in parallel
    """
    
    await manager.send_analysis_progress(request.project_id, {
        "status": "started",
        "total_variations": len(request.parameter_variations),
        "completed": 0
    })
    
    results = await executor.execute_parametric_study(
        request.base_model,
        request.parameter_variations
    )
    
    await manager.send_analysis_progress(request.project_id, {
        "status": "completed",
        "total_variations": len(request.parameter_variations),
        "completed": len(request.parameter_variations)
    })
    
    return {
        "message": "Parametric study completed",
        "variations_analyzed": len(request.parameter_variations),
        "results": results,
        "summary": _generate_parametric_summary(results)
    }


@router.get("/execution/status")
async def get_execution_status(current_user: TokenData = Depends(get_current_active_user)):
    """Get status of parallel execution system"""
    return {
        "max_workers": executor.max_workers,
        "tasks": executor.get_all_tasks(),
        "system_info": {
            "cpu_count": executor.max_workers,
            "execution_mode": "multi-process"
        }
    }


@router.get("/execution/capabilities")
async def get_execution_capabilities():
    """Get parallel execution capabilities"""
    import multiprocessing
    
    return {
        "cpu_cores": multiprocessing.cpu_count(),
        "max_parallel_analyses": executor.max_workers,
        "supported_features": [
            "batch_analysis",
            "parametric_study",
            "optimization",
            "load_case_combinations"
        ],
        "performance_estimate": {
            "single_analysis": "1x speed",
            "parallel_analysis": f"{executor.max_workers}x speed (theoretical)",
            "actual_speedup": f"{executor.max_workers * 0.7:.1f}x (typical)"
        }
    }


def _generate_parametric_summary(results: List[dict]) -> dict:
    """Generate summary of parametric study results"""
    if not results:
        return {}
    
    return {
        "total_variations": len(results),
        "successful": sum(1 for r in results if r.get("success", False)),
        "failed": sum(1 for r in results if not r.get("success", False)),
        "note": "Detailed analysis of each variation available in results"
    }
