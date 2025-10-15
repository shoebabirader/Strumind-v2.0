# 🏗️ StruMind - AI-Powered Structural Engineering Platform

A comprehensive structural analysis and design platform with AI capabilities, real-time 3D visualization, and collaborative features.

[![Status](https://img.shields.io/badge/status-production%20ready-brightgreen)]()
[![Version](https://img.shields.io/badge/version-2.1-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

---

## ✨ Key Features

- 🎨 **Interactive 3D Visualization** - Real-time model rendering with Three.js
- 🤖 **AI-Powered Design** - Automated model generation and optimization
- 📊 **Advanced Analysis** - Static, modal, time-history, pushover, P-Delta
- 🏗️ **Specialized Design** - Concrete, steel, foundations, retaining walls
- 🔧 **Automated Detailing** - Reinforcement detailing for beams, columns, slabs
- 📄 **Professional Reports** - Export to PDF, Excel, Word
- 👥 **Real-time Collaboration** - Multi-user editing with WebSocket
- 🏢 **BIM Integration** - Import/export IFC files
- 📚 **Version Control** - Track changes and restore previous versions

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/strumind.git
cd strumind

# Start Backend
cd backend
pip install -r requirements.txt
python main.py

# Start Frontend (in new terminal)
cd frontend
npm install
npm run dev
```

### Access the Application
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

### First Steps
1. Register a new account
2. Login to the workspace
3. Add your first node (click 📦 button)
4. See it appear in the 3D viewer!

**📖 For detailed instructions, see [Quick Start Guide](docs/guides/QUICK_START_GUIDE.md)**

---

## 🎮 Using the 3D Viewer

The interactive 3D viewer allows you to visualize your structural model in real-time:

- **🖱️ Left-click + drag** - Rotate camera
- **🖱️ Right-click + drag** - Pan camera
- **🖱️ Mouse wheel** - Zoom in/out

Nodes appear as green spheres, elements as gray cylinders. The grid and axes help with orientation.

---

## 📚 Documentation

Complete documentation is available in the [docs](docs/) directory:

### Quick Links
- **[Quick Start Guide](docs/guides/QUICK_START_GUIDE.md)** - Get started in 5 minutes
- **[New Features Guide](docs/guides/NEW_FEATURES_QUICK_GUIDE.md)** - Learn about all features
- **[Quick Fix Guide](docs/guides/QUICK_FIX_GUIDE.md)** - Troubleshooting
- **[Backend Integration](docs/guides/BACKEND_INTEGRATION_GUIDE.md)** - API documentation
- **[Architecture Map](docs/implementation/COMPLETE_ARCHITECTURE_MAP.md)** - System architecture

### Documentation Structure
```
docs/
├── guides/              # User and developer guides
├── implementation/      # Technical documentation
└── archive/            # Historical documentation
```

---

## 🏗️ Architecture

### Backend
- **Framework:** FastAPI (Python)
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **APIs:** 79+ RESTful endpoints
- **WebSocket:** Real-time collaboration
- **AI/ML:** PyTorch, TensorFlow, Scikit-learn

### Frontend
- **Framework:** Next.js 13+ with TypeScript
- **3D Engine:** Three.js with React Three Fiber
- **State:** React Context API
- **Styling:** Tailwind CSS + Custom CSS
- **UI:** 16 comprehensive dialogs, 30+ components

### Features Coverage
- ✅ Authentication & Authorization
- ✅ Project Management
- ✅ Node & Element CRUD
- ✅ Material & Section Libraries
- ✅ Load Definition
- ✅ Static & Dynamic Analysis
- ✅ Concrete & Steel Design
- ✅ Automated Detailing
- ✅ AI-Powered Features
- ✅ BIM Import/Export
- ✅ Report Generation
- ✅ Version Control
- ✅ Real-time Collaboration

---

## 🎯 Project Status

### Current Version: 2.1 (Production Ready)

| Component | Status | Coverage |
|-----------|--------|----------|
| Backend APIs | ✅ Complete | 79+ endpoints |
| Frontend UI | ✅ Complete | 100% |
| 3D Visualization | ✅ Working | Interactive |
| Database | ✅ Persisting | SQLite/PostgreSQL |
| Documentation | ✅ Complete | Comprehensive |

**All core features are implemented and functional!**

---

## 🛠️ Technology Stack

### Core Technologies
- **Backend:** Python 3.11, FastAPI, SQLAlchemy, Pydantic
- **Frontend:** React 18, Next.js 13, TypeScript, Tailwind CSS
- **3D Graphics:** Three.js, React Three Fiber, @react-three/drei
- **Database:** SQLite (development), PostgreSQL (production)
- **Authentication:** JWT tokens, bcrypt password hashing

### Development Tools
- **Version Control:** Git
- **Package Management:** npm (frontend), pip (backend)
- **Code Quality:** TypeScript, ESLint, Prettier
- **Testing:** Jest, Pytest (ready for implementation)

---

## 📦 Project Structure

```
strumind/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints (79+ routes)
│   │   ├── core/           # Core functionality
│   │   ├── models/         # Database models
│   │   └── services/       # Business logic
│   ├── main.py             # Application entry point
│   └── requirements.txt    # Python dependencies
│
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── dialogs/   # 16 feature dialogs
│   │   │   ├── panels/    # UI panels
│   │   │   ├── tables/    # Data tables
│   │   │   ├── viewport/  # 3D viewer
│   │   │   └── ui/        # Reusable UI components
│   │   ├── contexts/      # React contexts
│   │   ├── hooks/         # Custom hooks
│   │   ├── lib/           # Utilities
│   │   ├── pages/         # Next.js pages
│   │   └── styles/        # CSS styles
│   ├── package.json       # Node dependencies
│   └── tsconfig.json      # TypeScript config
│
├── docs/                   # Documentation
│   ├── guides/            # User guides
│   ├── implementation/    # Technical docs
│   └── archive/           # Historical docs
│
├── docker-compose.yml     # Docker configuration
└── README.md              # This file
```

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Three.js community for 3D visualization
- FastAPI team for the excellent framework
- React and Next.js teams
- All contributors and testers

---

## 📞 Support

- **Documentation:** [docs/](docs/)
- **Issues:** [GitHub Issues](https://github.com/yourusername/strumind/issues)
- **Email:** support@strumind.com

---

## 🎉 What's New in v2.1

- ✨ **Interactive 3D Viewer** - Real-time model visualization with camera controls
- 🎨 **Enhanced UI** - Professional dark theme with 16 feature dialogs
- 🔧 **Complete Backend Integration** - All 79+ APIs connected
- 📊 **Data Persistence** - SQLite database with automatic loading
- 🐛 **Bug Fixes** - React hooks error fixed, viewport rendering optimized
- 📚 **Comprehensive Documentation** - Organized docs directory

---

**Built with ❤️ for structural engineers**

*Last Updated: October 2025*
