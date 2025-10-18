# 🎨 UI Redesign Plan - Professional Structural Engineering Interface

## 🎯 Goal
Transform the current modern web UI into a professional desktop-style structural engineering interface similar to ETABS/STAAD Pro/Tekla.

## 📊 Key Changes Required

### 1. Layout Structure
**Current**: Modern web app with sidebar
**New**: Classic desktop application layout

```
┌─────────────────────────────────────────────────────────────┐
│ Menu Bar: File | Edit | View | Define | Draw | Select | ... │
├─────────────────────────────────────────────────────────────┤
│ Toolbar: [Icons for common actions]                         │
├──────────┬──────────────────────────────────┬───────────────┤
│          │                                  │               │
│  Model   │        3D Viewport               │  Properties   │
│ Explorer │                                  │    Panel      │
│  (Tree)  │                                  │               │
│          │                                  │  Data Tables  │
│          │                                  │               │
├──────────┴──────────────────────────────────┴───────────────┤
│ Status Bar: Load: 1.5W | Input Units: kip-ft | ...         │
└─────────────────────────────────────────────────────────────┘
```

### 2. Color Scheme
**Current**: Modern dark/light with colors
**New**: Professional gray/blue engineering software style

- Background: Light gray (#F0F0F0)
- Panels: White/Light gray
- Accents: Blue (#0078D4)
- Text: Dark gray (#333333)
- Borders: Medium gray (#CCCCCC)

### 3. Components to Create

#### Left Panel - Model Explorer (Tree View)
- Model
  - Project
  - Structure Layout
  - Properties
    - Materials
    - Frame Sections
    - Slab Sections
    - Wall Sections
  - Groups
  - Loads
  - Named Output Items

#### Top Menu Bar
- File
- Edit
- View
- Define
- Draw
- Select
- Assign
- Analyze
- Display
- Design
- Options
- Tools
- Help

#### Top Toolbar
- New, Open, Save icons
- Undo/Redo
- View controls (Zoom, Pan, Rotate)
- Selection tools
- Drawing tools
- Analysis/Design buttons

#### Right Panel - Properties & Tables
- Properties panel (top)
- Data tables (bottom)
  - Nodes table
  - Elements table
  - Results table

#### Bottom Status Bar
- Current load case
- Input units
- Selection info
- Coordinates

### 4. Dialogs Style
**Current**: Modern rounded dialogs
**New**: Classic rectangular dialogs with tabs

- Rectangular borders
- Tab-based navigation
- OK/Cancel/Apply buttons at bottom
- Professional form layouts

## 📁 Files to Create/Modify

### New Components:
1. `MenuBar.tsx` - Top menu bar
2. `Toolbar.tsx` - Icon toolbar
3. `ModelExplorer.tsx` - Left tree view
4. `PropertiesPanel.tsx` - Right properties
5. `DataTables.tsx` - Right data tables
6. `StatusBar.tsx` - Bottom status
7. `ClassicDialog.tsx` - Professional dialog wrapper

### Modified Components:
1. `workspace/page.tsx` - New layout
2. All dialog files - Classic style
3. `globals.css` - Professional color scheme

## 🎨 Design Tokens

```css
/* Professional Engineering Software Theme */
--bg-primary: #F0F0F0;
--bg-secondary: #FFFFFF;
--bg-panel: #E8E8E8;
--border-color: #CCCCCC;
--text-primary: #333333;
--text-secondary: #666666;
--accent-blue: #0078D4;
--accent-hover: #005A9E;
--toolbar-bg: #F5F5F5;
--menu-bg: #FAFAFA;
```

## 🚀 Implementation Steps

### Phase 1: Core Layout (Priority 1)
1. Create MenuBar component
2. Create Toolbar component
3. Create ModelExplorer tree
4. Update workspace layout
5. Create StatusBar

### Phase 2: Panels (Priority 2)
1. Create PropertiesPanel
2. Create DataTables
3. Integrate with 3D viewport

### Phase 3: Dialogs (Priority 3)
1. Create ClassicDialog wrapper
2. Update all 45 dialogs to classic style
3. Add tab navigation to complex dialogs

### Phase 4: Polish (Priority 4)
1. Add icons to toolbar
2. Add context menus
3. Add keyboard shortcuts
4. Professional styling touches

## 📦 Additional Dependencies Needed

```bash
npm install @radix-ui/react-menubar
npm install @radix-ui/react-context-menu
npm install @radix-ui/react-tree
npm install react-resizable-panels
```

## ⏱️ Estimated Time
- Phase 1: 2-3 hours
- Phase 2: 1-2 hours
- Phase 3: 3-4 hours
- Phase 4: 1-2 hours
**Total**: 7-11 hours of development

## 🎯 Success Criteria
- ✅ Looks like professional engineering software
- ✅ Tree-based navigation on left
- ✅ Classic menu bar and toolbar
- ✅ Professional gray color scheme
- ✅ All 45 dialogs accessible
- ✅ Data tables for viewing results
- ✅ Professional status bar

---

**Ready to implement?** This will be a complete UI transformation!
