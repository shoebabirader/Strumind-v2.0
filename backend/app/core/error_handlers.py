"""
Comprehensive error handling decorators and utilities
"""
import functools
import logging
from typing import Callable, Any
from fastapi import HTTPException
import traceback
import numpy as np

logger = logging.getLogger(__name__)


def handle_analysis_errors(func: Callable) -> Callable:
    """
    Decorator for handling analysis function errors
    Provides consistent error handling and logging
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            logger.error(f"Validation error in {func.__name__}: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except np.linalg.LinAlgError as e:
            logger.error(f"Linear algebra error in {func.__name__}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Analysis failed due to numerical instability. Check model for singularities."
            )
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}\n{traceback.format_exc()}")
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)[:100]}"
            )
    return wrapper


def handle_design_errors(func: Callable) -> Callable:
    """
    Decorator for handling design function errors
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            logger.error(f"Design validation error in {func.__name__}: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except ZeroDivisionError as e:
            logger.error(f"Division by zero in {func.__name__}: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail="Invalid input parameters causing division by zero"
            )
        except Exception as e:
            logger.error(f"Design error in {func.__name__}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Design failed: {str(e)[:100]}")
    return wrapper


def validate_numeric_input(value: Any, name: str, min_val: float = None, 
                          max_val: float = None, allow_zero: bool = True) -> float:
    """
    Validate numeric input with comprehensive checks
    
    Args:
        value: Input value
        name: Parameter name for error messages
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        allow_zero: Whether zero is allowed
        
    Returns:
        Validated float value
        
    Raises:
        ValueError: If validation fails
    """
    try:
        num = float(value)
    except (ValueError, TypeError):
        raise ValueError(f"{name} must be a valid number, got: {value}")
    
    if not np.isfinite(num):
        raise ValueError(f"{name} must be finite (not NaN or Inf)")
    
    if not allow_zero and num == 0:
        raise ValueError(f"{name} cannot be zero")
    
    if min_val is not None and num < min_val:
        raise ValueError(f"{name} must be >= {min_val}, got: {num}")
    
    if max_val is not None and num > max_val:
        raise ValueError(f"{name} must be <= {max_val}, got: {num}")
    
    return num


def validate_array_input(arr: Any, name: str, expected_shape: tuple = None,
                        allow_empty: bool = False) -> np.ndarray:
    """
    Validate array input
    
    Args:
        arr: Input array
        name: Parameter name
        expected_shape: Expected shape tuple
        allow_empty: Whether empty arrays are allowed
        
    Returns:
        Validated numpy array
    """
    try:
        arr = np.asarray(arr)
    except Exception as e:
        raise ValueError(f"{name} must be array-like: {str(e)}")
    
    if not allow_empty and arr.size == 0:
        raise ValueError(f"{name} cannot be empty")
    
    if expected_shape is not None and arr.shape != expected_shape:
        raise ValueError(f"{name} shape mismatch. Expected {expected_shape}, got {arr.shape}")
    
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} contains NaN or Inf values")
    
    return arr


class AnalysisError(Exception):
    """Base exception for analysis errors"""
    pass


class ValidationError(AnalysisError):
    """Input validation error"""
    pass


class ConvergenceError(AnalysisError):
    """Analysis convergence error"""
    pass


class SingularMatrixError(AnalysisError):
    """Singular matrix error"""
    pass



def handle_api_errors(func: Callable) -> Callable:
    """
    Comprehensive decorator for API endpoint error handling
    Handles validation, analysis, and unexpected errors
    """
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValueError as e:
            logger.warning(f"Validation error in {func.__name__}: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except ValidationError as e:
            logger.warning(f"Pydantic validation error in {func.__name__}: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))
        except np.linalg.LinAlgError as e:
            logger.error(f"Linear algebra error in {func.__name__}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Numerical instability detected. Check model for errors."
            )
        except ZeroDivisionError:
            logger.error(f"Division by zero in {func.__name__}")
            raise HTTPException(
                status_code=400,
                detail="Invalid parameters causing division by zero"
            )
        except OverflowError:
            logger.error(f"Numerical overflow in {func.__name__}")
            raise HTTPException(
                status_code=400,
                detail="Values too large, causing numerical overflow"
            )
        except MemoryError:
            logger.error(f"Memory error in {func.__name__}")
            raise HTTPException(
                status_code=507,
                detail="Insufficient memory for operation"
            )
        except TimeoutError:
            logger.error(f"Timeout in {func.__name__}")
            raise HTTPException(
                status_code=504,
                detail="Operation timed out"
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in {func.__name__}: {str(e)}\n"
                f"{traceback.format_exc()}"
            )
            # SECURITY: Don't expose internal details in production
            raise HTTPException(
                status_code=500,
                detail="Internal server error. Please contact support."
            )
    
    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            logger.warning(f"Validation error in {func.__name__}: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except ValidationError as e:
            logger.warning(f"Pydantic validation error in {func.__name__}: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))
        except np.linalg.LinAlgError as e:
            logger.error(f"Linear algebra error in {func.__name__}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Numerical instability detected. Check model for errors."
            )
        except ZeroDivisionError:
            logger.error(f"Division by zero in {func.__name__}")
            raise HTTPException(
                status_code=400,
                detail="Invalid parameters causing division by zero"
            )
        except OverflowError:
            logger.error(f"Numerical overflow in {func.__name__}")
            raise HTTPException(
                status_code=400,
                detail="Values too large, causing numerical overflow"
            )
        except MemoryError:
            logger.error(f"Memory error in {func.__name__}")
            raise HTTPException(
                status_code=507,
                detail="Insufficient memory for operation"
            )
        except TimeoutError:
            logger.error(f"Timeout in {func.__name__}")
            raise HTTPException(
                status_code=504,
                detail="Operation timed out"
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in {func.__name__}: {str(e)}\n"
                f"{traceback.format_exc()}"
            )
            # SECURITY: Don't expose internal details in production
            raise HTTPException(
                status_code=500,
                detail="Internal server error. Please contact support."
            )
    
    # Return appropriate wrapper based on function type
    import inspect
    if inspect.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper
