# StruMind Architecture

## System Overview

StruMind is a microservice-based structural engineering platform with AI/ML capabilities, designed for scalability and continuous learning.

## Architecture Layers

### 1. Presentation Layer (Frontend)
- **Technology**: Next.js 14 + React + TypeScript
- **UI Framework**: TailwindCSS
- **3D Rendering**: Three.js + WebGL
- **State Management**: React Hooks
- **Real-time**: WebSocket connections

**Components:**
- Model Viewer (Three.js canvas)
- AI Assistant (chat interface)
- Analysis Dashboard
- Design Interface
- Detailing & BBS Generator
- BIM Integration Panel

### 2. API Gateway Layer
- **Technology**: FastAPI
- **Authentication**: JWT + OAuth2
- **Rate Limiting**: API Gateway throttling
- **CORS**: Configured for cross-origin requests

### 3. Business Logic Layer

#### Structural Engine Module
- **Geometry Engine**: Node/element creation, validation
- **Analysis Engine**: Static, modal, pushover, time-history
- **Design Module**: IS 456, ACI 318, IS 800, AISC
- **Detailing Module**: BBS, BOQ, drawing generation
- **Optimization**: AI-driven section optimization

#### AI/ML Module
- **Auto-Modeler**: CNN for drawing interpretation
- **Design Assistant**: Neural network for optimal sections
- **Error Checker**: Anomaly detection (Isolation Forest)
- **Continuous Learning**: Automated retraining pipeline

#### BIM Module
- **IFC Handler**: Import/export IFC files
- **Visualization Engine**: Three.js scene generation
- **Sync Manager**: Bidirectional sync with Revit/Tekla

### 4. Data Layer
- **Primary Database**: PostgreSQL 15
- **Schema**:
  - projects (id, name, client, location, created_at)
  - models (id, project_id, geometry_data, materials, sections)
  - analysis_results (id, model_id, type, results_json)
  - designs (id, model_id, code, reinforcement)
  - detailing (id, design_id, drawings, bbs, boq)
  - ai_feedback (id, model_id, user_feedback)

### 5. ML Model Registry
- **Storage**: File system + S3
- **Versioning**: Timestamp-based versions
- **Tracking**: Model performance metrics
- **Format**: PyTorch .pt files

### 6. Infrastructure Layer

#### Containerization
- **Docker**: Multi-stage builds
- **Docker Compose**: Local development

#### Orchestration
- **Kubernetes**: Production deployment
- **Auto-scaling**: HPA based on CPU/memory
- **Load Balancing**: Service mesh

#### Monitoring
- **Metrics**: Prometheus
- **Visualization**: Grafana dashboards
- **Logging**: Structured JSON logs
- **Tracing**: OpenTelemetry (future)

## Data Flow

### Analysis Workflow
1. User creates/imports model → Frontend
2. Model data sent to API → Backend
3. Geometry validation → Geometry Engine
4. Stiffness matrix assembly → Analysis Engine
5. Solver execution (LU/Eigenvalue) → NumPy/SciPy
6. Results stored → PostgreSQL
7. Visualization data generated → BIM Module
8. Results displayed → Frontend

### ML Prediction Workflow
1. User requests design suggestion → Frontend
2. Request sent to ML API → Backend
3. Feature extraction → ML Module
4. Model inference (PyTorch) → Design Assistant
5. Predictions returned → Frontend
6. User approves/rejects → Feedback stored

### Continuous Learning Workflow
1. User feedback collected → Learning API
2. Data anonymized → Learning Pipeline
3. Training queue updated → PostgreSQL
4. Scheduled retraining triggered → ML Module
5. New model version saved → Model Registry
6. Performance metrics logged → Monitoring

## Security

- **Authentication**: JWT tokens with expiration
- **Authorization**: Role-based access control (future)
- **Data Encryption**: TLS in transit, encrypted at rest
- **API Security**: Rate limiting, input validation
- **Secrets Management**: Kubernetes secrets

## Scalability

- **Horizontal Scaling**: Multiple backend replicas
- **Database**: Connection pooling, read replicas
- **Caching**: Redis for session/results (future)
- **CDN**: Static assets delivery (future)
- **Async Processing**: Celery for long-running tasks (future)

## Technology Stack Summary

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js, React, TypeScript, Three.js |
| Backend | Python, FastAPI, SQLAlchemy |
| Database | PostgreSQL 15 |
| ML/AI | PyTorch, TensorFlow, Scikit-learn |
| Analysis | NumPy, SciPy |
| Containerization | Docker, Docker Compose |
| Orchestration | Kubernetes |
| Monitoring | Prometheus, Grafana |
| CI/CD | GitHub Actions |
| Cloud | AWS EC2, S3 (future) |
