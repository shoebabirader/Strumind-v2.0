from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.api import models, analysis, design, detailing, ml, bim, projects, collaboration, learning, templates

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="StruMind API",
    description="AI-powered structural engineering platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(models.router, prefix="/api/model", tags=["models"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])
app.include_router(design.router, prefix="/api/design", tags=["design"])
app.include_router(detailing.router, prefix="/api/detailing", tags=["detailing"])
app.include_router(ml.router, prefix="/api/ml", tags=["ml"])
app.include_router(bim.router, prefix="/api/bim", tags=["bim"])
app.include_router(collaboration.router, prefix="/api/collaboration", tags=["collaboration"])
app.include_router(learning.router, prefix="/api/learning", tags=["learning"])
app.include_router(templates.router, prefix="/api/templates", tags=["templates"])

@app.get("/")
def root():
    return {"message": "StruMind API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
