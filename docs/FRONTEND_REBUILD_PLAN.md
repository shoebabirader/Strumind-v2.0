# Frontend Rebuild Plan - From Scratch

**Date:** October 16, 2025  
**Status:** 📋 Planning Phase

---

## 🎯 Objective

Build a **clean, modern, professional** frontend for StruMind from scratch that:
- ✅ Connects seamlessly to the existing backend API
- ✅ Provides excellent UX for structural engineers
- ✅ Uses modern best practices
- ✅ Is maintainable and scalable
- ✅ Has a clear, logical structure

---

## 🗑️ Step 1: Clean Slate

### Delete Current Frontend:
```bash
# Delete entire frontend directory
rm -rf frontend/
```

**Reason:** Start fresh with a clean, well-planned structure

---

## 🏗️ Step 2: Technology Stack (Modern & Clean)

### Core Framework:
- **Next.js 14** (App Router) - Modern React framework
- **TypeScript** - Type safety
- **React 18** - Latest React features

### UI & Styling:
- **Tailwind CSS** - Utility-first CSS
- **shadcn/ui** - High-quality component library
- **Lucide React** - Modern icon library

### 3D Visualization:
- **Three.js** - 3D rendering
- **React Three Fiber** - React renderer for Three.js
- **@react-three/drei** - Useful helpers

### State Management:
- **Zustand** - Lightweight state management
- **React Query (TanStack Query)** - Server state management

### API Communication:
- **Axios** - HTTP client
- **WebSocket** - Real-time updates

### Charts & Graphs:
- **Recharts** - React charts library

### Forms & Validation:
- **React Hook Form** - Form management
- **Zod** - Schema validation

---

## 📁 Step 3: Clean Directory Structure

```
frontend/
├── public/                      # Static assets
│   ├── icons/
│   ├── images/
│   └── favicon.ico
│
├── src/
│   ├── app/                     # Next.js App Router
│   │   ├── layout.tsx           # Root layout
│   │   ├── page.tsx             # Home page
│   │   ├── workspace/           # Main workspace
│   │   │   └── page.tsx
│   │   ├── projects/            # Projects list
│   │   │   └── page.tsx
│   │   └── api/                 # API routes (if needed)
│   │
│   ├── components/              # React components
│   │   ├── ui/                  # shadcn/ui components
│   │   │   ├── button.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── input.tsx
│   │   │   └── ...
│   │   │
│   │   ├── layout/              # Layout components
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Footer.tsx
│   │   │
│   │   ├── workspace/           # Workspace-specific
│   │   │   ├── Canvas3D.tsx     # 3D viewer
│   │   │   ├── Toolbar.tsx
│   │   │   ├── PropertiesPanel.tsx
│   │   │   └── ResultsPanel.tsx
│   │   │
│   │   ├── dialogs/             # Modal dialogs
│   │   │   ├── NodeDialog.tsx
│   │   │   ├── ElementDialog.tsx
│   │   │   ├── MaterialDialog.tsx
│   │   │   ├── LoadDialog.tsx
│   │   │   ├── AnalysisDialog.tsx
│   │   │   └── ...
│   │   │
│   │   └── charts/              # Chart components
│   │       ├── DeflectionChart.tsx
│   │       ├── MomentDiagram.tsx
│   │       └── CapacityCurve.tsx
│   │
│   ├── lib/                     # Utilities & helpers
│   │   ├── api/                 # API client
│   │   │   ├── client.ts        # Axios instance
│   │   │   ├── nodes.ts         # Node API calls
│   │   │   ├── elements.ts      # Element API calls
│   │   │   ├── materials.ts     # Material API calls
│   │   │   ├── loads.ts         # Load API calls
│   │   │   ├── analysis.ts      # Analysis API calls
│   │   │   └── index.ts
│   │   │
│   │   ├── three/               # Three.js utilities
│   │   │   ├── scene-setup.ts
│   │   │   ├── geometries.ts
│   │   │   └── materials.ts
│   │   │
│   │   ├── utils/               # General utilities
│   │   │   ├── units.ts         # Unit conversions
│   │   │   ├── validation.ts    # Validation helpers
│   │   │   └── formatting.ts    # Number formatting
│   │   │
│   │   └── constants.ts         # App constants
│   │
│   ├── hooks/                   # Custom React hooks
│   │   ├── useModel.ts          # Model state hook
│   │   ├── useAnalysis.ts       # Analysis hook
│   │   ├── useWebSocket.ts      # WebSocket hook
│   │   └── use3DScene.ts        # 3D scene hook
│   │
│   ├── store/                   # Zustand stores
│   │   ├── modelStore.ts        # Model state
│   │   ├── uiStore.ts           # UI state
│   │   └── analysisStore.ts     # Analysis state
│   │
│   ├── types/                   # TypeScript types
│   │   ├── model.ts             # Model types
│   │   ├── analysis.ts          # Analysis types
│   │   ├── api.ts               # API types
│   │   └── index.ts
│   │
│   └── styles/                  # Global styles
│       └── globals.css          # Global CSS + Tailwind
│
├── .env.local                   # Environment variables
├── .env.example                 # Example env file
├── .gitignore
├── next.config.js               # Next.js config
├── tailwind.config.ts           # Tailwind config
├── tsconfig.json                # TypeScript config
├── package.json                 # Dependencies
└── README.md                    # Frontend docs
```

---

## 🎨 Step 4: Core Features (MVP)

### Phase 1: Foundation (Day 1)
1. ✅ Project setup with Next.js 14
2. ✅ Install dependencies
3. ✅ Setup Tailwind CSS
4. ✅ Install shadcn/ui components
5. ✅ Create basic layout (Header, Sidebar)
6. ✅ Setup API client (Axios)
7. ✅ Create type definitions

### Phase 2: Model Building (Day 2)
1. ✅ 3D Canvas with Three.js
2. ✅ Node creation dialog
3. ✅ Element creation dialog
4. ✅ Material selection dialog
5. ✅ Basic 3D visualization
6. ✅ Properties panel

### Phase 3: Loading & Analysis (Day 3)
1. ✅ Load definition dialog
2. ✅ Analysis configuration dialog
3. ✅ Run analysis button
4. ✅ Results display
5. ✅ Deflection visualization
6. ✅ Force diagrams

### Phase 4: Advanced Features (Day 4)
1. ✅ Seismic analysis dialog
2. ✅ Wind analysis dialog
3. ✅ Pushover analysis
4. ✅ P-Delta analysis
5. ✅ Modal analysis
6. ✅ Design checks

### Phase 5: Polish (Day 5)
1. ✅ Error handling
2. ✅ Loading states
3. ✅ Responsive design
4. ✅ Keyboard shortcuts
5. ✅ Export/Import
6. ✅ Documentation

---

## 🔌 Step 5: Backend Integration

### API Endpoints to Connect:

```typescript
// Base URL
const API_BASE = 'http://localhost:8000/api'

// Endpoints
/api/nodes              # GET, POST, PUT, DELETE
/api/elements           # GET, POST, PUT, DELETE
/api/materials          # GET, POST, PUT, DELETE
/api/loads              # GET, POST, PUT, DELETE
/api/analysis/linear    # POST
/api/analysis/nonlinear # POST
/api/analysis/modal     # POST
/api/analysis/pushover  # POST
/api/analysis/pdelta    # POST
/api/seismic            # POST
/api/wind               # POST
/api/design/concrete    # POST
/api/design/steel       # POST
```

### WebSocket Connection:
```typescript
const WS_URL = 'ws://localhost:8000/ws'
// For real-time analysis progress
```

---

## 🎯 Step 6: Key Principles

### 1. **Clean Code**
- Small, focused components
- Clear naming conventions
- Proper TypeScript types
- Comprehensive comments

### 2. **Performance**
- Lazy loading for dialogs
- Memoization for expensive calculations
- Efficient 3D rendering
- Debounced inputs

### 3. **User Experience**
- Intuitive interface
- Clear feedback
- Error messages
- Loading states
- Keyboard shortcuts

### 4. **Maintainability**
- Modular structure
- Reusable components
- Consistent patterns
- Good documentation

---

## 📦 Step 7: Dependencies (package.json)

```json
{
  "name": "strumind-frontend",
  "version": "2.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^14.2.0",
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "typescript": "^5.4.0",
    
    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-dropdown-menu": "^2.0.6",
    "@radix-ui/react-label": "^2.0.2",
    "@radix-ui/react-select": "^2.0.0",
    "@radix-ui/react-tabs": "^1.0.4",
    
    "tailwindcss": "^3.4.0",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.0",
    
    "three": "^0.163.0",
    "@react-three/fiber": "^8.16.0",
    "@react-three/drei": "^9.105.0",
    
    "zustand": "^4.5.0",
    "@tanstack/react-query": "^5.28.0",
    
    "axios": "^1.6.8",
    "zod": "^3.22.4",
    "react-hook-form": "^7.51.0",
    "@hookform/resolvers": "^3.3.4",
    
    "recharts": "^2.12.0",
    "lucide-react": "^0.363.0"
  },
  "devDependencies": {
    "@types/node": "^20.11.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@types/three": "^0.163.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "eslint": "^8.57.0",
    "eslint-config-next": "^14.2.0"
  }
}
```

---

## 🚀 Step 8: Implementation Order

### Day 1: Foundation
```bash
1. Delete old frontend
2. Create new Next.js project
3. Install dependencies
4. Setup Tailwind + shadcn/ui
5. Create basic layout
6. Setup API client
7. Create type definitions
```

### Day 2: Core UI
```bash
1. Build 3D canvas component
2. Create node dialog
3. Create element dialog
4. Create material dialog
5. Implement basic 3D visualization
6. Add properties panel
```

### Day 3: Analysis
```bash
1. Create load dialog
2. Create analysis dialog
3. Implement run analysis
4. Display results
5. Show deflection visualization
6. Add force diagrams
```

### Day 4: Advanced
```bash
1. Add seismic analysis
2. Add wind analysis
3. Add pushover analysis
4. Add design checks
5. Add export/import
```

### Day 5: Polish
```bash
1. Error handling
2. Loading states
3. Responsive design
4. Testing
5. Documentation
```

---

## ✅ Success Criteria

### Must Have:
- ✅ Clean, modern UI
- ✅ 3D model visualization
- ✅ Node/element creation
- ✅ Material assignment
- ✅ Load definition
- ✅ Linear analysis
- ✅ Results display
- ✅ Backend integration

### Should Have:
- ✅ Seismic analysis
- ✅ Wind analysis
- ✅ Pushover analysis
- ✅ Design checks
- ✅ Export/Import
- ✅ Keyboard shortcuts

### Nice to Have:
- ✅ Real-time collaboration
- ✅ Version control
- ✅ Templates
- ✅ AI assistant

---

## 🎯 Next Steps

1. **Confirm Plan** - Review and approve this plan
2. **Delete Old Frontend** - Remove entire frontend directory
3. **Create New Project** - Initialize Next.js 14 project
4. **Install Dependencies** - Setup all required packages
5. **Build Foundation** - Create basic structure
6. **Implement Features** - Build features incrementally
7. **Test & Polish** - Ensure quality

---

**Ready to proceed?** 

Say "yes" and I'll:
1. Delete the old frontend
2. Create the new project structure
3. Start building the clean, modern frontend

---

**Date:** October 16, 2025  
**Status:** 📋 **PLAN READY - AWAITING APPROVAL**
