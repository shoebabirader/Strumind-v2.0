"""
Custom error classes for structural analysis
Provides specific error types for better error handling and debugging
"""


class StructuralAnalysisError(Exception):
    """Base class for all structural analysis errors"""
    pass


# Analysis Errors
class AnalysisError(StructuralAnalysisError):
    """Base class for analysis-related errors"""
    pass


class SingularMatrixError(AnalysisError):
    """Stiffness matrix is singular - structure is unstable or improperly constrained"""
    def __init__(self, message="Stiffness matrix is singular"):
        self.message = message
        self.suggestions = [
            "Check for insufficient restraints",
            "Verify all elements are properly connected",
            "Check for zero stiffness elements",
            "Ensure no duplicate nodes exist",
            "Verify material properties are non-zero"
        ]
        super().__init__(self.format_message())
    
    def format_message(self):
        return f"{self.message}\n\nPossible causes:\n" + "\n".join(f"  - {s}" for s in self.suggestions)


class ConvergenceError(AnalysisError):
    """Iterative solver failed to converge"""
    def __init__(self, iterations: int, tolerance: float, message="Solver did not converge"):
        self.iterations = iterations
        self.tolerance = tolerance
        self.message = f"{message} after {iterations} iterations (tolerance: {tolerance})"
        super().__init__(self.message)


class NumericalInstabilityError(AnalysisError):
    """Numerical instability detected during analysis"""
    pass


class InvalidLoadCaseError(AnalysisError):
    """Load case is invalid or undefined"""
    pass


class InsufficientRestraintsError(AnalysisError):
    """Structure has insufficient restraints"""
    def __init__(self, n_restraints: int, min_required: int):
        message = f"Insufficient restraints: {n_restraints} provided, minimum {min_required} required"
        super().__init__(message)


# Geometry Errors
class GeometryError(StructuralAnalysisError):
    """Base class for geometry-related errors"""
    pass


class InvalidNodeError(GeometryError):
    """Node coordinates or properties are invalid"""
    pass


class DuplicateNodeError(GeometryError):
    """Duplicate node detected"""
    def __init__(self, node_id: str, existing_id: str, distance: float):
        message = f"Node {node_id} is duplicate of {existing_id} (distance: {distance:.6f}mm)"
        super().__init__(message)


class InvalidElementError(GeometryError):
    """Element definition is invalid"""
    pass


class ZeroLengthElementError(GeometryError):
    """Element has zero or near-zero length"""
    def __init__(self, element_id: str, length: float):
        message = f"Element {element_id} has zero/near-zero length: {length:.6f}mm"
        super().__init__(message)


class DisconnectedElementError(GeometryError):
    """Element references non-existent nodes"""
    def __init__(self, element_id: str, missing_nodes: list):
        message = f"Element {element_id} references non-existent nodes: {missing_nodes}"
        super().__init__(message)


class MechanismDetectedError(GeometryError):
    """Structure contains a mechanism (unstable configuration)"""
    pass


# Material Errors
class MaterialError(StructuralAnalysisError):
    """Base class for material-related errors"""
    pass


class InvalidMaterialPropertyError(MaterialError):
    """Material property is invalid"""
    pass


class MaterialNotFoundError(MaterialError):
    """Referenced material does not exist"""
    def __init__(self, material_id: str):
        message = f"Material '{material_id}' not found"
        super().__init__(message)


# Section Errors
class SectionError(StructuralAnalysisError):
    """Base class for section-related errors"""
    pass


class InvalidSectionPropertyError(SectionError):
    """Section property is invalid"""
    pass


class SectionNotFoundError(SectionError):
    """Referenced section does not exist"""
    def __init__(self, section_id: str):
        message = f"Section '{section_id}' not found"
        super().__init__(message)


# Load Errors
class LoadError(StructuralAnalysisError):
    """Base class for load-related errors"""
    pass


class InvalidLoadError(LoadError):
    """Load definition is invalid"""
    pass


class LoadCombinationError(LoadError):
    """Error in load combination"""
    pass


# Design Errors
class DesignError(StructuralAnalysisError):
    """Base class for design-related errors"""
    pass


class DesignCodeError(DesignError):
    """Error related to design code implementation"""
    pass


class CapacityExceededError(DesignError):
    """Member capacity exceeded"""
    def __init__(self, member_id: str, utilization_ratio: float):
        message = f"Member {member_id} capacity exceeded (UR: {utilization_ratio:.2f})"
        super().__init__(message)


class UnsupportedDesignCodeError(DesignError):
    """Design code not supported"""
    def __init__(self, code: str):
        message = f"Design code '{code}' is not supported"
        super().__init__(message)


# Database Errors
class DatabaseError(StructuralAnalysisError):
    """Base class for database-related errors"""
    pass


class ProjectNotFoundError(DatabaseError):
    """Project does not exist"""
    def __init__(self, project_id: int):
        message = f"Project {project_id} not found"
        super().__init__(message)


class DuplicateRecordError(DatabaseError):
    """Record already exists"""
    pass


class ConcurrentModificationError(DatabaseError):
    """Concurrent modification detected"""
    pass


# Validation Errors
class ValidationError(StructuralAnalysisError):
    """Base class for validation errors"""
    pass


class CoordinateValidationError(ValidationError):
    """Node coordinates are invalid"""
    pass


class PropertyValidationError(ValidationError):
    """Property value is invalid"""
    pass


# File Errors
class FileError(StructuralAnalysisError):
    """Base class for file-related errors"""
    pass


class FileFormatError(FileError):
    """File format is invalid or unsupported"""
    pass


class FileSizeError(FileError):
    """File size exceeds limit"""
    def __init__(self, size: int, max_size: int):
        message = f"File size ({size} bytes) exceeds maximum ({max_size} bytes)"
        super().__init__(message)


class IFCImportError(FileError):
    """Error importing IFC file"""
    pass


# Unit Errors
class UnitError(StructuralAnalysisError):
    """Base class for unit-related errors"""
    pass


class UnitConversionError(UnitError):
    """Error converting between units"""
    def __init__(self, from_unit: str, to_unit: str):
        message = f"Cannot convert from '{from_unit}' to '{to_unit}'"
        super().__init__(message)


class InconsistentUnitsError(UnitError):
    """Inconsistent units detected"""
    pass


# Helper function to convert errors to HTTP responses
def error_to_http_response(error: Exception) -> dict:
    """
    Convert custom error to HTTP response format
    
    Returns:
        dict with status_code and detail
    """
    error_map = {
        # 400 Bad Request
        ValidationError: 400,
        InvalidNodeError: 400,
        InvalidElementError: 400,
        InvalidMaterialPropertyError: 400,
        InvalidSectionPropertyError: 400,
        InvalidLoadError: 400,
        PropertyValidationError: 400,
        CoordinateValidationError: 400,
        UnsupportedDesignCodeError: 400,
        
        # 404 Not Found
        ProjectNotFoundError: 404,
        MaterialNotFoundError: 404,
        SectionNotFoundError: 404,
        
        # 409 Conflict
        DuplicateNodeError: 409,
        DuplicateRecordError: 409,
        ConcurrentModificationError: 409,
        
        # 422 Unprocessable Entity
        ZeroLengthElementError: 422,
        DisconnectedElementError: 422,
        InsufficientRestraintsError: 422,
        MechanismDetectedError: 422,
        
        # 500 Internal Server Error
        SingularMatrixError: 500,
        ConvergenceError: 500,
        NumericalInstabilityError: 500,
        AnalysisError: 500,
        
        # 503 Service Unavailable
        DatabaseError: 503,
    }
    
    status_code = 500  # Default
    for error_class, code in error_map.items():
        if isinstance(error, error_class):
            status_code = code
            break
    
    return {
        "status_code": status_code,
        "detail": str(error),
        "error_type": type(error).__name__
    }
