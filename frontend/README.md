# StruMind Frontend - Next.js 15 + React 19

Complete production-ready structural engineering platform frontend connecting to 150+ backend APIs.

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## 📁 Project Structure

```
src/
├── app/                    # Next.js 15 App Router
│   ├── layout.tsx         # Root layout with providers
│   ├── page.tsx           # Landing page
│   ├── login/             # Authentication pages
│   ├── register/
│   └── workspace/         # Main workspace
├── components/
│   ├── dialogs/           # 50+ dialog components
│   ├── panels/            # Side panels and tools
│   ├── tables/            # Data tables with TanStack Table
│   ├── viewport/          # 3D viewport with Three.js
│   ├── layout/            # Layout components
│   └── ui/                # Radix UI components
├── hooks/                 # Custom React hooks
├── stores/                # Zustand state management
├── lib/
│   └── api/              # 45 API client files
├── types/                # TypeScript definitions
└── utils/                # Utility functions
```

## 🔌 API Coverage (150+ Endpoints)

### Core CRUD (33 APIs)
- ✅ Projects (4)
- ✅ Nodes (5)
- ✅ Elements (5)
- ✅ Materials (6)
- ✅ Loads (7)
- ✅ Sections (6)

### Analysis (46 APIs)
- ✅ Basic Analysis (1)
- ✅ Advanced Analysis (15)
- ✅ Seismic (8)
- ✅ Wind (10)
- ✅ Pushover (3)
- ✅ P-Delta (3)
- ✅ Parallel Processing (4)

### Design (32 APIs)
- ✅ Basic Design (10)
- ✅ Foundation (4)
- ✅ Connections (3)
- ✅ Specialized Design (12)
- ✅ Serviceability (6)

### AI/ML (11 APIs)
- ✅ ML Predictions
- ✅ Generative Design
- ✅ Topology Optimization
- ✅ Learning & Feedback

### Collaboration (8 APIs)
- ✅ WebSocket Real-time
- ✅ Comments
- ✅ Active Users

### BIM Integration (6 APIs)
- ✅ IFC Import/Export
- ✅ 3D Visualization
- ✅ Stress/Deformation Views

### Additional Features
- ✅ Reporting & Detailing (3)
- ✅ Version Control (5)
- ✅ Templates (2)
- ✅ Plugins (9)
- ✅ Cache Management (4)

## 🛠️ Tech Stack

- **Framework**: Next.js 15 + React 19 + TypeScript
- **Styling**: Tailwind CSS + Radix UI + Framer Motion
- **3D Graphics**: Three.js + React Three Fiber + Drei
- **State Management**: Zustand + React Query + Immer
- **Forms**: React Hook Form + Zod
- **Tables**: TanStack Table + React Virtual
- **Charts**: Recharts + D3.js + Plotly.js
- **Real-time**: Socket.io
- **File Handling**: React Dropzone

## 🎨 Features

- ✅ Complete 3D viewport with node/element visualization
- ✅ Real-time collaboration with WebSocket
- ✅ Comprehensive analysis tools (Linear, Modal, Seismic, Wind, Pushover)
- ✅ Code-based design (IS456, IS800, ACI, AISC, Eurocode)
- ✅ AI-powered design suggestions
- ✅ BIM integration (IFC import/export)
- ✅ Automated reporting and detailing
- ✅ Version control and comparison
- ✅ Plugin system for extensibility
- ✅ Responsive design (desktop/tablet/mobile)
- ✅ Dark mode support
- ✅ Keyboard shortcuts
- ✅ Accessibility (WCAG 2.1 AA)

## 📦 Installation

```bash
npm install
```

## 🔧 Configuration

Copy `.env.example` to `.env.local` and configure:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

## 🚀 Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## 🏗️ Build

```bash
npm run build
npm start
```

## 📝 License

Proprietary - StruMind Engineering Software
