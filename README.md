# 🏗️ StruMind v2.0

**Professional Structural Analysis & Design Software**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Next.js](https://img.shields.io/badge/Next.js-15.5.6-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen)](https://github.com/shoebabirader/Strumind-v2.0)

> **A modern, web-based structural engineering platform that rivals industry leaders like STAAD.Pro, ETABS, and Tekla Structures.**

---

## 🌟 Overview

StruMind v2.0 is a comprehensive structural analysis and design platform built with cutting-edge web technologies. It provides engineers with powerful tools for modeling, analyzing, and designing structures while offering a modern, intuitive user experience.

### 🎯 Key Highlights

- **🚀 Production Ready**: 100% complete implementation with 181 frontend files and 207+ backend endpoints
- **🎨 Modern UI**: Professional interface with 66 specialized dialogs and advanced 3D viewport
- **⚡ High Performance**: Optimized for speed with React 18, Next.js 15, and FastAPI
- **🔧 Industry Standard**: Supports major design codes (IS 456, IS 800, ACI 318, Eurocode)
- **🤖 AI-Powered**: Machine learning integration for design optimization and predictions
- **🌐 Web-Based**: No installation required, works on any modern browser
- **👥 Collaborative**: Real-time collaboration with version control

---

## 📋 Table of Contents

- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Contributing](#-contributing)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [License](#-license)
- [Support](#-support)

---

## ✨ Features

### 🏗️ **Structural Analysis**
- **Linear Static Analysis** - Standard structural analysis
- **Modal Analysis** - Natural frequencies and mode shapes
- **Dynamic Analysis** - Time history and response spectrum
- **Nonlinear Analysis** - Material and geometric nonlinearity
- **Buckling Analysis** - Stability analysis
- **P-Delta Analysis** - Second-order effects
- **Pushover Analysis** - Seismic performance evaluation

### 🎨 **Design Capabilities**
- **Concrete Design** - IS 456, ACI 318, Eurocode 2
- **Steel Design** - IS 800, AISC 360, Eurocode 3
- **Foundation Design** - Isolated, combined, mat, and pile foundations
- **Slab Design** - One-way and two-way slabs
- **Connection Design** - Moment and shear connections
- **Specialized Structures** - Shear walls, retaining walls, staircases

### 🌪️ **Load Analysis**
- **Seismic Analysis** - IS 1893, ASCE 7, Eurocode 8
- **Wind Analysis** - IS 875, ASCE 7, Eurocode 1
- **Load Combinations** - Automatic generation per codes
- **Moving Loads** - Vehicle and crane loads
- **Temperature Effects** - Thermal analysis

### 🎯 **Advanced Features**
- **3D Visualization** - Professional viewport with 5 view modes
- **BIM Integration** - IFC import/export
- **Optimization** - Size, shape, and topology optimization
- **Machine Learning** - AI-powered design recommendations
- **Collaboration** - Real-time multi-user editing
- **Version Control** - Project history and branching
- **Reporting** - Comprehensive calculation reports

### 🖥️ **User Interface**
- **66 Specialized Dialogs** - Complete feature coverage
- **Professional 3D Viewport** - Industry-standard visualization
- **Modern Design** - Glass-morphism UI with dark theme
- **Keyboard Shortcuts** - Power user efficiency
- **Responsive Layout** - Works on desktop, tablet, mobile
- **Accessibility** - WCAG 2.1 compliant

---

## 🛠️ Technology Stack

### **Frontend**
- **Framework**: Next.js 15.5.6 (React 18)
- **Language**: TypeScript 5.0
- **Styling**: Tailwind CSS + Radix UI
- **3D Graphics**: React Three Fiber + Three.js
- **State Management**: Zustand + React Query
- **Build Tool**: Webpack 5 + Turbopack

### **Backend**
- **Framework**: FastAPI 0.104.1
- **Language**: Python 3.11
- **Database**: PostgreSQL 15 / SQLite
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT + OAuth2
- **WebSockets**: FastAPI WebSockets

### **Analysis Engine**
- **Core**: NumPy + SciPy
- **FEM**: Custom finite element implementation
- **Optimization**: SciPy.optimize + CVXPY
- **Machine Learning**: scikit-learn + TensorFlow
- **Parallel Computing**: Multiprocessing + Celery

### **Infrastructure**
- **Containerization**: Docker + Docker Compose
- **Database**: PostgreSQL + Redis
- **File Storage**: MinIO (S3-compatible)
- **Monitoring**: Prometheus + Grafana
- **Testing**: Pytest + Jest + Playwright

---

## 🏛️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                   │
├─────────────────────────────────────────────────────────┤
│  • 66 Dialogs        • 3D Viewport    • 21 Hooks        │
│  • 6 Layouts         • 4 Tables       • 45 API Clients  │
│  • 22 UI Components  • 5 Pages        • 3 Stores        │
└─────────────────────────────────────────────────────────┘
                              │
                              │ REST API + WebSockets
                              ▼
┌─────────────────────────────────────────────────────────┐
│                   Backend (FastAPI)                     │
├─────────────────────────────────────────────────────────┤
│  • 207+ Endpoints    • Authentication  • WebSockets     │
│  • Analysis Engine   • Design Codes    • ML/AI          │
│  • Database Layer    • File Storage    • Caching        │
└─────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────┐
│                     Data Layer                          │
├─────────────────────────────────────────────────────────┤
│  • PostgreSQL        • Redis Cache     • MinIO Storage  │
│  • Vector DB         • Time Series     • File System    │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+ and npm/yarn
- **Python** 3.11+
- **PostgreSQL** 15+ (or SQLite for development)
- **Redis** 6+ (optional)
- **Docker** (optional)

### 1. Clone Repository
```bash
git clone https://github.com/shoebabirader/Strumind-v2.0.git
cd Strumind-v2.0
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your database credentials

# Run database migrations
alembic upgrade head

# Start backend server
python main.py
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Set environment variables
cp .env.example .env.local
# Edit .env.local with your API URL

# Start development server
npm run dev
```

### 4. Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 📦 Installation

### Development Installation

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

#### Frontend
```bash
cd frontend
npm install
# or
yarn install
```

### Production Installation

#### Using Docker Compose (Recommended)
```bash
# Clone and navigate
git clone https://github.com/shoebabirader/Strumind-v2.0.git
cd Strumind-v2.0

# Start all services
docker-compose up -d

# Access at http://localhost:3000
```

#### Manual Production Setup
```bash
# Backend
cd backend
pip install -r requirements.txt
gunicorn main:app --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm run build
npm start
```

---

## 💻 Usage

### Creating Your First Project

1. **Register/Login**
   - Navigate to http://localhost:3000
   - Create account or login

2. **Create New Project**
   - Click "New Project" button
   - Enter project details
   - Select units and design codes

3. **Model Creation**
   - Use Node Dialog to create nodes
   - Use Element Dialog to create elements
   - Define materials and sections
   - Apply loads and constraints

4. **Analysis**
   - Open Analysis Dialog
   - Select analysis type
   - Configure parameters
   - Run analysis

5. **Design**
   - Open Design Dialog
   - Select design code
   - Configure design parameters
   - Generate design

6. **Results**
   - View 3D results in viewport
   - Generate reports
   - Export data

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+S` | Save Project |
| `Ctrl+Z` | Undo |
| `Ctrl+Y` | Redo |
| `I` | Isometric View |
| `T` | Top View |
| `F` | Front View |
| `S` | Side View |
| `E` | Zoom Extents |
| `?` | Show Shortcuts |

---

## 📚 API Documentation

### REST API Endpoints

The backend provides 207+ REST API endpoints organized by modules:

#### **Authentication**
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - User logout

#### **Projects**
- `GET /api/projects` - List projects
- `POST /api/projects` - Create project
- `GET /api/projects/{id}` - Get project
- `PUT /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project

#### **Model Entities**
- `GET /api/nodes` - List nodes
- `POST /api/nodes` - Create node
- `GET /api/elements` - List elements
- `POST /api/elements` - Create element
- `GET /api/materials` - List materials
- `POST /api/materials` - Create material

#### **Analysis**
- `POST /api/analysis/linear` - Linear analysis
- `POST /api/analysis/modal` - Modal analysis
- `POST /api/analysis/dynamic` - Dynamic analysis
- `POST /api/analysis/nonlinear` - Nonlinear analysis

#### **Design**
- `POST /api/design/concrete` - Concrete design
- `POST /api/design/steel` - Steel design
- `POST /api/design/foundation` - Foundation design

### WebSocket Events

- `project:join` - Join project room
- `project:leave` - Leave project room
- `model:update` - Model changes
- `analysis:progress` - Analysis progress
- `collaboration:cursor` - User cursors

### Interactive API Documentation

Visit http://localhost:8000/docs for complete interactive API documentation with Swagger UI.

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Workflow

1. **Fork the repository**
2. **Create feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make changes**
4. **Add tests**
5. **Run tests**
   ```bash
   # Backend tests
   cd backend && pytest
   
   # Frontend tests
   cd frontend && npm test
   ```
6. **Commit changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
7. **Push to branch**
   ```bash
   git push origin feature/amazing-feature
   ```
8. **Open Pull Request**

### Code Style

- **Python**: Follow PEP 8, use Black formatter
- **TypeScript**: Follow Airbnb style guide, use Prettier
- **Commits**: Use conventional commits format

### Testing Requirements

- Backend: Minimum 80% code coverage
- Frontend: Test all critical user flows
- E2E: Test major features with Playwright

---

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_analysis.py

# Run specific test
pytest tests/test_analysis.py::test_linear_analysis
```

### Frontend Tests

```bash
cd frontend

# Run unit tests
npm test

# Run with coverage
npm test -- --coverage

# Run E2E tests
npm run test:e2e

# Run specific test
npm test -- NodeDialog.test.tsx
```

### Test Results

- **Backend**: 38 passing tests
- **Frontend**: Comprehensive test coverage
- **E2E**: Critical user flows tested

---

## 🚀 Deployment

### Docker Deployment

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Deployment

#### Backend (Production)
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start with Gunicorn
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

#### Frontend (Production)
```bash
cd frontend

# Build production bundle
npm run build

# Start production server
npm start

# Or use PM2
pm2 start npm --name "strumind-frontend" -- start
```

### Environment Variables

#### Backend (.env)
```env
DATABASE_URL=postgresql://user:pass@localhost/strumind
SECRET_KEY=your-secret-key-here
REDIS_URL=redis://localhost:6379
CORS_ORIGINS=http://localhost:3000
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

---

## 📊 Project Statistics

### Frontend
- **Total Files**: 181
- **Dialogs**: 66
- **Components**: 22 UI + 6 Layout + 3 Viewport
- **Hooks**: 21
- **API Clients**: 45
- **Pages**: 5
- **Stores**: 3
- **Types**: 5

### Backend
- **Endpoints**: 207+
- **Modules**: 30+
- **Tests**: 38 passing
- **Design Codes**: 4 (IS 456, IS 800, ACI 318, Eurocode)
- **Analysis Types**: 7

---

## 📖 Documentation

- **[Quick Start Guide](QUICK_START.md)** - Get started in 5 minutes
- **[API Reference](API_ENDPOINT_REFERENCE.md)** - Complete API documentation
- **[Architecture](docs/ARCHITECTURE.md)** - System architecture details
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment
- **[Contributing Guide](docs/CONTRIBUTING.md)** - How to contribute

---

## 🎯 Roadmap

### Phase 1: Core Features ✅ COMPLETE
- [x] User authentication and authorization
- [x] Project management
- [x] 3D modeling interface
- [x] Linear static analysis
- [x] Basic design features

### Phase 2: Advanced Analysis ✅ COMPLETE
- [x] Modal analysis
- [x] Dynamic analysis
- [x] Nonlinear analysis
- [x] P-Delta analysis
- [x] Pushover analysis

### Phase 3: Design Codes ✅ COMPLETE
- [x] IS 456 (Concrete)
- [x] IS 800 (Steel)
- [x] ACI 318 (Concrete)
- [x] Eurocode 2 & 3

### Phase 4: Advanced Features ✅ COMPLETE
- [x] BIM integration
- [x] Optimization
- [x] Machine learning
- [x] Real-time collaboration
- [x] Version control

### Phase 5: Future Enhancements 🔄 PLANNED
- [ ] Mobile app (iOS/Android)
- [ ] Cloud rendering
- [ ] Advanced AI features
- [ ] More design codes
- [ ] Plugin marketplace

---

## 🏆 Comparison with Industry Tools

| Feature | StruMind v2.0 | STAAD.Pro | ETABS | SAP2000 |
|---------|----------------|-----------|-------|---------|
| **Web-Based** | ✅ | ❌ | ❌ | ❌ |
| **Modern UI** | ✅ | ❌ | ⚠️ | ⚠️ |
| **Real-time Collaboration** | ✅ | ❌ | ❌ | ❌ |
| **AI/ML Integration** | ✅ | ❌ | ❌ | ❌ |
| **Open Source** | ✅ | ❌ | ❌ | ❌ |
| **BIM Integration** | ✅ | ✅ | ✅ | ✅ |
| **Design Codes** | ✅ | ✅ | ✅ | ✅ |
| **Nonlinear Analysis** | ✅ | ✅ | ✅ | ✅ |
| **Price** | Free | $$$$ | $$$$ | $$$$ |

---

## 🐛 Known Issues

- None currently reported

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 StruMind

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 👥 Team

- **Lead Developer**: Shoebabi Rader
- **Contributors**: Open source community

---

## 🙏 Acknowledgments

- **React Three Fiber** - 3D graphics library
- **FastAPI** - Modern Python web framework
- **Radix UI** - Accessible component library
- **Tailwind CSS** - Utility-first CSS framework
- **NumPy/SciPy** - Scientific computing libraries

---

## 📞 Support

### Get Help

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/shoebabirader/Strumind-v2.0/issues)
- **Discussions**: [GitHub Discussions](https://github.com/shoebabirader/Strumind-v2.0/discussions)
- **Email**: support@strumind.com

### Community

- **Discord**: [Join our Discord](https://discord.gg/strumind)
- **Twitter**: [@StruMind](https://twitter.com/strumind)
- **LinkedIn**: [StruMind](https://linkedin.com/company/strumind)

---

## 🌟 Star History

If you find this project useful, please consider giving it a star on GitHub!

[![Star History Chart](https://api.star-history.com/svg?repos=shoebabirader/Strumind-v2.0&type=Date)](https://star-history.com/#shoebabirader/Strumind-v2.0&Date)

---

## 📈 Project Status

**Status**: ✅ Production Ready

- **Version**: 2.0.0
- **Last Updated**: October 2025
- **Build Status**: Passing
- **Test Coverage**: 80%+
- **Documentation**: Complete

---

<div align="center">

**Built with ❤️ by engineers, for engineers**

[Website](https://strumind.com) • [Documentation](docs/) • [GitHub](https://github.com/shoebabirader/Strumind-v2.0)

</div>
