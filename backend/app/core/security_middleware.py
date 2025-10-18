"""
Security middleware for FastAPI application
Implements various security headers and protections
"""
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import time
from typing import Callable
import logging
import re

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Add security headers to all responses
    Prevents XSS, clickjacking, and other attacks
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # SECURITY FIX: Enforce HTTPS in production
        if request.url.scheme == "http" and request.headers.get("host", "").startswith("localhost") is False:
            # Redirect to HTTPS
            https_url = str(request.url).replace("http://", "https://", 1)
            return JSONResponse(
                status_code=301,
                headers={"Location": https_url},
                content={"detail": "Redirecting to HTTPS"}
            )
        
        response = await call_next(request)
        
        # SECURITY FIX: Add comprehensive security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # Allow Swagger UI CDN for /docs endpoint
        if request.url.path in ["/docs", "/redoc"]:
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://unpkg.com; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://unpkg.com; "
                "img-src 'self' data: https:; "
                "font-src 'self' data: https://cdn.jsdelivr.net https://unpkg.com; "
                "connect-src 'self' ws: wss:"
            )
        else:
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self' data:; "
                "connect-src 'self' ws: wss:"
            )
        
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        return response


class RequestValidationMiddleware(BaseHTTPMiddleware):
    """
    Validate and sanitize incoming requests
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # SECURITY FIX: Validate request size
        MAX_REQUEST_SIZE = 50 * 1024 * 1024  # 50MB
        
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > MAX_REQUEST_SIZE:
            return JSONResponse(
                status_code=413,
                content={"detail": "Request too large"}
            )
        
        # SECURITY FIX: Validate content type for POST/PUT
        if request.method in ["POST", "PUT", "PATCH"]:
            content_type = request.headers.get("content-type", "")
            allowed_types = [
                "application/json",
                "multipart/form-data",
                "application/x-www-form-urlencoded"
            ]
            if not any(ct in content_type for ct in allowed_types):
                return JSONResponse(
                    status_code=415,
                    content={"detail": "Unsupported media type"}
                )
        
        response = await call_next(request)
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Simple rate limiting middleware
    """
    
    def __init__(self, app: ASGIApp, requests_per_minute: int = 100):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.request_counts = {}
        self.window_start = {}
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        
        # SECURITY FIX: Implement rate limiting
        current_time = time.time()
        
        # Reset window if needed
        if client_ip not in self.window_start or \
           current_time - self.window_start[client_ip] > 60:
            self.window_start[client_ip] = current_time
            self.request_counts[client_ip] = 0
        
        # Check rate limit
        self.request_counts[client_ip] = self.request_counts.get(client_ip, 0) + 1
        
        if self.request_counts[client_ip] > self.requests_per_minute:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests. Please try again later."}
            )
        
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(
            max(0, self.requests_per_minute - self.request_counts[client_ip])
        )
        
        return response


class AuditLoggingMiddleware(BaseHTTPMiddleware):
    """
    Log all requests for security auditing
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # SECURITY FIX: Log request details (sanitized)
        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        path = request.url.path
        
        try:
            response = await call_next(request)
            duration = time.time() - start_time
            
            # Log successful requests
            logger.info(
                f"Request: {method} {path} | "
                f"IP: {client_ip} | "
                f"Status: {response.status_code} | "
                f"Duration: {duration:.3f}s"
            )
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            
            # Log failed requests
            logger.error(
                f"Request Failed: {method} {path} | "
                f"IP: {client_ip} | "
                f"Error: {str(e)[:100]} | "
                f"Duration: {duration:.3f}s"
            )
            
            raise



class SSRFPreventionMiddleware(BaseHTTPMiddleware):
    """
    Prevent Server-Side Request Forgery (SSRF) attacks
    Validates URLs in request parameters
    """
    
    # Patterns that might indicate SSRF attempts
    SUSPICIOUS_PATTERNS = [
        r'localhost',
        r'127\.0\.0\.\d+',
        r'0\.0\.0\.0',
        r'169\.254\.169\.254',  # AWS/Azure metadata
        r'metadata\.google\.internal',  # GCP metadata
        r'::1',  # IPv6 localhost
        r'0000:',  # IPv6 variations
    ]
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Check query parameters for suspicious URLs
        for param_name, param_value in request.query_params.items():
            if self._is_suspicious_url(param_value):
                logger.warning(
                    f"SSRF attempt detected: {param_name}={param_value[:50]} "
                    f"from IP: {request.client.host if request.client else 'unknown'}"
                )
                return JSONResponse(
                    status_code=400,
                    content={"detail": "Invalid URL parameter"}
                )
        
        response = await call_next(request)
        return response
    
    def _is_suspicious_url(self, value: str) -> bool:
        """Check if value contains suspicious URL patterns"""
        if not isinstance(value, str):
            return False
        
        value_lower = value.lower()
        
        # Check for URL-like patterns
        if not any(proto in value_lower for proto in ['http://', 'https://', 'ftp://']):
            return False
        
        # Check against suspicious patterns
        for pattern in self.SUSPICIOUS_PATTERNS:
            if re.search(pattern, value_lower, re.IGNORECASE):
                return True
        
        return False
