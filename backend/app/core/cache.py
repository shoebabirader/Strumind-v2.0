"""
Result caching system for faster repeated analyses
"""
from typing import Any, Optional, Callable
import hashlib
import json
import pickle
from datetime import datetime, timedelta
from functools import wraps
import asyncio
# SECURITY FIX: Use timezone-aware datetime
from app.core.datetime_utils import utc_now


class CacheManager:
    """In-memory cache with TTL support"""
    
    def __init__(self, default_ttl: int = 3600):
        self.cache: dict = {}
        self.expiry: dict = {}
        self.default_ttl = default_ttl  # seconds
        self.hits = 0
        self.misses = 0
        self._cleanup_task = None
        
        # Cleanup task will be started when event loop is available
        # asyncio.create_task(self._cleanup_expired())
    
    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate cache key from function arguments"""
        # Create a deterministic string from args and kwargs
        key_data = {
            "prefix": prefix,
            "args": args,
            "kwargs": sorted(kwargs.items())
        }
        key_string = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.sha256(key_string.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        # Check if key exists and not expired
        if key in self.cache:
            # SECURITY FIX: Use timezone-aware datetime
            if key in self.expiry and utc_now() > self.expiry[key]:
                # Expired
                del self.cache[key]
                del self.expiry[key]
                self.misses += 1
                return None
            
            self.hits += 1
            return self.cache[key]
        
        self.misses += 1
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in cache with TTL"""
        self.cache[key] = value
        
        if ttl is None:
            ttl = self.default_ttl
        
        # SECURITY FIX: Use timezone-aware datetime
        self.expiry[key] = utc_now() + timedelta(seconds=ttl)
    
    def delete(self, key: str):
        """Delete key from cache"""
        if key in self.cache:
            del self.cache[key]
        if key in self.expiry:
            del self.expiry[key]
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
        self.expiry.clear()
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{hit_rate:.2f}%",
            "size": len(self.cache),
            "memory_usage_mb": self._estimate_size() / (1024 * 1024)
        }
    
    def _estimate_size(self) -> int:
        """Estimate cache size in bytes"""
        try:
            return len(pickle.dumps(self.cache))
        except:
            return 0
    
    async def _cleanup_expired(self):
        """Periodically clean up expired entries"""
        while True:
            await asyncio.sleep(300)  # Every 5 minutes
            
            # SECURITY FIX: Use timezone-aware datetime
            now = utc_now()
            expired_keys = [
                key for key, expiry in self.expiry.items()
                if now > expiry
            ]
            
            for key in expired_keys:
                self.delete(key)


# Global cache instance
cache = CacheManager(default_ttl=3600)  # 1 hour default


def cached(ttl: Optional[int] = None, prefix: str = ""):
    """
    Decorator for caching function results
    
    Usage:
    @cached(ttl=3600, prefix="analysis")
    def expensive_analysis(model_data):
        # ... expensive computation
        return results
    """
    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = cache._generate_key(prefix or func.__name__, *args, **kwargs)
            
            # Try to get from cache
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Store in cache
            cache.set(cache_key, result, ttl)
            
            return result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = cache._generate_key(prefix or func.__name__, *args, **kwargs)
            
            # Try to get from cache
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Store in cache
            cache.set(cache_key, result, ttl)
            
            return result
        
        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


class AnalysisCache:
    """Specialized cache for analysis results"""
    
    def __init__(self):
        self.cache_manager = cache
    
    def get_analysis_key(self, model_hash: str, analysis_type: str, params: dict) -> str:
        """Generate cache key for analysis"""
        key_data = {
            "model": model_hash,
            "type": analysis_type,
            "params": sorted(params.items())
        }
        key_string = json.dumps(key_data, sort_keys=True)
        return f"analysis_{hashlib.sha256(key_string.encode()).hexdigest()}"
    
    def get_model_hash(self, model_data: dict) -> str:
        """Generate hash of model data"""
        model_string = json.dumps(model_data, sort_keys=True, default=str)
        return hashlib.sha256(model_string.encode()).hexdigest()
    
    def cache_analysis(self, model_data: dict, analysis_type: str, 
                      params: dict, results: dict, ttl: int = 7200):
        """Cache analysis results"""
        model_hash = self.get_model_hash(model_data)
        cache_key = self.get_analysis_key(model_hash, analysis_type, params)
        
        cache_data = {
            "results": results,
            # SECURITY FIX: Use timezone-aware datetime
            "cached_at": utc_now().isoformat(),
            "model_hash": model_hash,
            "analysis_type": analysis_type
        }
        
        self.cache_manager.set(cache_key, cache_data, ttl)
    
    def get_cached_analysis(self, model_data: dict, analysis_type: str, 
                           params: dict) -> Optional[dict]:
        """Get cached analysis results"""
        model_hash = self.get_model_hash(model_data)
        cache_key = self.get_analysis_key(model_hash, analysis_type, params)
        
        cached_data = self.cache_manager.get(cache_key)
        if cached_data:
            return cached_data["results"]
        
        return None
    
    def invalidate_model(self, model_data: dict):
        """Invalidate all cached analyses for a model"""
        model_hash = self.get_model_hash(model_data)
        
        # Find and delete all keys with this model hash
        keys_to_delete = [
            key for key in self.cache_manager.cache.keys()
            if key.startswith(f"analysis_") and 
            self.cache_manager.cache[key].get("model_hash") == model_hash
        ]
        
        for key in keys_to_delete:
            self.cache_manager.delete(key)


# Global analysis cache
analysis_cache = AnalysisCache()
