"""
Project versioning models to prevent data loss
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class ProjectVersion(Base):
    """
    Version control for projects - stores snapshots of project state
    """
    __tablename__ = "project_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    version_number = Column(Integer, nullable=False)  # Auto-incrementing version
    
    # Version metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))
    commit_message = Column(String)
    
    # Snapshot data
    project_data = Column(JSON)  # Full project state as JSON
    model_data = Column(JSON)  # Structural model snapshot
    analysis_results = Column(JSON)  # Analysis results at this version
    
    # Change tracking
    changes_summary = Column(Text)  # Human-readable summary of changes
    parent_version_id = Column(Integer, ForeignKey("project_versions.id"))
    
    # Relationships
    parent_version = relationship("ProjectVersion", remote_side=[id])
    
    class Config:
        orm_mode = True


class ProjectBackup(Base):
    """
    Automatic backups of projects (separate from manual versions)
    """
    __tablename__ = "project_backups"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    # Backup metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    backup_type = Column(String)  # 'auto', 'manual', 'pre-analysis', 'pre-design'
    
    # Backup data
    full_backup = Column(JSON)  # Complete project backup
    
    # Retention
    expires_at = Column(DateTime(timezone=True))  # Auto-delete old backups
    
    class Config:
        orm_mode = True
