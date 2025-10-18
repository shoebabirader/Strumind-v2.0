"""
Timezone-aware datetime utilities
SECURITY FIX: All datetime operations should be timezone-aware
"""
from datetime import datetime, timezone, timedelta
from typing import Optional


def utc_now() -> datetime:
    """
    Get current UTC time (timezone-aware)
    SECURITY FIX: Replaces datetime.utcnow() which is naive
    
    Returns:
        Timezone-aware datetime in UTC
    """
    return datetime.now(timezone.utc)


def local_now() -> datetime:
    """
    Get current local time (timezone-aware)
    
    Returns:
        Timezone-aware datetime in local timezone
    """
    return datetime.now()


def to_utc(dt: datetime) -> datetime:
    """
    Convert datetime to UTC
    
    Args:
        dt: Datetime to convert (naive or aware)
        
    Returns:
        Timezone-aware datetime in UTC
    """
    if dt.tzinfo is None:
        # Assume naive datetime is UTC
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def from_timestamp(timestamp: float) -> datetime:
    """
    Create timezone-aware datetime from Unix timestamp
    
    Args:
        timestamp: Unix timestamp
        
    Returns:
        Timezone-aware datetime in UTC
    """
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)


def to_iso_string(dt: datetime) -> str:
    """
    Convert datetime to ISO 8601 string with timezone
    
    Args:
        dt: Datetime to convert
        
    Returns:
        ISO 8601 formatted string with timezone
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()


def parse_iso_string(iso_string: str) -> datetime:
    """
    Parse ISO 8601 string to timezone-aware datetime
    
    Args:
        iso_string: ISO 8601 formatted string
        
    Returns:
        Timezone-aware datetime
    """
    dt = datetime.fromisoformat(iso_string)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def add_time(dt: datetime, **kwargs) -> datetime:
    """
    Add time to datetime while preserving timezone
    
    Args:
        dt: Base datetime
        **kwargs: Arguments for timedelta (days, hours, minutes, etc.)
        
    Returns:
        New datetime with time added
    """
    return dt + timedelta(**kwargs)


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S %Z") -> str:
    """
    Format datetime to string
    
    Args:
        dt: Datetime to format
        format_str: Format string
        
    Returns:
        Formatted string
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.strftime(format_str)


# Convenience constants
UTC = timezone.utc
