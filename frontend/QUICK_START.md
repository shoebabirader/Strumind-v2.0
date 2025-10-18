# StruMind Frontend - Quick Start Guide

## 🚀 Get Started in 3 Minutes

### Step 1: Install Dependencies

```bash
cd frontend
npm install
```

This will install all required packages:
- Next.js 15 + React 19
- Tailwind CSS + Radix UI
- Three.js + React Three Fiber
- Zustand + React Query
- And 30+ other dependencies

### Step 2: Configure Environment

The `.env.local` file is already configured for local development:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

### Step 3: Start Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## ✅ What's Working Now

### Pages
- ✅ Landing page (http://localhost:3000)
- ✅ Beautiful hero section with features
- ✅ Navigation to login/register

### API Integration
- ✅ 11 API client files connected to backend
- ✅ Authentication APIs (login, register, disclaimer)
- ✅ Core CRUD APIs (projects, nodes, elements, materials, loads, sections)
- ✅ Analysis APIs (seismic, wind)

### State Management
- ✅ Authentication store (Zustand)
- ✅ Model store (structural data)
- ✅ UI store (dialogs, panels, theme)

### Styling
- ✅ Tailwind CSS configured
- ✅ Dark mode support
- ✅ Radix UI theme variables
- ✅ Custom scrollbars
- ✅ Responsive design

## 🔧 Development Commands

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Type check
npm run type-check

# Lint code
npm run lint
```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js 15 App Router
│   │   ├── layout.tsx         # Root layout ✅
│   │   ├── page.tsx           # Landing page ✅
│   │   ├── providers.tsx      # React Query provider ✅
│   │   └── globals.css        # Global styles ✅
│   ├── components/
│   │   └── ui/
│   │       └── button.tsx     # Button component ✅
│   ├── lib/
│   │   ├── api/               # API clients (11/45 done)
│   │   │   ├── client.ts      # Axios client ✅
│   │   │   ├── auth.ts        # Auth APIs ✅
│   │   │   ├── projects.ts    # Project APIs ✅
│   │   │   ├── nodes.ts       # Node APIs ✅
│   │   │   ├── elements.ts    # Element APIs ✅
│   │   │   ├── materials.ts   # Material APIs ✅
│   │   │   ├── loads.ts       # Load APIs ✅
│   │   │   ├── sections.ts    # Section APIs ✅
│   │   │   ├── analysis.ts    # Analysis APIs ✅
│   │   │   ├── seismic.ts     # Seismic APIs ✅
│   │   │   └── wind.ts        # Wind APIs ✅
│   │   └── utils.ts           # Utilities ✅
│   ├── stores/                # Zustand stores
│   │   ├── authStore.ts       # Auth state ✅
│   │   ├── modelStore.ts      # Model state ✅
│   │   └── uiStore.ts         # UI state ✅
│   └── types/                 # TypeScript types
│       ├── api.ts             # API types ✅
│       ├── auth.ts            # Auth types ✅
│       ├── model.ts           # Model types ✅
│       ├── analysis.ts        # Analysis types ✅
│       └── design.ts          # Design types ✅
├── package.json               # Dependencies ✅
├── tsconfig.json              # TypeScript config ✅
├── tailwind.config.js         # Tailwind config ✅
├── next.config.js             # Next.js config ✅
└── .env.local                 # Environment variables ✅
```

## 🎯 Next Development Steps

### Phase 1: Authentication (1-2 hours)
1. Create login page
2. Create register page
3. Implement disclaimer dialog
4. Add protected route wrapper

### Phase 2: Main Workspace (2-3 hours)
1. Create workspace layout
2. Add header with navigation
3. Add left panel (model explorer)
4. Add right panel (properties)
5. Add status bar

### Phase 3: Core Dialogs (3-4 hours)
1. Project dialog
2. Node dialog
3. Element dialog
4. Material dialog
5. Load dialog
6. Section dialog

### Phase 4: 3D Viewport (4-5 hours)
1. Setup Three.js scene
2. Render nodes as spheres
3. Render elements as lines/cylinders
4. Add camera controls
5. Add selection

### Phase 5: Analysis Features (3-4 hours)
1. Analysis configuration dialog
2. Seismic analysis dialog
3. Wind analysis dialog
4. Results visualization

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 3000
npx kill-port 3000

# Or use different port
npm run dev -- -p 3001
```

### Module Not Found
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### TypeScript Errors
```bash
# Check types
npm run type-check

# Restart TypeScript server in VS Code
Cmd/Ctrl + Shift + P → "TypeScript: Restart TS Server"
```

## 📚 Resources

- [Next.js 15 Docs](https://nextjs.org/docs)
- [React 19 Docs](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [Radix UI](https://www.radix-ui.com)
- [Three.js](https://threejs.org)
- [Zustand](https://zustand-demo.pmnd.rs)
- [React Query](https://tanstack.com/query)

## 🤝 Backend Connection

Make sure the backend is running:

```bash
cd backend
python start.py
```

Backend should be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

## ✨ Features Ready to Use

- ✅ Modern Next.js 15 with App Router
- ✅ React 19 with Server Components
- ✅ TypeScript with strict mode
- ✅ Tailwind CSS with custom theme
- ✅ Radix UI components
- ✅ Zustand state management
- ✅ React Query for data fetching
- ✅ Axios with interceptors
- ✅ Dark mode support
- ✅ Responsive design
- ✅ Type-safe API clients

## 🎉 You're Ready!

The foundation is solid. Now you can:
1. Run `npm run dev`
2. Open http://localhost:3000
3. Start building features!

Happy coding! 🚀
