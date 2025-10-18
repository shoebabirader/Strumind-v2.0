# 🔗 API Endpoint Reference

This document maps all backend endpoints to help fix frontend API calls.

## Backend Router Prefixes (from main.py)

Based on `backend/main.py`, here are the router prefixes:

```python
app.include_router(auth.router, prefix="/api/auth")
app.include_router(projects.router, prefix="/api/projects")
app.include_router(versioning.router, prefix="/api")
app.include_router(models.router, prefix="/api/model")
app.include_router(nodes.router, prefix="/api/nodes")
app.include_router(elements.router, prefix="/api/elements")
app.include_router(materials.router, prefix="/api/materials")
app.include_router(loads.router, prefix="/api/loads")
app.include_router(sections.router, prefix="/api/sections")
app.include_router(analysis.router, prefix="/api/analysis")
app.include_router(design.router, prefix="/api/design")
app.include_router(detailing.router, prefix="/api/detailing")
app.include_router(ml.router, prefix="/api/ml")
app.include_router(bim.router, prefix="/api/bim")
app.include_router(collaboration.router, prefix="/api/collaboration")
app.include_router(learning.router, prefix="/api/learning")
app.include_router(seismic.router, prefix="/api/seismic")
app.include_router(wind.router, prefix="/api/wind")
app.include_router(pdelta.router, prefix="/api/pdelta")
app.include_router(connections.router, prefix="/api/connections")
app.include_router(reporting.router, prefix="/api/reporting")
app.include_router(design_extended.router, prefix="/api/design-extended")
app.include_router(templates.router, prefix="/api/templates")
app.include_router(advanced_analysis.router, prefix="/api/advanced-analysis")
app.include_router(specialized_design.router, prefix="/api/specialized-design")
app.include_router(serviceability.router, prefix="/api/serviceability")
app.include_router(websocket.router, prefix="/api")
app.include_router(cache_management.router, prefix="/api")
app.include_router(parallel_analysis.router, prefix="/api")
app.include_router(plugins.router, prefix="/api")
app.include_router(pushover.router, prefix="/api")
app.include_router(foundation.router, prefix="/api/foundation")
app.include_router(advanced_features.router, prefix="/api/advanced")
app.include_router(generative.router, prefix="/api/generative")
app.include_router(slab_design.router, prefix="/api")
app.include_router(workflow.router, prefix="/api")
app.include_router(geometry.router, prefix="/api")
app.include_router(optimization.router, prefix="/api")
app.include_router(results_processing.router, prefix="/api")
app.include_router(load_combinations.router, prefix="/api")
app.include_router(nonlinear.router, prefix="/api")
app.include_router(units.router, prefix="/api")
app.include_router(dynamic_analysis.router, prefix="/api")
app.include_router(advanced_elements.router, prefix="/api")
```

## Common Pattern

Most frontend API clients should call:
- Base URL: `http://localhost:8000/api`
- Full endpoint: `http://localhost:8000/api/{router_prefix}/{endpoint}`

## Quick Fix Strategy

For each frontend API client file, ensure the endpoints match the backend router prefix + endpoint path.

Example:
- Frontend: `apiClient.post('/analysis/run', data)`
- Backend: `@router.post("/run")` with prefix `/api/analysis`
- Full URL: `http://localhost:8000/api/analysis/run` ✅

## Note

The frontend `apiClient` in `frontend/src/lib/api/client.ts` should have:
```typescript
baseURL: 'http://localhost:8000/api'
```

So frontend calls like `/analysis/run` become `http://localhost:8000/api/analysis/run`
