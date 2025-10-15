"""
Project versioning endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.core.security import get_current_active_user, TokenData

router = APIRouter()


class VersionCreate(BaseModel):
    project_id: int
    commit_message: str
    project_data: Dict[Any, Any]
    model_data: Optional[Dict[Any, Any]] = None
    analysis_results: Optional[Dict[Any, Any]] = None


class VersionResponse(BaseModel):
    id: int
    project_id: int
    version_number: int
    created_at: datetime
    created_by: int
    commit_message: str
    changes_summary: Optional[str] = None


class VersionDetail(VersionResponse):
    project_data: Dict[Any, Any]
    model_data: Optional[Dict[Any, Any]] = None
    analysis_results: Optional[Dict[Any, Any]] = None


# Mock version storage (replace with database)
versions_db: Dict[int, List[Dict]] = {}
version_counter = 0


@router.post("/versions", response_model=VersionResponse)
async def create_version(
    version: VersionCreate,
    current_user: TokenData = Depends(get_current_active_user)
):
    """
    Create a new version of a project
    Automatically creates snapshots before major operations
    """
    global version_counter
    version_counter += 1
    
    # Get current version number for this project
    project_versions = versions_db.get(version.project_id, [])
    version_number = len(project_versions) + 1
    
    # Create version record
    new_version = {
        "id": version_counter,
        "project_id": version.project_id,
        "version_number": version_number,
        "created_at": datetime.utcnow(),
        "created_by": current_user.user_id,
        "commit_message": version.commit_message,
        "project_data": version.project_data,
        "model_data": version.model_data,
        "analysis_results": version.analysis_results,
        "changes_summary": f"Version {version_number}: {version.commit_message}"
    }
    
    # Store version
    if version.project_id not in versions_db:
        versions_db[version.project_id] = []
    versions_db[version.project_id].append(new_version)
    
    return VersionResponse(
        id=new_version["id"],
        project_id=new_version["project_id"],
        version_number=new_version["version_number"],
        created_at=new_version["created_at"],
        created_by=new_version["created_by"],
        commit_message=new_version["commit_message"],
        changes_summary=new_version["changes_summary"]
    )


@router.get("/projects/{project_id}/versions", response_model=List[VersionResponse])
async def list_versions(
    project_id: int,
    current_user: TokenData = Depends(get_current_active_user)
):
    """
    List all versions of a project
    """
    project_versions = versions_db.get(project_id, [])
    
    return [
        VersionResponse(
            id=v["id"],
            project_id=v["project_id"],
            version_number=v["version_number"],
            created_at=v["created_at"],
            created_by=v["created_by"],
            commit_message=v["commit_message"],
            changes_summary=v["changes_summary"]
        )
        for v in project_versions
    ]


@router.get("/versions/{version_id}", response_model=VersionDetail)
async def get_version(
    version_id: int,
    current_user: TokenData = Depends(get_current_active_user)
):
    """
    Get a specific version with full data
    """
    # Find version
    for project_versions in versions_db.values():
        for v in project_versions:
            if v["id"] == version_id:
                return VersionDetail(**v)
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Version not found"
    )


@router.post("/projects/{project_id}/restore/{version_number}")
async def restore_version(
    project_id: int,
    version_number: int,
    current_user: TokenData = Depends(get_current_active_user)
):
    """
    Restore a project to a specific version
    Creates a new version with the restored data
    """
    project_versions = versions_db.get(project_id, [])
    
    # Find the version to restore
    version_to_restore = None
    for v in project_versions:
        if v["version_number"] == version_number:
            version_to_restore = v
            break
    
    if not version_to_restore:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Version {version_number} not found"
        )
    
    # Create new version with restored data
    restored_version = await create_version(
        VersionCreate(
            project_id=project_id,
            commit_message=f"Restored from version {version_number}",
            project_data=version_to_restore["project_data"],
            model_data=version_to_restore["model_data"],
            analysis_results=version_to_restore["analysis_results"]
        ),
        current_user
    )
    
    return {
        "message": f"Project restored to version {version_number}",
        "new_version": restored_version
    }


@router.get("/projects/{project_id}/versions/compare/{version1}/{version2}")
async def compare_versions(
    project_id: int,
    version1: int,
    version2: int,
    current_user: TokenData = Depends(get_current_active_user)
):
    """
    Compare two versions of a project
    Shows what changed between versions
    """
    project_versions = versions_db.get(project_id, [])
    
    v1_data = None
    v2_data = None
    
    for v in project_versions:
        if v["version_number"] == version1:
            v1_data = v
        if v["version_number"] == version2:
            v2_data = v
    
    if not v1_data or not v2_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or both versions not found"
        )
    
    return {
        "version1": version1,
        "version2": version2,
        "version1_date": v1_data["created_at"],
        "version2_date": v2_data["created_at"],
        "changes": {
            "message": f"Comparing version {version1} to version {version2}",
            "note": "Detailed diff implementation would go here"
        }
    }
