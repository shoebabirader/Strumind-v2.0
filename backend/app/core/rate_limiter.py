"""
Rate limiting middleware to prevent API abuse
"""
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, Tuple
import asyncio


# SECURITY FIX: Use timezone-aware datetime
from app.core.datetime_utils import utc_now
class RateLimiter(BaseHTTPMiddleware):
    """
    Rate limiting middleware
    Default: 100 requests per minute per IP
    """
    
    def __init__(self, app, requests_per_minute: int = 100):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = defaultdict(list)
        self.cleanup_interval = 60  # Clean up old entries every 60 seconds
        asyncio.create_task(self._cleanup_old_entries())
    
    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host
        
        # Skip rate limiting for health check
        if request.url.path in ["/health", "/"]:
            return await call_next(request)
        
        # Check rate limit
        now = utc_now()
        minute_ago = now - timedelta(minutes=1)
        
        # Remove old requests
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if req_time > minute_ago
        ]
        
        # Check if limit exceeded
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": f"Rate limit exceeded. Maximum {self.requests_per_minute} requests per minute.",
                    "retry_after": 60
                }
            )
        
        # Add current request
        self.requests[client_ip].append(now)
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(
            self.requests_per_minute - len(self.requests[client_ip])
        )
        response.headers["X-RateLimit-Reset"] = str(int((now + timedelta(minutes=1)).timestamp()))
        
        return response
    
    async def _cleanup_old_entries(self):
        """Periodically clean up old entries to prevent memory leak"""
        while True:
            await asyncio.sleep(self.cleanup_interval)
            now = utc_now()
            minute_ago = now - timedelta(minutes=1)
            
            # Clean up old entries
            for ip in list(self.requests.keys()):
                self.requests[ip] = [
                    req_time for req_time in self.requests[ip]
                    if req_time > minute_ago
                ]
                # Remove empty entries
                if not self.requests[ip]:
                    del self.requests[ip]
