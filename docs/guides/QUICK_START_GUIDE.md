# 🚀 Quick Start Guide - StruMind Pro

## Get Started in 5 Minutes!

---

## 📋 **Prerequisites**

- Node.js 16+ installed
- Python 3.8+ installed
- Backend running on `http://localhost:8000`
- Frontend running on `http://localhost:3000`

---

## 🏃 **Quick Start**

### **Step 1: Start Backend**
```bash
cd backend
python main.py
```

### **Step 2: Start Frontend**
```bash
cd frontend
npm run dev
```

### **Step 3: Login**
- Open `http://localhost:3000/login`
- Username: `demo`
- Password: `demo123`

---

## 🎯 **Basic Workflow**

### **1. Create a Simple Frame (5 steps)**

#### **Step 1: Add Nodes**
```
Click 📦 icon → Add Node Dialog
- Node N1: (0, 0, 0) - Fixed support (check all restraints)
- Node N2: (5, 0, 0) - No restraints
- Node N3: (5, 3, 0) - No restraints
- Node N4: (0, 3, 0) - Fixed support (check all restraints)
```

#### **Step 2: Add Material**
```
Click 📐 icon → Material Library
- Select "Concrete M25" or "Steel Fe415"
- Click to add to project
```

#### **Step 3: Add Elements**
```
Click ➕ icon → Add Element Dialog
- Element E1: Beam, N1→N2, Material: M25, Section: 0.3×0.5
- Element E2: Column, N2→N3, Material: M25, Section: 0.3×0.3
- Element E3: Beam, N3→N4, Material: M25, Section: 0.3×0.5
- Element E4: Column, N4→N1, Material: M25, Section: 0.3×0.3
```

#### **Step 4: Add Loads**
```
Click ⚡ icon → Load Dialog
- Nodal Load on N2: FY = -50 kN (Dead Load)
- Nodal Load on N3: FY = -50 kN (Dead Load)
```

#### **Step 5: Run Analysis**
```
Click ▶️ icon → Analysis Dialog
- Analysis Type: Static Linear
- Solver: Direct (Skyline)
- Load Combination: 1.4DL
- Click "Run Analysis"
```

---

## 📊 **View Results**

### **Switch to Results Tab**
```
Right Panel → Click "Results" tab
- View Displacements
- View Forces
- View Stresses
```

### **View Tables**
```
Right Panel → Click "Tables" tab
- Nodes Tab: See all nodes
- Elements Tab: See all elements
```

---

## 🎨 **Toolbar Quick Reference**

| Icon | Function | Shortcut |
|------|----------|----------|
| 💾 | Save | Ctrl+S |
| 📁 | Open/New Project | Ctrl+O |
| 📋 | Copy | Ctrl+C |
| 🗑️ | Delete | Del |
| 📦 | Add Node | N |
| ➕ | Add Element | E |
| 📐 | Materials | M |
| ⚡ | Loads | L |
| ▦ | Grid | G |
| 📊 | Tables | T |
| 🔍+ | Zoom In | + |
| 🔍- | Zoom Out | - |
| ↻ | Reset View | R |
| ▶️ | Run Analysis | F5 |

---

## 🎮 **Keyboard Shortcuts**

### **Navigation**
- `Space` - Pan mode
- `Scroll` - Zoom
- `Middle Mouse` - Rotate view

### **Selection**
- `Click` - Select item
- `Ctrl+Click` - Multi-select
- `Ctrl+A` - Select all
- `Esc` - Clear selection

### **Editing**
- `Delete` - Delete selected
- `Ctrl+D` - Duplicate
- `Ctrl+Z` - Undo
- `Ctrl+Y` - Redo

---

## 📋 **Common Tasks**

### **Add Multiple Nodes Quickly**
```
1. Click 📦 icon
2. Enter node data
3. Click "Add Node"
4. Dialog stays open
5. Enter next node
6. Repeat
7. Click "Cancel" when done
```

### **Copy Element Properties**
```
1. Select element in table
2. Click Edit (✏️)
3. Change ID and nodes
4. Click "Add Element"
```

### **Change Units**
```
Secondary Toolbar → Units dropdown → Select unit system
```

### **Change View**
```
Secondary Toolbar → View buttons
- 3D: Isometric view
- XY: Plan view
- XZ: Elevation view
- YZ: Side view
```

---

## 🎯 **Example Projects**

### **Simple Beam**
```
Nodes:
- N1: (0, 0, 0) - Fixed
- N2: (5, 0, 0) - Free

Elements:
- E1: Beam, N1→N2, M25, 0.3×0.5

Loads:
- N2: FY = -50 kN

Analysis: Static Linear
```

### **Portal Frame**
```
Nodes:
- N1: (0, 0, 0) - Fixed
- N2: (0, 3, 0) - Free
- N3: (5, 3, 0) - Free
- N4: (5, 0, 0) - Fixed

Elements:
- E1: Column, N1→N2, M25, 0.3×0.3
- E2: Beam, N2→N3, M25, 0.3×0.5
- E3: Column, N3→N4, M25, 0.3×0.3

Loads:
- E2: Uniform, -10 kN/m (Dead Load)

Analysis: Static Linear
```

### **Simple Truss**
```
Nodes:
- N1: (0, 0, 0) - Fixed
- N2: (2, 2, 0) - Free
- N3: (4, 0, 0) - Pinned (UX, UY)

Elements:
- E1: Truss, N1→N2, Fe415, 0.05×0.05
- E2: Truss, N2→N3, Fe415, 0.05×0.05
- E3: Truss, N1→N3, Fe415, 0.05×0.05

Loads:
- N2: FY = -100 kN

Analysis: Static Linear
```

---

## 🔧 **Troubleshooting**

### **Dialog Not Opening?**
- Check browser console for errors
- Refresh page (F5)
- Clear browser cache

### **Data Not Saving?**
- Check backend is running
- Check network tab for API errors
- Verify authentication token

### **Analysis Not Running?**
- Ensure nodes are defined
- Ensure elements are defined
- Ensure loads are defined
- Check analysis configuration

### **Results Not Showing?**
- Switch to Results tab
- Check analysis completed successfully
- Refresh results panel

---

## 💡 **Tips & Tricks**

### **Productivity Tips**
1. Use keyboard shortcuts for faster workflow
2. Keep dialogs open for batch input
3. Use tables for quick editing
4. Use search in material library
5. Save frequently

### **Best Practices**
1. Name nodes and elements systematically (N1, N2, E1, E2)
2. Define materials before elements
3. Check restraints carefully
4. Use appropriate load combinations
5. Verify results make sense

### **Common Mistakes to Avoid**
1. ❌ Forgetting to add restraints (structure will be unstable)
2. ❌ Using wrong units
3. ❌ Not selecting material for elements
4. ❌ Connecting elements to non-existent nodes
5. ❌ Running analysis without loads

---

## 📚 **Learn More**

### **Documentation**
- `COMPLETE_COMPONENTS_SUMMARY.md` - All components
- `VISUAL_COMPONENTS_GUIDE.md` - UI guide
- `FINAL_STATUS_REPORT.md` - Status report

### **Support**
- Check browser console for errors
- Review network tab for API issues
- Check backend logs

---

## 🎉 **You're Ready!**

You now know how to:
- ✅ Add nodes and elements
- ✅ Define materials and loads
- ✅ Run analysis
- ✅ View results
- ✅ Use all dialogs and tables

**Start building your first structure!** 🏗️

---

**Happy Analyzing! 🚀**
