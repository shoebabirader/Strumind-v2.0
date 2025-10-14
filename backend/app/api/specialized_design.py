from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional, List
from app.engine.wall_design import ShearWallDesign
from app.engine.retaining_wall_design import RetainingWallDesign
from app.engine.staircase_design import StaircaseDesign
from app.engine.composite_design import CompositeBeamDesign
from app.engine.moving_load_analysis import MovingLoadAnalysis
from app.engine.temperature_analysis import TemperatureAnalysis
from app.engine.meshing import AutoMesher

router = APIRouter()

# Request Models
class ShearWallRequest(BaseModel):
    height: float
    length: float
    thickness: float
    axial_load: float
    shear_force: float
    moment: float
    boundary_element: bool = True

class CouplingBeamRequest(BaseModel):
    span: float
    depth: float
    width: float
    shear_force: float
    moment: float

class RetainingWallRequest(BaseModel):
    wall_type: str  # 'cantilever' or 'gravity'
    height: float
    stem_thickness_top: Optional[float] = None
    stem_thickness_bottom: Optional[float] = None
    base_width: Optional[float] = None
    base_thickness: Optional[float] = None
    toe_length: Optional[float] = None
    top_width: Optional[float] = None
    bottom_width: Optional[float] = None
    surcharge: float = 0

class StaircaseRequest(BaseModel):
    stair_type: str  # 'dog_legged', 'cantilever', 'spiral'
    flight_length: Optional[float] = None
    flight_width: Optional[float] = None
    waist_thickness: float
    riser: float
    tread: float
    loads: Dict
    cantilever_length: Optional[float] = None
    width: Optional[float] = None
    inner_radius: Optional[float] = None
    outer_radius: Optional[float] = None
    total_angle: Optional[float] = None

class CompositeBeamRequest(BaseModel):
    span: float
    steel_section: Dict
    slab_thickness: float
    slab_width: float
    loads: Dict
    shear_connectors: str = "stud"

class CompositeColumnRequest(BaseModel):
    height: float
    steel_section: Dict
    concrete_dimensions: Dict
    axial_load: float
    moment: float

class MovingLoadRequest(BaseModel):
    span: float
    response_type: str
    location: float
    load_train: Optional[List[Dict]] = None
    loading_standard: Optional[str] = None  # 'IRC_Class_A', 'AASHTO_HS20'

class TemperatureLoadRequest(BaseModel):
    analysis_type: str  # 'uniform', 'gradient', 'fire', 'seasonal'
    delta_T: Optional[float] = None
    material: str = "concrete"
    length: float
    area: Optional[float] = None
    restraint: str = "fixed"
    T_top: Optional[float] = None
    T_bottom: Optional[float] = None
    depth: Optional[float] = None
    I: Optional[float] = None
    fire_duration: Optional[float] = None
    section_type: Optional[str] = None
    dimensions: Optional[Dict] = None
    cover: float = 50
    T_summer: Optional[float] = None
    T_winter: Optional[float] = None
    expansion_joint_spacing: Optional[float] = None

class MeshRequest(BaseModel):
    mesh_type: str  # 'rectangle', 'circle'
    width: Optional[float] = None
    height: Optional[float] = None
    nx: Optional[int] = None
    ny: Optional[int] = None
    radius: Optional[float] = None
    n_radial: Optional[int] = None
    n_circumferential: Optional[int] = None
    element_type: str = "quad4"

class MeshRefinementRequest(BaseModel):
    mesh: Dict
    refinement_factor: int = 2

class MeshQualityRequest(BaseModel):
    mesh: Dict

# Shear Wall Design
@router.post("/shear-wall")
def design_shear_wall(request: ShearWallRequest):
    """Design RC shear wall"""
    try:
        designer = ShearWallDesign()
        result = designer.design_shear_wall(
            request.height,
            request.length,
            request.thickness,
            request.axial_load,
            request.shear_force,
            request.moment,
            request.boundary_element
        )
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/coupling-beam")
def design_coupling_beam(request: CouplingBeamRequest):
    """Design coupling beam"""
    try:
        designer = ShearWallDesign()
        result = designer.design_coupling_beam(
            request.span,
            request.depth,
            request.width,
            request.shear_force,
            request.moment
        )
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Retaining Wall Design
@router.post("/retaining-wall")
def design_retaining_wall(request: RetainingWallRequest):
    """Design retaining wall"""
    try:
        designer = RetainingWallDesign()
        
        if request.wall_type == "cantilever":
            result = designer.cantilever_retaining_wall(
                request.height,
                request.stem_thickness_top,
                request.stem_thickness_bottom,
                request.base_width,
                request.base_thickness,
                request.toe_length,
                request.surcharge
            )
        elif request.wall_type == "gravity":
            result = designer.gravity_retaining_wall(
                request.height,
                request.top_width,
                request.bottom_width,
                request.surcharge
            )
        else:
            raise ValueError(f"Unknown wall type: {request.wall_type}")
        
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Staircase Design
@router.post("/staircase")
def design_staircase(request: StaircaseRequest):
    """Design staircase"""
    try:
        designer = StaircaseDesign()
        
        if request.stair_type == "dog_legged":
            result = designer.dog_legged_stair(
                request.flight_length,
                request.flight_width,
                request.waist_thickness,
                request.riser,
                request.tread,
                request.loads
            )
        elif request.stair_type == "cantilever":
            result = designer.cantilever_stair(
                request.cantilever_length,
                request.width,
                request.waist_thickness,
                request.riser,
                request.tread,
                request.loads
            )
        elif request.stair_type == "spiral":
            result = designer.spiral_stair(
                request.inner_radius,
                request.outer_radius,
                request.waist_thickness,
                request.total_angle,
                request.loads
            )
        else:
            raise ValueError(f"Unknown stair type: {request.stair_type}")
        
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Composite Design
@router.post("/composite-beam")
def design_composite_beam(request: CompositeBeamRequest):
    """Design composite beam"""
    try:
        designer = CompositeBeamDesign()
        result = designer.design_composite_beam(
            request.span,
            request.steel_section,
            request.slab_thickness,
            request.slab_width,
            request.loads,
            request.shear_connectors
        )
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/composite-column")
def design_composite_column(request: CompositeColumnRequest):
    """Design composite column"""
    try:
        designer = CompositeBeamDesign()
        result = designer.design_composite_column(
            request.height,
            request.steel_section,
            request.concrete_dimensions,
            request.axial_load,
            request.moment
        )
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Moving Load Analysis
@router.post("/moving-load")
def analyze_moving_load(request: MovingLoadRequest):
    """Analyze moving loads"""
    try:
        analyzer = MovingLoadAnalysis()
        
        if request.loading_standard == "IRC_Class_A":
            result = analyzer.irc_class_a_loading(
                request.span,
                request.response_type,
                request.location
            )
        elif request.loading_standard == "AASHTO_HS20":
            result = analyzer.aashto_hs20_loading(
                request.span,
                request.response_type,
                request.location
            )
        elif request.load_train:
            result = analyzer.analyze_moving_load_train(
                request.span,
                request.response_type,
                request.location,
                request.load_train
            )
        else:
            # Generate influence line only
            result = analyzer.generate_influence_line(
                request.span,
                100,
                request.response_type,
                request.location
            )
        
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Temperature Analysis
@router.post("/temperature-analysis")
def analyze_temperature(request: TemperatureLoadRequest):
    """Analyze temperature effects"""
    try:
        analyzer = TemperatureAnalysis()
        
        if request.analysis_type == "uniform":
            result = analyzer.uniform_temperature_load(
                request.delta_T,
                request.material,
                request.length,
                request.area,
                request.restraint
            )
        elif request.analysis_type == "gradient":
            result = analyzer.gradient_temperature_load(
                request.T_top,
                request.T_bottom,
                request.depth,
                request.material,
                request.length,
                request.I
            )
        elif request.analysis_type == "fire":
            result = analyzer.fire_exposure_analysis(
                request.fire_duration,
                request.section_type,
                request.dimensions,
                request.cover
            )
        elif request.analysis_type == "seasonal":
            result = analyzer.seasonal_temperature_effects(
                request.T_summer,
                request.T_winter,
                request.length,
                request.material,
                request.expansion_joint_spacing
            )
        else:
            raise ValueError(f"Unknown analysis type: {request.analysis_type}")
        
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Meshing
@router.post("/mesh/generate")
def generate_mesh(request: MeshRequest):
    """Generate mesh"""
    try:
        mesher = AutoMesher()
        
        if request.mesh_type == "rectangle":
            result = mesher.mesh_rectangle(
                request.width,
                request.height,
                request.nx,
                request.ny,
                request.element_type
            )
        elif request.mesh_type == "circle":
            result = mesher.mesh_circle(
                request.radius,
                request.n_radial,
                request.n_circumferential,
                request.element_type
            )
        else:
            raise ValueError(f"Unknown mesh type: {request.mesh_type}")
        
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/mesh/refine")
def refine_mesh(request: MeshRefinementRequest):
    """Refine existing mesh"""
    try:
        mesher = AutoMesher()
        result = mesher.refine_mesh(request.mesh, request.refinement_factor)
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/mesh/quality-check")
def check_mesh_quality(request: MeshQualityRequest):
    """Check mesh quality"""
    try:
        mesher = AutoMesher()
        result = mesher.check_mesh_quality(request.mesh)
        return {"status": "success", "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
