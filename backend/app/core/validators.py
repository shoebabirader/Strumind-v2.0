"""
Comprehensive validation utilities for structural analysis
Implements input validation, geometry checks, and data sanitization
"""
import numpy as np
from typing import List, Dict, Tuple, Optional
from pydantic import BaseModel, field_validator, Field


class ValidationError(Exception):
    """Base class for validation errors"""
    pass


class NodeValidator:
    """Validator for node coordinates and properties"""
    
    COORDINATE_TOLERANCE = 1e-3  # mm
    MAX_COORDINATE = 1e6  # mm (1 km)
    
    @staticmethod
    def validate_coordinates(x: float, y: float, z: float) -> Tuple[bool, Optional[str]]:
        """
        Validate node coordinates
        
        Returns:
            (is_valid, error_message)
        """
        # Check for finite values
        if not np.isfinite([x, y, z]).all():
            return False, "Coordinates must be finite (not NaN or Inf)"
        
        # Check reasonable range
        if abs(x) > NodeValidator.MAX_COORDINATE:
            return False, f"X coordinate out of range (max ±{NodeValidator.MAX_COORDINATE}mm)"
        if abs(y) > NodeValidator.MAX_COORDINATE:
            return False, f"Y coordinate out of range (max ±{NodeValidator.MAX_COORDINATE}mm)"
        if abs(z) > NodeValidator.MAX_COORDINATE:
            return False, f"Z coordinate out of range (max ±{NodeValidator.MAX_COORDINATE}mm)"
        
        return True, None
    
    @staticmethod
    def check_duplicate(x: float, y: float, z: float, existing_nodes: List) -> Tuple[bool, Optional[str]]:
        """Check for duplicate nodes within tolerance"""
        for node in existing_nodes:
            dist = np.sqrt((x - node.x)**2 + (y - node.y)**2 + (z - node.z)**2)
            if dist < NodeValidator.COORDINATE_TOLERANCE:
                return True, f"Duplicate node detected near node {node.id} (distance: {dist:.6f}mm)"
        
        return False, None


class MaterialValidator:
    """Validator for material properties"""
    
    # Typical ranges for structural materials
    E_MIN = 1000  # MPa (timber)
    E_MAX = 500000  # MPa (high-strength steel)
    NU_MIN = -1.0
    NU_MAX = 0.5
    DENSITY_MIN = 100  # kg/m³
    DENSITY_MAX = 20000  # kg/m³
    
    @staticmethod
    def validate_elastic_modulus(E: float) -> Tuple[bool, Optional[str]]:
        """Validate Young's modulus"""
        if E <= 0:
            return False, "Young's modulus must be positive"
        
        if E < MaterialValidator.E_MIN:
            return False, f"Young's modulus too low (min {MaterialValidator.E_MIN} MPa)"
        
        if E > MaterialValidator.E_MAX:
            return False, f"Young's modulus too high (max {MaterialValidator.E_MAX} MPa)"
        
        return True, None
    
    @staticmethod
    def validate_poisson_ratio(nu: float) -> Tuple[bool, Optional[str]]:
        """Validate Poisson's ratio"""
        if nu < MaterialValidator.NU_MIN or nu > MaterialValidator.NU_MAX:
            return False, f"Poisson's ratio must be between {MaterialValidator.NU_MIN} and {MaterialValidator.NU_MAX}"
        
        return True, None

    
    @staticmethod
    def validate_yield_stress(fy: float, fu: Optional[float] = None) -> Tuple[bool, Optional[str]]:
        """Validate yield and ultimate stress"""
        if fy <= 0:
            return False, "Yield stress must be positive"
        
        if fu is not None:
            if fu <= 0:
                return False, "Ultimate stress must be positive"
            if fy > fu:
                return False, "Yield stress cannot exceed ultimate stress"
        
        return True, None
    
    @staticmethod
    def validate_density(rho: float) -> Tuple[bool, Optional[str]]:
        """Validate material density"""
        if rho <= 0:
            return False, "Density must be positive"
        
        if rho < MaterialValidator.DENSITY_MIN or rho > MaterialValidator.DENSITY_MAX:
            return False, f"Density out of typical range ({MaterialValidator.DENSITY_MIN}-{MaterialValidator.DENSITY_MAX} kg/m³)"
        
        return True, None


class SectionValidator:
    """Validator for section properties"""
    
    @staticmethod
    def validate_area(A: float) -> Tuple[bool, Optional[str]]:
        """Validate cross-sectional area"""
        if A <= 0:
            return False, "Cross-sectional area must be positive"
        
        if A < 1:  # mm²
            return False, "Cross-sectional area too small (min 1 mm²)"
        
        if A > 1e8:  # mm²
            return False, "Cross-sectional area too large (max 1e8 mm²)"
        
        return True, None
    
    @staticmethod
    def validate_moment_of_inertia(I: float, axis: str = "") -> Tuple[bool, Optional[str]]:
        """Validate moment of inertia"""
        if I <= 0:
            return False, f"Moment of inertia{' about ' + axis if axis else ''} must be positive"
        
        if I < 1:  # mm⁴
            return False, f"Moment of inertia{' about ' + axis if axis else ''} too small (min 1 mm⁴)"
        
        return True, None
    
    @staticmethod
    def validate_section_properties(A: float, Iy: float, Iz: float, J: float) -> Tuple[bool, Optional[str]]:
        """Validate complete section properties"""
        # Area
        is_valid, error = SectionValidator.validate_area(A)
        if not is_valid:
            return False, error
        
        # Moment of inertia about y-axis
        is_valid, error = SectionValidator.validate_moment_of_inertia(Iy, "y-axis")
        if not is_valid:
            return False, error
        
        # Moment of inertia about z-axis
        is_valid, error = SectionValidator.validate_moment_of_inertia(Iz, "z-axis")
        if not is_valid:
            return False, error
        
        # Torsion constant
        if J <= 0:
            return False, "Torsion constant must be positive"
        
        return True, None


class LoadValidator:
    """Validator for loads"""
    
    MAX_FORCE = 1e8  # N (100,000 kN)
    MAX_MOMENT = 1e10  # N·mm (10,000 kN·m)
    
    @staticmethod
    def validate_force(F: float, direction: str = "") -> Tuple[bool, Optional[str]]:
        """Validate force magnitude"""
        if not np.isfinite(F):
            return False, f"Force{' in ' + direction if direction else ''} must be finite"
        
        if abs(F) > LoadValidator.MAX_FORCE:
            return False, f"Force{' in ' + direction if direction else ''} magnitude too large (max {LoadValidator.MAX_FORCE} N)"
        
        return True, None
    
    @staticmethod
    def validate_moment(M: float, axis: str = "") -> Tuple[bool, Optional[str]]:
        """Validate moment magnitude"""
        if not np.isfinite(M):
            return False, f"Moment{' about ' + axis if axis else ''} must be finite"
        
        if abs(M) > LoadValidator.MAX_MOMENT:
            return False, f"Moment{' about ' + axis if axis else ''} magnitude too large (max {LoadValidator.MAX_MOMENT} N·mm)"
        
        return True, None


class GeometryValidator:
    """Validator for structural geometry"""
    
    MIN_ELEMENT_LENGTH = 1.0  # mm
    MAX_ASPECT_RATIO = 1000
    
    @staticmethod
    def validate_element_length(length: float) -> Tuple[bool, Optional[str]]:
        """Validate element length"""
        if length < GeometryValidator.MIN_ELEMENT_LENGTH:
            return False, f"Element length too small (min {GeometryValidator.MIN_ELEMENT_LENGTH} mm)"
        
        return True, None
    
    @staticmethod
    def validate_element_connectivity(element, nodes_dict: Dict) -> Tuple[bool, Optional[str]]:
        """Validate that element nodes exist"""
        for node_id in element.node_ids:
            if node_id not in nodes_dict:
                return False, f"Node {node_id} referenced by element does not exist"
        
        return True, None
    
    @staticmethod
    def check_stability(n_nodes: int, n_restraints: int, dimension: int = 3) -> Tuple[bool, Optional[str]]:
        """
        Check basic structural stability
        
        Args:
            n_nodes: Number of nodes
            n_restraints: Number of restrained DOF
            dimension: 2D or 3D (2 or 3)
        """
        min_restraints = 3 if dimension == 2 else 6
        
        if n_restraints < min_restraints:
            return False, f"Insufficient restraints (minimum {min_restraints} for {dimension}D structure)"
        
        dof_per_node = 3 if dimension == 2 else 6
        total_dof = n_nodes * dof_per_node
        
        if n_restraints >= total_dof:
            return False, "Structure is over-constrained (restraints ≥ total DOF)"
        
        return True, None
    
    @staticmethod
    def check_element_aspect_ratio(length: float, min_dimension: float) -> Tuple[bool, Optional[str]]:
        """Check element aspect ratio"""
        if min_dimension <= 0:
            return False, "Element dimension must be positive"
        
        aspect_ratio = length / min_dimension
        
        if aspect_ratio > GeometryValidator.MAX_ASPECT_RATIO:
            return False, f"Element aspect ratio too high ({aspect_ratio:.1f} > {GeometryValidator.MAX_ASPECT_RATIO})"
        
        return True, None


class AnalysisValidator:
    """Validator for analysis parameters"""
    
    @staticmethod
    def validate_convergence_tolerance(tol: float) -> Tuple[bool, Optional[str]]:
        """Validate convergence tolerance"""
        if tol <= 0:
            return False, "Convergence tolerance must be positive"
        
        if tol < 1e-12:
            return False, "Convergence tolerance too small (min 1e-12)"
        
        if tol > 1e-3:
            return False, "Convergence tolerance too large (max 1e-3)"
        
        return True, None
    
    @staticmethod
    def validate_max_iterations(max_iter: int) -> Tuple[bool, Optional[str]]:
        """Validate maximum iterations"""
        if max_iter < 1:
            return False, "Maximum iterations must be at least 1"
        
        if max_iter > 10000:
            return False, "Maximum iterations too large (max 10000)"
        
        return True, None
    
    @staticmethod
    def validate_time_step(dt: float, total_time: float) -> Tuple[bool, Optional[str]]:
        """Validate time step for dynamic analysis"""
        if dt <= 0:
            return False, "Time step must be positive"
        
        if total_time <= 0:
            return False, "Total time must be positive"
        
        if dt > total_time:
            return False, "Time step cannot exceed total time"
        
        n_steps = int(total_time / dt)
        if n_steps > 100000:
            return False, f"Too many time steps ({n_steps}). Increase time step or reduce total time."
        
        return True, None


# Pydantic models with validation
class ValidatedNodeCreate(BaseModel):
    """Node creation with validation"""
    project_id: int
    node_id: str
    x: float
    y: float
    z: float
    
    @field_validator('x', 'y', 'z')
    @classmethod
    def validate_coordinates(cls, v, info):
        if not np.isfinite(v):
            raise ValueError(f"{info.field_name} must be finite")
        if abs(v) > NodeValidator.MAX_COORDINATE:
            raise ValueError(f"{info.field_name} out of range")
        return v


class ValidatedMaterialCreate(BaseModel):
    """Material creation with validation"""
    project_id: int
    material_id: str
    name: str
    E: float = Field(gt=0, description="Young's modulus (MPa)")
    nu: float = Field(ge=-1, le=0.5, description="Poisson's ratio")
    density: float = Field(gt=0, description="Density (kg/m³)")
    fy: Optional[float] = Field(None, gt=0, description="Yield stress (MPa)")
    fu: Optional[float] = Field(None, gt=0, description="Ultimate stress (MPa)")
    
    @field_validator('E')
    @classmethod
    def validate_E(cls, v):
        is_valid, error = MaterialValidator.validate_elastic_modulus(v)
        if not is_valid:
            raise ValueError(error)
        return v
    
    @field_validator('fy', 'fu')
    @classmethod
    def validate_stresses(cls, v, info):
        # Note: In Pydantic V2, cross-field validation is done differently
        # This is a simplified version
        if v is not None:
            # Additional validation can be added in model_validator
            pass
        return v


class ValidatedSectionCreate(BaseModel):
    """Section creation with validation"""
    project_id: int
    section_id: str
    name: str
    section_type: str
    A: float = Field(gt=0, description="Area (mm²)")
    Iy: float = Field(gt=0, description="Moment of inertia about y (mm⁴)")
    Iz: float = Field(gt=0, description="Moment of inertia about z (mm⁴)")
    J: float = Field(gt=0, description="Torsion constant (mm⁴)")
    
    @field_validator('A')
    @classmethod
    def validate_area(cls, v):
        is_valid, error = SectionValidator.validate_area(v)
        if not is_valid:
            raise ValueError(error)
        return v
