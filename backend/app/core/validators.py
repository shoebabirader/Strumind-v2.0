"""
Security validators for input sanitization and validation
Prevents injection attacks, validates data types, and ensures safe operations
"""
import re
from typing import Any, Union
from pathlib import Path


class SecurityValidator:
    """Comprehensive security validation utilities"""
    
    @staticmethod
    def sanitize_string(value: str, max_length: int = 1000) -> str:
        """
        Sanitize string input to prevent injection attacks
        
        Args:
            value: Input string
            max_length: Maximum allowed length
            
        Returns:
            Sanitized string
        """
        if not isinstance(value, str):
            raise ValueError("Input must be a string")
        
        # Truncate to max length
        value = value[:max_length]
        
        # Remove control characters except newline and tab
        value = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', value)
        
        return value.strip()
    
    @staticmethod
    def validate_numeric(value: Any, min_val: float = None, max_val: float = None,
                        allow_negative: bool = True, allow_zero: bool = True) -> float:
        """
        Validate and sanitize numeric input
        
        Args:
            value: Input value
            min_val: Minimum allowed value
            max_val: Maximum allowed value
            allow_negative: Whether negative values are allowed
            allow_zero: Whether zero is allowed
            
        Returns:
            Validated float value
        """
        try:
            num = float(value)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid numeric value: {value}")
        
        if not allow_negative and num < 0:
            raise ValueError(f"Negative values not allowed: {num}")
        
        if not allow_zero and num == 0:
            raise ValueError("Zero value not allowed")
        
        if min_val is not None and num < min_val:
            raise ValueError(f"Value {num} below minimum {min_val}")
        
        if max_val is not None and num > max_val:
            raise ValueError(f"Value {num} exceeds maximum {max_val}")
        
        if not (-1e308 < num < 1e308):  # Check for infinity
            raise ValueError("Value out of valid range")
        
        return num
    
    @staticmethod
    def validate_path(path: str, base_dir: str = None, must_exist: bool = False) -> Path:
        """
        Validate file path to prevent path traversal attacks
        
        Args:
            path: File path to validate
            base_dir: Base directory to restrict access to
            must_exist: Whether path must exist
            
        Returns:
            Validated Path object
        """
        if not isinstance(path, str):
            raise ValueError("Path must be a string")
        
        # Remove null bytes
        path = path.replace('\x00', '')
        
        # Convert to Path and resolve
        path_obj = Path(path).resolve()
        
        # Check for path traversal
        if base_dir:
            base_path = Path(base_dir).resolve()
            try:
                path_obj.relative_to(base_path)
            except ValueError:
                raise ValueError(f"Path traversal attempt detected: {path}")
        
        # Check existence if required
        if must_exist and not path_obj.exists():
            raise ValueError(f"Path does not exist: {path}")
        
        return path_obj
    
    @staticmethod
    def validate_identifier(value: str, max_length: int = 100) -> str:
        """
        Validate identifier (variable name, table name, etc.)
        Only allows alphanumeric and underscore
        
        Args:
            value: Identifier to validate
            max_length: Maximum length
            
        Returns:
            Validated identifier
        """
        if not isinstance(value, str):
            raise ValueError("Identifier must be a string")
        
        if not value:
            raise ValueError("Identifier cannot be empty")
        
        if len(value) > max_length:
            raise ValueError(f"Identifier too long (max {max_length})")
        
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', value):
            raise ValueError(f"Invalid identifier format: {value}")
        
        return value
    
    @staticmethod
    def validate_email(email: str) -> str:
        """
        Validate email address format
        
        Args:
            email: Email address
            
        Returns:
            Validated email
        """
        if not isinstance(email, str):
            raise ValueError("Email must be a string")
        
        email = email.strip().lower()
        
        # Basic email validation
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValueError(f"Invalid email format: {email}")
        
        if len(email) > 254:  # RFC 5321
            raise ValueError("Email too long")
        
        return email
    
    @staticmethod
    def sanitize_sql_like(value: str) -> str:
        """
        Sanitize value for SQL LIKE queries
        Escapes special characters
        
        Args:
            value: Input value
            
        Returns:
            Sanitized value
        """
        if not isinstance(value, str):
            raise ValueError("Value must be a string")
        
        # Escape SQL LIKE wildcards
        value = value.replace('\\', '\\\\')
        value = value.replace('%', '\\%')
        value = value.replace('_', '\\_')
        
        return value
    
    @staticmethod
    def validate_url(url: str, allowed_schemes: list = None) -> str:
        """
        Validate URL to prevent SSRF attacks
        
        Args:
            url: URL to validate
            allowed_schemes: List of allowed schemes (default: ['http', 'https'])
            
        Returns:
            Validated URL
        """
        if not isinstance(url, str):
            raise ValueError("URL must be a string")
        
        if allowed_schemes is None:
            allowed_schemes = ['http', 'https']
        
        url = url.strip()
        
        # Basic URL validation
        pattern = r'^(https?):\/\/([\w\-\.]+)(:\d+)?(\/.*)?$'
        match = re.match(pattern, url, re.IGNORECASE)
        
        if not match:
            raise ValueError(f"Invalid URL format: {url}")
        
        scheme = match.group(1).lower()
        if scheme not in allowed_schemes:
            raise ValueError(f"URL scheme not allowed: {scheme}")
        
        # Prevent localhost/internal network access
        host = match.group(2).lower()
        blocked_hosts = ['localhost', '127.0.0.1', '0.0.0.0', '::1']
        if host in blocked_hosts or host.startswith('192.168.') or host.startswith('10.'):
            raise ValueError(f"Access to internal network not allowed: {host}")
        
        return url



class EngineeringValidator:
    """
    Engineering-specific input validation
    Validates structural engineering parameters
    """
    
    @staticmethod
    def validate_material_property(value: float, property_name: str) -> float:
        """
        Validate material properties with engineering constraints
        
        Args:
            value: Property value
            property_name: Name of property (E, fy, fck, etc.)
            
        Returns:
            Validated value
        """
        # Common ranges for material properties
        ranges = {
            'E': (1000, 500000),  # Elastic modulus (MPa): 1 GPa to 500 GPa
            'G': (500, 200000),   # Shear modulus (MPa)
            'fy': (200, 1000),    # Yield strength (MPa)
            'fu': (300, 1500),    # Ultimate strength (MPa)
            'fck': (10, 150),     # Concrete strength (MPa)
            'density': (1000, 10000),  # kg/m³
            'poisson': (0.0, 0.5),     # Poisson's ratio
        }
        
        value = SecurityValidator.validate_numeric(
            value,
            allow_negative=False,
            allow_zero=False
        )
        
        if property_name in ranges:
            min_val, max_val = ranges[property_name]
            if not (min_val <= value <= max_val):
                raise ValueError(
                    f"{property_name} value {value} outside valid range "
                    f"[{min_val}, {max_val}]"
                )
        
        return value
    
    @staticmethod
    def validate_section_property(value: float, property_name: str) -> float:
        """
        Validate section properties
        
        Args:
            value: Property value
            property_name: Name of property (A, I, J, etc.)
            
        Returns:
            Validated value
        """
        # Section properties must be positive
        value = SecurityValidator.validate_numeric(
            value,
            min_val=1e-6,  # Minimum to avoid numerical issues
            allow_negative=False,
            allow_zero=False
        )
        
        # Maximum reasonable values (to catch input errors)
        max_values = {
            'A': 1e9,      # Area (mm²): ~1 m²
            'Ix': 1e15,    # Moment of inertia (mm⁴)
            'Iy': 1e15,
            'Iz': 1e15,
            'J': 1e15,     # Torsion constant (mm⁴)
            'Zx': 1e12,    # Section modulus (mm³)
            'Zy': 1e12,
            'Zz': 1e12,
        }
        
        if property_name in max_values:
            if value > max_values[property_name]:
                raise ValueError(
                    f"{property_name} value {value} exceeds maximum "
                    f"{max_values[property_name]}"
                )
        
        return value
    
    @staticmethod
    def validate_load(value: float, load_type: str = 'force') -> float:
        """
        Validate load values
        
        Args:
            value: Load value
            load_type: Type of load (force, moment, pressure, etc.)
            
        Returns:
            Validated value
        """
        # Loads can be negative (direction)
        value = SecurityValidator.validate_numeric(
            value,
            allow_negative=True,
            allow_zero=True
        )
        
        # Sanity check for unreasonably large loads
        max_values = {
            'force': 1e9,      # 1 GN
            'moment': 1e12,    # 1 GN·m
            'pressure': 1e6,   # 1000 MPa
            'distributed': 1e6, # 1000 kN/m
        }
        
        max_val = max_values.get(load_type, 1e12)
        if abs(value) > max_val:
            raise ValueError(
                f"{load_type} value {value} exceeds reasonable limit {max_val}"
            )
        
        return value
    
    @staticmethod
    def validate_dimension(value: float, dimension_type: str = 'length') -> float:
        """
        Validate geometric dimensions
        
        Args:
            value: Dimension value
            dimension_type: Type (length, width, height, thickness, etc.)
            
        Returns:
            Validated value
        """
        # Dimensions must be positive
        value = SecurityValidator.validate_numeric(
            value,
            min_val=0.1,  # Minimum 0.1 mm
            allow_negative=False,
            allow_zero=False
        )
        
        # Maximum reasonable dimensions
        max_values = {
            'length': 1000000,    # 1000 m
            'width': 100000,      # 100 m
            'height': 100000,     # 100 m
            'thickness': 10000,   # 10 m
            'diameter': 10000,    # 10 m
            'spacing': 50000,     # 50 m
        }
        
        max_val = max_values.get(dimension_type, 1000000)
        if value > max_val:
            raise ValueError(
                f"{dimension_type} value {value} exceeds maximum {max_val}"
            )
        
        return value
    
    @staticmethod
    def validate_array_dimensions(array: list, expected_shape: tuple = None,
                                  min_size: int = None, max_size: int = None) -> list:
        """
        Validate array dimensions and size
        
        Args:
            array: Input array
            expected_shape: Expected shape (rows, cols) for 2D arrays
            min_size: Minimum array size
            max_size: Maximum array size
            
        Returns:
            Validated array
        """
        if not isinstance(array, (list, tuple)):
            raise ValueError("Input must be a list or tuple")
        
        size = len(array)
        
        if min_size is not None and size < min_size:
            raise ValueError(f"Array size {size} below minimum {min_size}")
        
        if max_size is not None and size > max_size:
            raise ValueError(f"Array size {size} exceeds maximum {max_size}")
        
        # Check for 2D arrays
        if expected_shape and len(expected_shape) == 2:
            rows, cols = expected_shape
            if size != rows:
                raise ValueError(
                    f"Array has {size} rows, expected {rows}"
                )
            for i, row in enumerate(array):
                if not isinstance(row, (list, tuple)):
                    raise ValueError(f"Row {i} is not a list/tuple")
                if len(row) != cols:
                    raise ValueError(
                        f"Row {i} has {len(row)} columns, expected {cols}"
                    )
        
        return array
    
    @staticmethod
    def validate_dof(dof: int, max_dof: int = 6) -> int:
        """
        Validate degree of freedom index
        
        Args:
            dof: DOF index
            max_dof: Maximum DOF per node
            
        Returns:
            Validated DOF
        """
        if not isinstance(dof, int):
            raise ValueError("DOF must be an integer")
        
        if not (0 <= dof < max_dof):
            raise ValueError(f"DOF {dof} out of range [0, {max_dof})")
        
        return dof
    
    @staticmethod
    def validate_node_id(node_id: int, max_nodes: int = 1000000) -> int:
        """
        Validate node ID
        
        Args:
            node_id: Node identifier
            max_nodes: Maximum number of nodes
            
        Returns:
            Validated node ID
        """
        if not isinstance(node_id, int):
            raise ValueError("Node ID must be an integer")
        
        if node_id < 0:
            raise ValueError("Node ID must be non-negative")
        
        if node_id >= max_nodes:
            raise ValueError(f"Node ID {node_id} exceeds maximum {max_nodes}")
        
        return node_id
    
    @staticmethod
    def validate_element_id(element_id: int, max_elements: int = 1000000) -> int:
        """
        Validate element ID
        
        Args:
            element_id: Element identifier
            max_elements: Maximum number of elements
            
        Returns:
            Validated element ID
        """
        if not isinstance(element_id, int):
            raise ValueError("Element ID must be an integer")
        
        if element_id < 0:
            raise ValueError("Element ID must be non-negative")
        
        if element_id >= max_elements:
            raise ValueError(f"Element ID {element_id} exceeds maximum {max_elements}")
        
        return element_id
    
    @staticmethod
    def validate_design_code(code: str) -> str:
        """
        Validate design code identifier
        
        Args:
            code: Design code (IS456, IS800, ACI318, etc.)
            
        Returns:
            Validated code
        """
        code = SecurityValidator.sanitize_string(code, max_length=50)
        
        # List of supported codes
        supported_codes = [
            'IS456', 'IS800', 'IS1893', 'IS875',
            'ACI318', 'AISC360', 'ASCE7',
            'EC2', 'EC3', 'EC8',
            'BS8110', 'BS5950',
            'AS3600', 'AS4100',
        ]
        
        if code.upper() not in supported_codes:
            raise ValueError(f"Unsupported design code: {code}")
        
        return code.upper()
