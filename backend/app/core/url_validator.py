"""
URL Validation Utilities
Prevents SSRF (Server-Side Request Forgery) attacks
"""
import re
import ipaddress
from urllib.parse import urlparse
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class URLValidator:
    """
    Validates URLs to prevent SSRF attacks
    """
    
    # Blocked IP ranges (private networks, localhost, etc.)
    BLOCKED_IP_RANGES = [
        ipaddress.ip_network('127.0.0.0/8'),      # Loopback
        ipaddress.ip_network('10.0.0.0/8'),       # Private
        ipaddress.ip_network('172.16.0.0/12'),    # Private
        ipaddress.ip_network('192.168.0.0/16'),   # Private
        ipaddress.ip_network('169.254.0.0/16'),   # Link-local
        ipaddress.ip_network('::1/128'),          # IPv6 loopback
        ipaddress.ip_network('fc00::/7'),         # IPv6 private
        ipaddress.ip_network('fe80::/10'),        # IPv6 link-local
    ]
    
    # Allowed protocols
    ALLOWED_PROTOCOLS = ['http', 'https']
    
    # Blocked hostnames
    BLOCKED_HOSTNAMES = [
        'localhost',
        'metadata.google.internal',  # GCP metadata
        '169.254.169.254',            # AWS/Azure metadata
    ]
    
    @classmethod
    def is_safe_url(cls, url: str, allow_private: bool = False) -> bool:
        """
        Check if URL is safe to fetch
        
        Args:
            url: URL to validate
            allow_private: Allow private IP ranges (for development)
        
        Returns:
            True if URL is safe, False otherwise
        """
        try:
            parsed = urlparse(url)
            
            # Check protocol
            if parsed.scheme not in cls.ALLOWED_PROTOCOLS:
                logger.warning(f"Blocked URL with invalid protocol: {parsed.scheme}")
                return False
            
            # Check hostname
            hostname = parsed.hostname
            if not hostname:
                logger.warning("URL has no hostname")
                return False
            
            # Check blocked hostnames
            if hostname.lower() in cls.BLOCKED_HOSTNAMES:
                logger.warning(f"Blocked hostname: {hostname}")
                return False
            
            # Check if hostname is an IP address
            try:
                ip = ipaddress.ip_address(hostname)
                
                # Block private IPs unless explicitly allowed
                if not allow_private:
                    for blocked_range in cls.BLOCKED_IP_RANGES:
                        if ip in blocked_range:
                            logger.warning(f"Blocked private IP: {ip}")
                            return False
                
            except ValueError:
                # Not an IP address, it's a domain name
                # Check for localhost variations
                if 'localhost' in hostname.lower():
                    logger.warning(f"Blocked localhost variation: {hostname}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating URL: {e}")
            return False
    
    @classmethod
    def sanitize_url(cls, url: str) -> Optional[str]:
        """
        Sanitize and validate URL
        
        Returns:
            Sanitized URL if valid, None otherwise
        """
        if not isinstance(url, str):
            return None
        
        url = url.strip()
        
        if not url:
            return None
        
        # Check if URL is safe
        if not cls.is_safe_url(url):
            return None
        
        return url
    
    @classmethod
    def validate_webhook_url(cls, url: str) -> bool:
        """
        Validate webhook URL (stricter than general URL validation)
        
        Args:
            url: Webhook URL to validate
        
        Returns:
            True if valid webhook URL
        """
        if not cls.is_safe_url(url, allow_private=False):
            return False
        
        parsed = urlparse(url)
        
        # Webhook must use HTTPS in production
        if parsed.scheme != 'https':
            logger.warning("Webhook must use HTTPS")
            return False
        
        # Must have a path
        if not parsed.path or parsed.path == '/':
            logger.warning("Webhook URL must have a path")
            return False
        
        return True


def validate_external_url(url: str, allow_private: bool = False) -> Optional[str]:
    """
    Convenience function to validate external URLs
    
    Args:
        url: URL to validate
        allow_private: Allow private IP ranges
    
    Returns:
        Validated URL or None
    """
    return URLValidator.sanitize_url(url) if URLValidator.is_safe_url(url, allow_private) else None
