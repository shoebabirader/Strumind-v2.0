# 🚀 Frontend Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

This will install all required packages including:
- **Radix UI Components** - Accessible UI primitives
- **class-variance-authority** - CSS variant management
- **clsx** - Conditional classnames
- **tailwind-merge** - Tailwind class merging
- **lucide-react** - Icon library
- **recharts** - Chart library
- **Three.js** - 3D visualization

### 2. Run Development Server

```bash
npm run dev
```

The frontend will be available at: http://localhost:3000

### 3. Build for Production

```bash
npm run build
npm start
```

---

## 📦 Dependencies Added

### UI Components (Radix UI):
- `@radix-ui/react-dialog` - Modal dialogs
- `@radix-ui/react-dropdown-menu` - Dropdown menus
- `@radix-ui/react-label` - Form labels
- `@radix-ui/react-progress` - Progress bars
- `@radix-ui/react-select` - Select dropdowns
- `@radix-ui/react-slot` - Slot component
- `@radix-ui/react-tabs` - Tabbed interfaces

### Styling:
- `class-variance-authority` - CSS variants
- `clsx` - Conditional classes
- `tailwind-merge` - Merge Tailwind classes

### Icons & Charts:
- `lucide-react` - Icon library
- `recharts` - Chart components

### 3D Visualization:
- `@react-three/fiber` - React Three.js
- `@react-three/drei` - Three.js helpers
- `three` - Three.js library

---

## 🎨 UI Components Available

### Dialogs (27 total):
1. NodeDialog
2. ElementDialog
3. MaterialDialog
4. LoadDialog
5. AnalysisDialog
6. DesignDialog
7. DetailingDialog
8. AIAssistantDialog
9. ReportDialog
10. AdvancedAnalysisDialog
11. SpecializedDesignDialog
12. VersionDialog
13. CollaborationDialog
14. BIMDialog
15. SeismicDialog
16. WindDialog
17. NewProjectDialog
18. FoundationDialog ✨
19. ConnectionsDialog ✨
20. ServiceabilityDialog ✨
21. PushoverDialog ✨
22. SectionLibraryDialog ✨
23. TemplatesDialog ✨
24. ParallelAnalysisDialog ✨
25. CacheManagementDialog ✨
26. PluginsDialog ✨
27. GenerativeDialog ✨

### Base UI Components:
- Button (with variants)
- Input
- Label
- Dialog
- Tabs
- Select
- Textarea
- Badge
- Progress
- DropdownMenu
- Toast notifications

---

## 🔧 Troubleshooting

### Issue: Module not found errors

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Issue: TypeScript errors

**Solution:**
```bash
npm run build
```
This will show any TypeScript errors that need fixing.

### Issue: Tailwind classes not working

**Solution:**
Check that `tailwind.config.js` and `postcss.config.js` are properly configured.

---

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── dialogs/          # 27 dialog components
│   │   ├── ui/               # Base UI components
│   │   ├── workspace/        # Workspace components
│   │   └── tables/           # Data tables
│   ├── contexts/             # React contexts
│   ├── lib/                  # Utilities
│   ├── pages/                # Next.js pages
│   └── styles/               # Global styles
├── public/                   # Static assets
└── package.json              # Dependencies
```

---

## ✅ Verification

After installation, verify everything works:

```bash
# 1. Check dependencies
npm list

# 2. Run dev server
npm run dev

# 3. Open browser
# Navigate to http://localhost:3000

# 4. Check for errors in console
# Should see no module not found errors
```

---

## 🎉 Success Criteria

✅ All dependencies installed  
✅ No module not found errors  
✅ Dev server starts successfully  
✅ All dialogs render without errors  
✅ UI components work properly  
✅ Icons display correctly  
✅ Charts render properly  

---

**Status:** ✅ **READY TO RUN**  
**Next:** Run `npm install` in the frontend directory
