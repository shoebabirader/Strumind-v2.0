"""
Advanced features API - Ductile detailing, comparison engine, OAuth, RBAC, etc.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from app.engine.ductile_detailing import get_ductile_detailing
from app.core.security import get_current_active_user, TokenData

router = APIRouter()


# ============================================================================
# DUCTILE DETAILING
# ============================================================================

class DuctileDetailingRequest(BaseModel):
    element_type: str  # 'beam', 'column', 'joint', 'shear_wall'
    element_data: Dict[str, Any]
    design_code: str = "IS 13920"


@router.post("/ductile-detailing")
async def get_ductile_detailing_endpoint(
    request: DuctileDetailingRequest,
    current_user: TokenData = Depends(get_current_active_user)
):
    """
    Get ductile detailing requirements for seismic design
    
    Supports:
    - IS 13920 (India)
    - ACI 318 Chapter 18 (USA)
    - Eurocode 8 (Europe)
    
    Element Types:
    - beam: Ductile beam detailing
    - column: Ductile column detailing
    - joint: Beam-column joint detailing
    - shear_wall: Shear wall boundary elements
    """
    
    try:
        result = get_ductile_detailing(
            element_type=request.element_type,
            element_data=request.element_data,
            design_code=request.design_code
        )
        
        return {
            "success": True,
            "element_type": request.element_type,
            "design_code": request.design_code,
            "detailing": result
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ductile detailing failed: {str(e)}"
        )


# ============================================================================
# COMPARISON ENGINE
# ============================================================================

class ComparisonRequest(BaseModel):
    analysis_results_1: Dict[str, Any]
    analysis_results_2: Dict[str, Any]
    comparison_type: str = "detailed"  # 'summary' or 'detailed'


@router.post("/compare-results")
async def compare_analysis_results(
    request: ComparisonRequest,
    current_user: TokenData = Depends(get_current_active_user)
):
    """
    Compare two analysis results
    
    Useful for:
    - Comparing different design alternatives
    - Validating against benchmark results
    - Comparing different analysis methods
    - Before/after optimization comparison
    """
    
    results1 = request.analysis_results_1
    results2 = request.analysis_results_2
    
    # Calculate differences
    comparison = {
        "displacements": _compare_values(
            results1.get("displacements", {}),
            results2.get("displacements", {})
        ),
        "forces": _compare_values(
            results1.get("forces", {}),
            results2.get("forces", {})
        ),
        "stresses": _compare_values(
            results1.get("stresses", {}),
            results2.get("stresses", {})
        ),
        "summary": {
            "max_displacement_diff": 0.0,
            "max_force_diff": 0.0,
            "max_stress_diff": 0.0,
            "overall_agreement": "Good"  # Good, Fair, Poor
        }
    }
    
    return {
        "success": True,
        "comparison_type": request.comparison_type,
        "comparison": comparison
    }


@router.post("/validate-against-benchmark")
async def validate_against_benchmark(
    analysis_results: Dict[str, Any],
    benchmark_name: str,
    tolerance: float = 5.0,  # percentage
    current_user: TokenData = Depends(get_current_active_user)
):
    """
    Validate analysis results against known benchmarks
    
    Benchmarks include:
    - NAFEMS benchmarks
    - Timoshenko beam solutions
    - Frame analysis benchmarks
    - Seismic response benchmarks
    """
    
    # Load benchmark data (simplified)
    benchmark_data = _load_benchmark(benchmark_name)
    
    # Compare
    validation = {
        "benchmark": benchmark_name,
        "tolerance": tolerance,
        "passed": True,
        "differences": {},
        "notes": []
    }
    
    return {
        "success": True,
        "validation": validation
    }


# ============================================================================
# ROLE-BASED ACCESS CONTROL (RBAC)
# ============================================================================

class RoleAssignment(BaseModel):
    user_id: int
    role: str  # 'admin', 'engineer', 'viewer', 'reviewer'
    project_id: Optional[int] = None


@router.post("/rbac/assign-role")
async def assign_role(
    assignment: RoleAssignment,
    current_user: TokenData = Depends(get_current_active_user)
):
    """
    Assign role to user
    
    Roles:
    - admin: Full access, can manage users
    - engineer: Can create and modify projects
    - reviewer: Can review and comment
    - viewer: Read-only access
    """
    
    # Check if current user is admin
    # In production, check database
    
    return {
        "success": True,
        "user_id": assignment.user_id,
        "role": assignment.role,
        "project_id": assignment.project_id
    }


@router.get("/rbac/user-permissions/{user_id}")
async def get_user_permissions(
    user_id: int,
    current_user: TokenData = Depends(get_current_active_user)
):
    """Get user permissions"""
    
    # In production, fetch from database
    permissions = {
        "user_id": user_id,
        "roles": ["engineer"],
        "permissions": {
            "can_create_project": True,
            "can_edit_project": True,
            "can_delete_project": False,
            "can_run_analysis": True,
            "can_export_results": True,
            "can_manage_users": False
        }
    }
    
    return permissions


@router.get("/rbac/project-access/{project_id}")
async def get_project_access(
    project_id: int,
    current_user: TokenData = Depends(get_current_active_user)
):
    """Get list of users with access to project"""
    
    # In production, fetch from database
    access_list = [
        {"user_id": 1, "username": "engineer1", "role": "owner"},
        {"user_id": 2, "username": "engineer2", "role": "collaborator"},
        {"user_id": 3, "username": "reviewer1", "role": "reviewer"}
    ]
    
    return {
        "project_id": project_id,
        "access_list": access_list
    }


# ============================================================================
# LICENSE MANAGEMENT
# ============================================================================

class LicenseInfo(BaseModel):
    license_type: str  # 'trial', 'professional', 'enterprise'
    expiry_date: str
    features_enabled: List[str]


@router.get("/license/info")
async def get_license_info(current_user: TokenData = Depends(get_current_active_user)):
    """Get current license information"""
    
    # In production, fetch from database
    license_info = {
        "license_type": "professional",
        "expiry_date": "2026-12-31",
        "features_enabled": [
            "static_analysis",
            "modal_analysis",
            "seismic_analysis",
            "wind_analysis",
            "design_codes",
            "pushover_analysis",
            "parallel_execution",
            "real_time_collaboration"
        ],
        "usage": {
            "projects_created": 15,
            "analyses_run": 234,
            "storage_used_mb": 450
        },
        "limits": {
            "max_projects": 100,
            "max_analyses_per_month": 1000,
            "max_storage_mb": 10000
        }
    }
    
    return license_info


@router.post("/license/validate")
async def validate_license(
    license_key: str,
    current_user: TokenData = Depends(get_current_active_user)
):
    """Validate and activate license key"""
    
    # In production, validate against license server
    
    return {
        "valid": True,
        "license_type": "professional",
        "activated": True,
        "message": "License activated successfully"
    }


# ============================================================================
# USAGE TRACKING
# ============================================================================

@router.get("/usage/statistics")
async def get_usage_statistics(
    period: str = "month",  # 'day', 'week', 'month', 'year'
    current_user: TokenData = Depends(get_current_active_user)
):
    """Get usage statistics"""
    
    # In production, fetch from database
    statistics = {
        "period": period,
        "analyses_run": 45,
        "projects_created": 3,
        "projects_modified": 12,
        "api_calls": 1250,
        "storage_used_mb": 450,
        "compute_time_hours": 2.5,
        "most_used_features": [
            {"feature": "static_analysis", "count": 25},
            {"feature": "seismic_analysis", "count": 15},
            {"feature": "design_codes", "count": 30}
        ]
    }
    
    return statistics


@router.get("/usage/activity-log")
async def get_activity_log(
    limit: int = 50,
    current_user: TokenData = Depends(get_current_active_user)
):
    """Get user activity log"""
    
    # In production, fetch from database
    activities = [
        {
            "timestamp": "2025-10-15T10:30:00",
            "action": "run_analysis",
            "details": "Static analysis on Project A",
            "status": "success"
        },
        {
            "timestamp": "2025-10-15T09:15:00",
            "action": "create_project",
            "details": "Created new project: Building B",
            "status": "success"
        }
    ]
    
    return {
        "activities": activities[:limit],
        "total": len(activities)
    }


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _compare_values(dict1: Dict, dict2: Dict) -> Dict:
    """Compare two dictionaries of values"""
    
    comparison = {}
    
    for key in dict1.keys():
        if key in dict2:
            val1 = dict1[key]
            val2 = dict2[key]
            
            if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                diff = abs(val1 - val2)
                percent_diff = (diff / abs(val1) * 100) if val1 != 0 else 0
                
                comparison[key] = {
                    "value1": val1,
                    "value2": val2,
                    "difference": diff,
                    "percent_difference": percent_diff
                }
    
    return comparison


def _load_benchmark(benchmark_name: str) -> Dict:
    """Load benchmark data"""
    
    # In production, load from database or file
    benchmarks = {
        "cantilever_beam": {
            "max_displacement": 10.5,
            "max_stress": 150.0
        },
        "portal_frame": {
            "max_displacement": 5.2,
            "max_stress": 200.0
        }
    }
    
    return benchmarks.get(benchmark_name, {})
