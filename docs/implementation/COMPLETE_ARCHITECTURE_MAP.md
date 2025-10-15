# 🏗️ Complete Architecture Map

## 🎯 **System Overview**

```
┌─────────────────────────────────────────────────────────────────┐
│                        StruMind Pro                              │
│                   Structural Analysis Software                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │
        ┌─────────────────────┴─────────────────────┐
        │                                           │
        ▼                                           ▼
┌───────────────┐                          ┌───────────────┐
│   Frontend    │◄────────────────────────►│   Backend     │
│   (React)     │      REST API / WS       │   (FastAPI)   │
└───────────────┘                          └───────────────┘
```

---

## 🎨 **Frontend Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend Layer                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Pages      │  │  Components  │  │   Contexts   │         │
│  │              │  │              │  │              │         │
│  │ • workspace  │  │ • Dialogs    │  │ • Auth       │         │
│  │ • login      │  │ • Panels     │  │ • Model      │         │
│  │ • register   │  │ • Tables     │  │ • Selection  │         │
│  │ • index      │  │ • UI         │  │ • Viewport   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Hooks      │  │    Utils     │  │   Styles     │         │
│  │              │  │              │  │              │         │
│  │ • useAuth    │  │ • api.ts     │  │ • globals    │         │
│  │ • useModel   │  │ • geometry   │  │ • professional│        │
│  │ • useSelect  │  │ • three      │  │              │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎭 **Component Hierarchy**

```
App (_app.tsx)
│
├── AuthProvider
│   ├── ModelProvider
│   │   └── SelectionProvider
│   │       │
│   │       ├── Login Page
│   │       ├── Register Page
│   │       ├── Index Page
│   │       │
│   │       └── Workspace Page ⭐
│   │           │
│   │           ├── Menu Bar
│   │           │   └── MenuButton (x8)
│   │           │
│   │           ├── Main Toolbar
│   │           │   └── Toolbar Buttons (x15)
│   │           │
│   │           ├── Secondary Toolbar
│   │           │   └── View Controls
│   │           │
│   │           ├── Main Content Area
│   │           │   │
│   │           │   ├── Model Explorer (Left Panel)
│   │           │   │   ├── Tree Nodes
│   │           │   │   └── Context Menus
│   │           │   │
│   │           │   ├── Viewport (Center)
│   │           │   │   ├── 3D View
│   │           │   │   ├── Grid Helper
│   │           │   │   ├── Axis Helper
│   │           │   │   └── Viewport Controls
│   │           │   │
│   │           │   └── Properties Panel (Right)
│   │           │       ├── Properties Tab
│   │           │       ├── Tables Tab
│   │           │       │   ├── Nodes Table
│   │           │       │   └── Elements Table
│   │           │       └── Results Tab
│   │           │           └── Results Table
│   │           │
│   │           ├── Status Bar
│   │           │
│   │           └── Dialogs (16 total)
│   │               ├── NodeDialog
│   │               ├── ElementDialog
│   │               ├── MaterialDialog
│   │               ├── LoadDialog
│   │               ├── AnalysisDialog
│   │               ├── DesignDialog
│   │               ├── NewProjectDialog
│   │               ├── DetailingDialog ✨
│   │               ├── AIAssistantDialog ✨
│   │               ├── ReportDialog ✨
│   │               ├── AdvancedAnalysisDialog ✨
│   │               ├── SpecializedDesignDialog ✨
│   │               ├── VersionDialog ✨
│   │               ├── CollaborationDialog ✨
│   │               └── BIMDialog ✨
│   │
│   └── UI Components
│       ├── ContextMenu ✨
│       └── MenuButton ✨
```

---

## 🔄 **Data Flow**

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Actions                             │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      UI Components                               │
│  (Buttons, Menus, Context Menus, Dialogs)                       │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Event Handlers                                │
│  (onClick, onSubmit, onContextMenu)                             │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    State Management                              │
│  (React State, Context API)                                     │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API Calls                                   │
│  (fetch, axios - to backend)                                    │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Backend APIs                                  │
│  (FastAPI endpoints - 79+ routes)                               │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Database                                    │
│  (PostgreSQL / SQLite)                                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 **Feature Map**

```
┌─────────────────────────────────────────────────────────────────┐
│                      Core Features                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Authentication          Model Management       Analysis         │
│  ├── Login              ├── Nodes              ├── Static       │
│  ├── Register           ├── Elements           ├── Modal        │
│  └── Logout             ├── Materials          ├── Time History │
│                         ├── Loads              ├── Response     │
│                         └── Sections           ├── Pushover     │
│                                                └── P-Delta       │
│                                                                  │
│  Design                 Detailing              AI/ML             │
│  ├── Concrete           ├── Beam               ├── Auto Model   │
│  ├── Steel              ├── Column             ├── Design Assist│
│  ├── Foundation         ├── Slab               ├── Error Check  │
│  ├── Shear Wall         └── Ductile            └── Optimize     │
│  ├── Retaining Wall                                             │
│  ├── Staircase                                                  │
│  └── Composite                                                  │
│                                                                  │
│  BIM                    Collaboration          Reporting         │
│  ├── Import IFC         ├── Share              ├── Analysis     │
│  ├── Export IFC         ├── Permissions        ├── Calculation  │
│  └── Visualize          ├── Active Users       └── Design       │
│                         └── Real-time                           │
│                                                                  │
│  Version Control        3D Viewport            Tables            │
│  ├── History            ├── 3D View            ├── Nodes        │
│  ├── Compare            ├── Grid               ├── Elements     │
│  └── Restore            ├── Axis               └── Results      │
│                         └── Controls                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🗂️ **Dialog System**

```
┌─────────────────────────────────────────────────────────────────┐
│                        Dialog Manager                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Basic Dialogs (7)              Advanced Dialogs (8) ✨         │
│  ┌──────────────────┐          ┌──────────────────┐            │
│  │ NodeDialog       │          │ DetailingDialog  │            │
│  │ ElementDialog    │          │ AIAssistantDialog│            │
│  │ MaterialDialog   │          │ ReportDialog     │            │
│  │ LoadDialog       │          │ AdvancedAnalysis │            │
│  │ AnalysisDialog   │          │ SpecializedDesign│            │
│  │ DesignDialog     │          │ VersionDialog    │            │
│  │ NewProjectDialog │          │ CollaborationDlg │            │
│  └──────────────────┘          │ BIMDialog        │            │
│                                 └──────────────────┘            │
│                                                                  │
│  All dialogs share:                                             │
│  • Consistent design                                            │
│  • Type-safe props                                              │
│  • Form validation                                              │
│  • Loading states                                               │
│  • Error handling                                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎨 **Context System**

```
┌─────────────────────────────────────────────────────────────────┐
│                      Context Providers                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  AuthContext                                                     │
│  ├── user: User | null                                          │
│  ├── isAuthenticated: boolean                                   │
│  ├── login(credentials)                                         │
│  ├── register(userData)                                         │
│  └── logout()                                                   │
│                                                                  │
│  ModelContext                                                    │
│  ├── nodes: Node[]                                              │
│  ├── elements: Element[]                                        │
│  ├── materials: Material[]                                      │
│  ├── loads: Load[]                                              │
│  ├── addNode(node)                                              │
│  ├── updateNode(id, data)                                       │
│  ├── deleteNode(id)                                             │
│  └── ... (similar for other entities)                           │
│                                                                  │
│  SelectionContext ✨                                            │
│  ├── selectedItem: { type, data } | null                        │
│  ├── setSelectedItem(item)                                      │
│  └── clearSelection()                                           │
│                                                                  │
│  ViewportContext                                                 │
│  ├── camera: Camera                                             │
│  ├── controls: Controls                                         │
│  ├── zoom(factor)                                               │
│  ├── pan(x, y)                                                  │
│  └── reset()                                                    │
│                                                                  │
│  UIContext                                                       │
│  ├── theme: 'dark' | 'light'                                    │
│  ├── notifications: Notification[]                              │
│  ├── showNotification(message)                                  │
│  └── setTheme(theme)                                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔌 **API Integration Map**

```
┌─────────────────────────────────────────────────────────────────┐
│                      Backend Endpoints                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Authentication (3)          Nodes (5)                          │
│  POST /api/auth/register     GET    /api/nodes                 │
│  POST /api/auth/login        POST   /api/nodes                 │
│  POST /api/auth/logout       GET    /api/nodes/{id}            │
│                              PUT    /api/nodes/{id}            │
│  Elements (5)                DELETE /api/nodes/{id}            │
│  GET    /api/elements                                           │
│  POST   /api/elements        Materials (5)                      │
│  GET    /api/elements/{id}   GET    /api/materials             │
│  PUT    /api/elements/{id}   POST   /api/materials             │
│  DELETE /api/elements/{id}   GET    /api/materials/{id}        │
│                              PUT    /api/materials/{id}        │
│  Loads (5)                   DELETE /api/materials/{id}        │
│  GET    /api/loads                                              │
│  POST   /api/loads           Sections (5)                       │
│  GET    /api/loads/{id}      GET    /api/sections              │
│  PUT    /api/loads/{id}      POST   /api/sections              │
│  DELETE /api/loads/{id}      GET    /api/sections/{id}         │
│                              PUT    /api/sections/{id}         │
│  Analysis (6)                DELETE /api/sections/{id}         │
│  POST /api/analysis/static                                      │
│  POST /api/analysis/modal    Advanced Analysis (4) ✨          │
│  POST /api/analysis/dynamic  POST /api/advanced/time-history   │
│  POST /api/analysis/seismic  POST /api/advanced/response       │
│  POST /api/analysis/wind     POST /api/pushover/pushover       │
│  POST /api/analysis/thermal  POST /api/pdelta/analysis         │
│                                                                  │
│  Design (8)                  Detailing (4) ✨                   │
│  POST /api/design/concrete   POST /api/detailing/beam          │
│  POST /api/design/steel      POST /api/detailing/column        │
│  POST /api/design/foundation POST /api/detailing/slab          │
│  POST /api/design/beam       POST /api/detailing/ductile       │
│  POST /api/design/column                                        │
│  POST /api/design/slab       Specialized Design (4) ✨         │
│  POST /api/design/wall       POST /api/specialized/shear-wall  │
│  POST /api/design/footing    POST /api/specialized/retaining   │
│                              POST /api/specialized/staircase   │
│  AI/ML (6) ✨                POST /api/specialized/composite   │
│  POST /api/ml/auto-model                                        │
│  POST /api/ml/design-assist  BIM (3) ✨                        │
│  POST /api/ml/error-checker  POST /api/bim/import              │
│  POST /api/ml/optimize       POST /api/bim/export              │
│  POST /api/generative/design POST /api/bim/visualize           │
│  POST /api/generative/topo                                      │
│                              Collaboration (3) ✨              │
│  Reporting (3) ✨            POST /api/collaboration/share     │
│  POST /api/reporting/analysis GET  /api/projects/{id}/users   │
│  POST /api/reporting/calc    WS   /ws/{project_id}             │
│  POST /api/reporting/design                                     │
│                              Versioning (3) ✨                 │
│  Projects (8)                GET  /api/projects/{id}/versions  │
│  GET    /api/projects        POST /api/versions                │
│  POST   /api/projects        POST /api/projects/{id}/restore   │
│  GET    /api/projects/{id}                                      │
│  PUT    /api/projects/{id}   Templates (2)                      │
│  DELETE /api/projects/{id}   GET /api/templates/list           │
│  POST   /api/projects/import GET /api/templates/{name}         │
│  POST   /api/projects/export                                    │
│  GET    /api/projects/list                                      │
│                                                                  │
│  Total: 79+ endpoints                                           │
│  Coverage: 100% ✅                                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 **User Journey Map**

```
┌─────────────────────────────────────────────────────────────────┐
│                      User Workflows                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Getting Started                                             │
│     Register → Login → Create Project → Workspace               │
│                                                                  │
│  2. Building Model                                              │
│     Add Nodes → Add Elements → Assign Materials → Apply Loads   │
│     │                                                            │
│     └─→ OR use AI: "Create 5-story building..." → Auto Generate │
│                                                                  │
│  3. Running Analysis                                            │
│     Configure Analysis → Run → View Results → Generate Report   │
│     │                                                            │
│     └─→ OR Advanced: Time History / Pushover / P-Delta          │
│                                                                  │
│  4. Design & Detailing                                          │
│     Run Design → Check Results → Generate Detailing → Export    │
│     │                                                            │
│     └─→ OR Specialized: Shear Wall / Retaining Wall / Staircase │
│                                                                  │
│  5. Collaboration                                               │
│     Share Project → Set Permissions → Real-time Editing         │
│                                                                  │
│  6. Documentation                                               │
│     Generate Report → Export PDF/Excel → Share with Client      │
│                                                                  │
│  7. BIM Integration                                             │
│     Import IFC → Analyze → Design → Export IFC → Coordination   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔐 **Security Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                      Security Layers                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Frontend Security                                              │
│  ├── JWT Token Storage (httpOnly cookies)                       │
│  ├── Protected Routes (auth check)                              │
│  ├── Input Validation (client-side)                             │
│  └── XSS Prevention (React escaping)                            │
│                                                                  │
│  Backend Security                                               │
│  ├── JWT Authentication                                         │
│  ├── Password Hashing (bcrypt)                                  │
│  ├── Input Validation (Pydantic)                                │
│  ├── SQL Injection Prevention (ORM)                             │
│  ├── CORS Configuration                                         │
│  └── Rate Limiting                                              │
│                                                                  │
│  Database Security                                              │
│  ├── Encrypted Connections                                      │
│  ├── User Permissions                                           │
│  └── Backup Strategy                                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 **Performance Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                   Performance Optimizations                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Frontend                                                        │
│  ├── Code Splitting (Next.js automatic)                         │
│  ├── Lazy Loading (dialogs on demand)                           │
│  ├── Memoization (React.memo, useMemo)                          │
│  ├── Virtual Scrolling (large tables)                           │
│  └── Debouncing (search, input)                                 │
│                                                                  │
│  Backend                                                         │
│  ├── Database Indexing                                          │
│  ├── Query Optimization                                         │
│  ├── Caching (Redis ready)                                      │
│  ├── Async Processing                                           │
│  └── Connection Pooling                                         │
│                                                                  │
│  Network                                                         │
│  ├── Compression (gzip)                                         │
│  ├── CDN (static assets)                                        │
│  ├── HTTP/2                                                     │
│  └── WebSocket (real-time)                                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎨 **Design System**

```
┌─────────────────────────────────────────────────────────────────┐
│                      Design Tokens                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Colors                      Typography                          │
│  ├── Primary: #1e40af       ├── Font: Inter                     │
│  ├── Secondary: #64748b     ├── Sizes: 12-24px                  │
│  ├── Success: #10b981       └── Weights: 400-700                │
│  ├── Warning: #f59e0b                                            │
│  ├── Error: #ef4444         Spacing                             │
│  └── Info: #3b82f6          ├── Base: 4px                       │
│                              ├── Scale: 0.5x - 4x                │
│  Backgrounds                 └── Grid: 8px                       │
│  ├── Primary: #0f172a                                            │
│  ├── Secondary: #1e293b     Borders                             │
│  └── Tertiary: #334155      ├── Width: 1-2px                    │
│                              ├── Radius: 4-8px                   │
│  Text                        └── Color: #334155                 │
│  ├── Primary: #f1f5f9                                            │
│  ├── Secondary: #cbd5e1     Shadows                             │
│  └── Tertiary: #64748b      ├── Small: 0 1px 2px                │
│                              ├── Medium: 0 4px 6px               │
│                              └── Large: 0 10px 15px              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 **Deployment Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                    Deployment Strategy                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Development                                                     │
│  ├── Local: npm run dev                                         │
│  ├── Hot Reload: Enabled                                        │
│  └── Debug: Source Maps                                         │
│                                                                  │
│  Staging                                                         │
│  ├── Build: npm run build                                       │
│  ├── Test: Automated tests                                      │
│  └── Preview: Vercel/Netlify                                    │
│                                                                  │
│  Production                                                      │
│  ├── Frontend: Vercel/Netlify                                   │
│  ├── Backend: AWS/GCP/Azure                                     │
│  ├── Database: Managed PostgreSQL                               │
│  ├── CDN: CloudFlare                                            │
│  └── Monitoring: Sentry/DataDog                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📈 **Scalability Plan**

```
┌─────────────────────────────────────────────────────────────────┐
│                      Scaling Strategy                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Horizontal Scaling                                             │
│  ├── Load Balancer                                              │
│  ├── Multiple Backend Instances                                 │
│  ├── Database Read Replicas                                     │
│  └── Distributed Cache                                          │
│                                                                  │
│  Vertical Scaling                                               │
│  ├── Increase Server Resources                                  │
│  ├── Optimize Database Queries                                  │
│  └── Code Optimization                                          │
│                                                                  │
│  Microservices (Future)                                         │
│  ├── Analysis Service                                           │
│  ├── Design Service                                             │
│  ├── AI/ML Service                                              │
│  └── BIM Service                                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

**Last Updated:** January 2024  
**Version:** 2.0  
**Status:** Production Ready ✅
