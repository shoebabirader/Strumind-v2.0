# StruMind

An AI-powered, full-scale structural engineering platform for modeling, analysis, design, detailing, BIM integration, and continuous learning.

## Architecture

- **Backend**: Python (FastAPI)
- **Database**: PostgreSQL
- **Frontend**: React/Next.js + TypeScript
- **AI/ML**: PyTorch + TensorFlow + Scikit-learn
- **BIM**: Three.js + WebGL + IFC.js
- **Deployment**: Docker + Kubernetes + AWS
- **Monitoring**: Prometheus + Grafana

## Features

### 🏗️ Interactive Model Creation (Like SAP2000/ETABS)
- **Model Builder Interface**
  - Create nodes with X, Y, Z coordinates
  - Define elements (beams, columns, trusses, slabs, shells)
  - Assign materials (Concrete M25, Steel Fe415, custom)
  - Select sections (300x450, 300x300, I-sections, custom)
  - Set restraints (Ux, Uy, Uz, Rx, Ry, Rz)
  
- **Quick Start Templates**
  - Simple Frame (2D portal)
  - Building Frame (3D multi-story)
  - Truss structures
  - Grid floor systems
  - Bridge structures
  
- **Loads Panel**
  - Point loads, distributed loads, moments
  - Multiple load cases (Dead, Live, Wind, Seismic)
  - Direction control (X, Y, Z, MX, MY, MZ)
  - Load case combinations

### Phase 1: Advanced Structural Engine ✅
- Static & modal analysis (stiffness matrix, eigenvalue)
- RC and steel design per IS 456/ACI 318/IS 800/AISC
- Automated detailing with BBS and BOQ
- Multi-format export (DXF, IFC, PDF)

### Phase 2: AI & ML Integration ✅
- Auto-modeler: CNN-based drawing interpretation
- Design assistant: Neural network for optimal sections
- Error checker: Anomaly detection for code violations

### Phase 3: Continuous Learning ✅
- Data ingestion from user projects
- Automated model retraining pipeline
- Version control for ML models
- User feedback integration

### Phase 4: BIM Integration ✅
- IFC import/export
- Three.js 3D visualization
- Real-time stress/deformation rendering
- Bidirectional sync with Revit/Tekla

### Phase 5: Project Management ✅
- PostgreSQL database with full schema
- Project, model, and analysis tracking
- Multi-user collaboration with WebSockets
- Threaded comments per element

### Phase 6: Cloud Deployment ✅
- Docker containerization
- Kubernetes orchestration with auto-scaling
- Prometheus metrics and monitoring
- CI/CD pipeline with GitHub Actions

### Phase 7: Frontend ✅
- Next.js dashboard with TailwindCSS
- Interactive 3D model viewer
- AI assistant chat interface
- Real-time collaboration features

## Model Creation Workflow

1. **Start New Project** → Select template or start blank
2. **Create Nodes** → Define coordinates and restraints
3. **Add Elements** → Connect nodes, assign materials/sections
4. **Apply Loads** → Define load cases and magnitudes
5. **Run Analysis** → Static, modal, or advanced
6. **Design** → Select code (IS/ACI/AISC) and generate design
7. **Detailing** → Auto-generate BBS, BOQ, and drawings
8. **Export** → IFC for BIM, DXF for CAD, PDF for reports

## Quick Start

### Local Development

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python main.py
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
# App: http://localhost:3000
```

### Docker Compose
```bash
docker-compose up
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# PostgreSQL: localhost:5432
```

### Kubernetes Deployment
```bash
kubectl apply -f kubernetes/secrets.yaml
kubectl apply -f kubernetes/pvc.yaml
kubectl apply -f kubernetes/postgres-deployment.yaml
kubectl apply -f kubernetes/deployment.yaml
```

## API Endpoints (26 Total)

### Projects (4)
- `POST /api/projects/create` - Create project
- `GET /api/projects/list` - List all projects
- `GET /api/projects/{id}` - Get project details
- `DELETE /api/projects/{id}` - Delete project

### Modeling (2)
- `POST /api/model/create` - Create structural model
- `GET /api/model/{id}` - Get model

### Templates (2)
- `GET /api/templates/list` - List available templates
- `GET /api/templates/{name}` - Get template geometry

### Analysis (1)
- `POST /api/analysis/run` - Run structural analysis

### Design (1)
- `POST /api/design/run` - Generate design per code

### Detailing (1)
- `POST /api/detailing/generate` - Generate drawings/BBS/BOQ

### ML & AI (2)
- `POST /api/ml/predict` - Get AI predictions
- `POST /api/ml/train` - Train ML models

### Learning (3)
- `POST /api/learning/feedback/submit` - Submit feedback
- `POST /api/learning/retrain` - Trigger retraining
- `GET /api/learning/models/versions` - List model versions

### BIM (5)
- `POST /api/bim/export/ifc` - Export to IFC
- `POST /api/bim/import/ifc` - Import IFC file
- `POST /api/bim/visualization/scene` - Generate 3D scene
- `POST /api/bim/visualization/stress` - Stress visualization
- `POST /api/bim/visualization/deformation` - Deformation visualization

### Collaboration (3)
- `WS /api/collaboration/ws/{project_id}` - WebSocket for real-time sync
- `POST /api/collaboration/comments/add` - Add comment
- `GET /api/collaboration/comments/{element_id}` - Get comments

### System (2)
- `GET /` - API info
- `GET /health` - Health check

## Testing

```bash
cd backend
pytest tests/ --cov=app
```

## Environment Variables

Create `.env` file in backend directory:
```
DATABASE_URL=postgresql://user:pass@localhost:5432/strumind
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## ML Model Training

The platform includes continuous learning capabilities:

1. User designs are anonymized and collected
2. Approved feedback triggers retraining
3. Models are versioned and tracked
4. New versions deployed automatically

## 📊 Competitive Analysis

We've conducted a comprehensive analysis of our position in the market:

- **[Competitive Analysis](COMPETITIVE_ANALYSIS.md)** - Detailed comparison with ETABS, SAP2000, STAAD, Tekla, Robot
- **[Feature Roadmap](FEATURE_ROADMAP.md)** - Implementation plan for missing features
- **[Market Position](MARKET_POSITION.md)** - Market segmentation and go-to-market strategy
- **[Executive Summary](EXECUTIVE_SUMMARY.md)** - Investment pitch and business case

### Key Findings

**Current Status**: 60% feature parity with market leaders

**Unique Advantages** (What competitors DON'T have):
- ✅ AI-powered design assistant
- ✅ Continuous learning system
- ✅ Cloud-native architecture
- ✅ Real-time collaboration
- ✅ 80% lower cost

**Critical Gaps** (What we NEED):
- 🔴 Seismic analysis (IS 1893, ASCE 7)
- 🔴 Wind analysis (IS 875, ASCE 7)
- 🔴 P-Delta analysis
- 🔴 Professional reporting
- 🔴 Steel connection design
- 🔴 More design codes (Eurocode, BS)

**Timeline**: 6-12 months to achieve 85% feature parity and capture SME market

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## License

Proprietary - All rights reserved
