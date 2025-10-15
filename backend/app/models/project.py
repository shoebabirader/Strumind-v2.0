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

class Node(Base):
    __tablename__ = "nodes"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    node_id = Column(String, nullable=False)
    x = Column(Integer)  # Using Integer for Float
    y = Column(Integer)
    z = Column(Integer)
    restraints = Column(JSON)  # [ux, uy, uz, rx, ry, rz]
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Element(Base):
    __tablename__ = "elements"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    element_id = Column(String, nullable=False)
    node_i = Column(String, nullable=False)
    node_j = Column(String, nullable=False)
    element_type = Column(String)  # beam, column, brace, truss
    material_id = Column(String)
    section_type = Column(String)
    width = Column(Integer)  # Using Integer for Float
    height = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Material(Base):
    __tablename__ = "materials"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    material_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    E = Column(Integer)  # Young's modulus (MPa)
    nu = Column(Integer)  # Poisson's ratio (stored as integer, divide by 100)
    density = Column(Integer)  # kg/m³
    fy = Column(Integer)  # Yield strength (MPa)
    material_type = Column(String)  # concrete, steel, aluminum
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Section(Base):
    __tablename__ = "sections"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    section_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    section_type = Column(String)  # rectangular, circular, i-section, t-section
    width = Column(Integer)  # Using Integer for Float
    height = Column(Integer)
    diameter = Column(Integer)
    flange_width = Column(Integer)
    flange_thickness = Column(Integer)
    web_thickness = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Load(Base):
    __tablename__ = "loads"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    load_id = Column(String, nullable=False)
    load_type = Column(String)  # nodal, element
    load_case = Column(String)  # DL, LL, WL, EQ, SL
    target_id = Column(String)  # node_id or element_id
    fx = Column(Integer)  # Using Integer for Float
    fy = Column(Integer)
    fz = Column(Integer)
    mx = Column(Integer)
    my = Column(Integer)
    mz = Column(Integer)
    magnitude = Column(Integer)
    direction = Column(String)
    distribution = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
