"""
Cache management endpoints
"""
from fastapi import APIRouter, Depends
from app.core.cache import cache, analysis_cache
from app.core.security import get_current_active_user, TokenData

router = APIRouter()


@router.get("/cache/stats")
async def get_cache_stats(current_user: TokenData = Depends(get_current_active_user)):
    """Get cache statistics"""
    return cache.get_stats()


@router.post("/cache/clear")
async def clear_cache(current_user: TokenData = Depends(get_current_active_user)):
    """Clear all cache (admin only)"""
    cache.clear()
    return {"message": "Cache cleared successfully"}


@router.delete("/cache/analysis/{model_hash}")
async def invalidate_model_cache(
    model_hash: str,
    current_user: TokenData = Depends(get_current_active_user)
):
    """Invalidate cached analyses for a specific model"""
    # In production, verify user owns the model
    analysis_cache.invalidate_model({"hash": model_hash})
    return {"message": f"Cache invalidated for model {model_hash}"}


@router.get("/cache/health")
async def cache_health():
    """Check cache health"""
    stats = cache.get_stats()
    
    # Determine health status
    hit_rate = float(stats["hit_rate"].rstrip("%"))
    health_status = "healthy" if hit_rate > 50 else "degraded" if hit_rate > 20 else "poor"
    
    return {
        "status": health_status,
        "stats": stats,
        "recommendations": _get_recommendations(stats)
    }


def _get_recommendations(stats: dict) -> list:
    """Get cache optimization recommendations"""
    recommendations = []
    
    hit_rate = float(stats["hit_rate"].rstrip("%"))
    if hit_rate < 30:
        recommendations.append("Low cache hit rate - consider increasing TTL")
    
    if stats["size"] > 10000:
        recommendations.append("Large cache size - consider implementing LRU eviction")
    
    if stats["memory_usage_mb"] > 1000:
        recommendations.append("High memory usage - consider using Redis for caching")
    
    return recommendations
