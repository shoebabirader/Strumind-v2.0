from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import init_db
from app.core.rate_limiter import RateLimiter
from app.api import (
    models, analysis, design, detailing, ml, bim, projects, 
    collaboration, learning, seismic, wind, pdelta, connections, 
    reporting, design_extended, templates, advanced_analysis, 
    specialized_design, serviceability, auth, versioning,
    websocket, cache_management, parallel_analysis, plugins,
    pushover, foundation, advanced_features, generative,
    nodes, elements, materials, loads, sections
)

# Initialize database (optional - core features work without it)
init_db()

app = FastAPI(
    title="StruMind API",
    description="""
    AI-powered structural engineering platform
    
    ⚠️ IMPORTANT: This is engineering software that requires professional verification.
    See /api/auth/disclaimer for full legal terms.
    """,
    version="1.0.0-beta",
    terms_of_service="/api/auth/disclaimer",
    contact={
        "name": "StruMind Support",
        "email": "support@strumind.com"
    }
)

# Rate limiting middleware (100 requests per minute)
app.add_middleware(RateLimiter, requests_per_minute=100)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# Authentication & Legal (public endpoints)
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])

# Core functionality
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(versioning.router, prefix="/api", tags=["versioning"])
app.include_router(models.router, prefix="/api/model", tags=["models"])

# Entity CRUD
app.include_router(nodes.router, prefix="/api/nodes", tags=["nodes"])
app.include_router(elements.router, prefix="/api/elements", tags=["elements"])
app.include_router(materials.router, prefix="/api/materials", tags=["materials"])
app.include_router(loads.router, prefix="/api/loads", tags=["loads"])
app.include_router(sections.router, prefix="/api/sections", tags=["sections"])

app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])
app.include_router(design.router, prefix="/api/design", tags=["design"])
app.include_router(detailing.router, prefix="/api/detailing", tags=["detailing"])
app.include_router(ml.router, prefix="/api/ml", tags=["ml"])
app.include_router(bim.router, prefix="/api/bim", tags=["bim"])
app.include_router(collaboration.router, prefix="/api/collaboration", tags=["collaboration"])
app.include_router(learning.router, prefix="/api/learning", tags=["learning"])
app.include_router(seismic.router, prefix="/api/seismic", tags=["seismic"])
app.include_router(wind.router, prefix="/api/wind", tags=["wind"])
app.include_router(pdelta.router, prefix="/api/pdelta", tags=["pdelta"])
app.include_router(connections.router, prefix="/api/connections", tags=["connections"])
app.include_router(reporting.router, prefix="/api/reporting", tags=["reporting"])
app.include_router(design_extended.router, prefix="/api/design-extended", tags=["design-extended"])
app.include_router(templates.router, prefix="/api/templates", tags=["templates"])
app.include_router(advanced_analysis.router, prefix="/api/advanced-analysis", tags=["advanced-analysis"])
app.include_router(specialized_design.router, prefix="/api/specialized-design", tags=["specialized-design"])
app.include_router(serviceability.router, prefix="/api/serviceability", tags=["serviceability"])

# Advanced features (Priority 2)
app.include_router(websocket.router, prefix="/api", tags=["websocket"])
app.include_router(cache_management.router, prefix="/api", tags=["cache"])
app.include_router(parallel_analysis.router, prefix="/api", tags=["parallel"])
app.include_router(plugins.router, prefix="/api", tags=["plugins"])

# Missing features implementation
app.include_router(pushover.router, prefix="/api", tags=["pushover"])
app.include_router(foundation.router, prefix="/api/foundation", tags=["foundation"])
app.include_router(advanced_features.router, prefix="/api/advanced", tags=["advanced"])
app.include_router(generative.router, prefix="/api/generative", tags=["generative"])

@app.get("/")
def root():
    return {
        "message": "StruMind API",
        "version": "1.0.0-beta",
        "status": "operational",
        "disclaimer": "Engineering software - professional verification required. See /api/auth/disclaimer",
        "docs": "/docs",
        "authentication": "/api/auth/login",
        "features": {
            "authentication": "JWT-based",
            "rate_limiting": "100 req/min",
            "websocket": "Real-time collaboration",
            "caching": "Result caching enabled",
            "parallel_execution": "Multi-core analysis",
            "plugins": "Extensible plugin system"
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0-beta",
        "rate_limit": "100 requests/minute"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
