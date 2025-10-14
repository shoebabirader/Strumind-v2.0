from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    client = Column(String)
    location = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    models = relationship("StructuralModel", back_populates="project")

class StructuralModel(Base):
    __tablename__ = "models"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    geometry_data = Column(JSON)
    materials = Column(JSON)
    sections = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    project = relationship("Project", back_populates="models")
    analysis_results = relationship("AnalysisResult", back_populates="model")

class AnalysisResult(Base):
    __tablename__ = "analysis_results"
    
    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("models.id"))
    analysis_type = Column(String)
    results_json = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    model = relationship("StructuralModel", back_populates="analysis_results")
