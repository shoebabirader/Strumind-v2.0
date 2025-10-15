# 📘 StruMind User Guide

## Welcome to StruMind - AI-Powered Structural Analysis Platform

---

## 🚀 Getting Started

### System Requirements
- **Browser**: Chrome, Firefox, Safari, or Edge (latest version)
- **Internet**: Stable connection required
- **Screen**: Minimum 1366x768 resolution recommended

### First Time Setup
1. Open your browser and navigate to StruMind
2. Create an account or sign in
3. You'll land on the professional dashboard

---

## 📊 Dashboard Overview

The dashboard is your command center with:

### Quick Stats
- **Total Nodes**: Number of nodes in your model
- **Elements**: Total structural elements
- **Load Cases**: Defined load combinations
- **Analyses Run**: Completed analysis count

### Recent Analyses
Track your analysis history with status indicators:
- ✅ **Completed** - Analysis finished successfully
- ⏳ **Running** - Analysis in progress
- ⏸️ **Pending** - Queued for execution

### Design Modules
Monitor design status for:
- RC Beam Design
- RC Column Design
- Slab Design
- Foundation Design

---

## 🏗️ Model Builder

### Creating a New Model

1. **Click "Model Builder"** from the sidebar
2. **Add Nodes**:
   - Click on the 3D canvas to place nodes
   - Or use coordinates: X, Y, Z values
   - Snap to grid for precision

3. **Add Elements**:
   - Select two nodes to create a beam/column
   - Choose element type (beam, column, brace)
   - Assign section properties

4. **Define Supports**:
   - Click on nodes to add supports
   - Choose support type:
     - Fixed (all DOF restrained)
     - Pinned (translations restrained)
     - Roller (vertical translation restrained)

5. **Apply Loads**:
   - Point loads on nodes
   - Distributed loads on elements
   - Moments and forces

### 3D Viewer Controls
- **Rotate**: Left-click + drag
- **Pan**: Right-click + drag
- **Zoom**: Mouse wheel
- **Reset View**: Double-click

---

## 🔬 Analysis Module

### Available Analysis Types

#### 1. Static Analysis
- **Purpose**: Calculate displacements and forces under static loads
- **When to Use**: Dead load, live load, static wind/seismic
- **Steps**:
  1. Go to Analysis → Static
  2. Select load cases
  3. Click "Run Analysis"
  4. View results in Results tab

#### 2. Modal Analysis
- **Purpose**: Find natural frequencies and mode shapes
- **When to Use**: Dynamic behavior, vibration studies
- **Parameters**:
  - Number of modes (default: 10)
  - Mass source (dead load factor)

#### 3. Response Spectrum
- **Purpose**: Seismic analysis using response spectrum
- **When to Use**: Earthquake-resistant design
- **Steps**:
  1. Select seismic code (IS 1893, ASCE 7, EC8)
  2. Define spectrum parameters
  3. Choose direction (X, Y, Z)
  4. Run analysis

#### 4. Time-History Analysis
- **Purpose**: Dynamic analysis with time-varying loads
- **When to Use**: Earthquake records, blast loads
- **Parameters**:
  - Time step (0.01s recommended)
  - Damping ratio (5% typical)
  - Load history data

#### 5. Buckling Analysis
- **Purpose**: Find critical buckling loads
- **When to Use**: Slender columns, compression members
- **Output**: Load factors and buckling modes

#### 6. P-Delta Analysis
- **Purpose**: Include geometric nonlinearity
- **When to Use**: Tall buildings, large deformations
- **Note**: Iterative analysis, may take longer

---

## 🎨 Design Module

### RC Design

#### Beam Design
1. Navigate to Design → RC Beam
2. Input parameters:
   - Span length
   - Cross-section (width × depth)
   - Concrete grade (M20, M25, M30, etc.)
   - Steel grade (Fe415, Fe500)
3. Select design code (IS 456, ACI 318, EC2, etc.)
4. Click "Design"
5. Review:
   - Required reinforcement
   - Bar arrangement
   - Shear reinforcement
   - Deflection check

#### Column Design
1. Navigate to Design → RC Column
2. Input:
   - Height
   - Cross-section
   - Axial load
   - Moments (Mx, My)
3. Design outputs:
   - Longitudinal steel
   - Ties/stirrups
   - Interaction diagram
   - Slenderness check

#### Slab Design
1. Navigate to Design → Slab Design
2. Choose slab type:
   - **One-Way Slab**: Ly/Lx > 2
   - **Two-Way Slab**: Ly/Lx ≤ 2
   - **Flat Slab**: No beams
3. Input:
   - Span dimensions
   - Thickness
   - Loads (dead, live)
   - Support conditions
4. Results:
   - Main reinforcement
   - Distribution steel
   - Punching shear check (flat slabs)

#### Shear Wall Design
1. Navigate to Design → Shear Wall
2. Input:
   - Height and length
   - Thickness
   - Axial load, shear, moment
3. Options:
   - Include boundary elements
   - Coupling beams
4. Outputs:
   - Boundary element reinforcement
   - Web reinforcement
   - Shear capacity

### Steel Design

#### Steel Member Design
1. Navigate to Design → Steel Member
2. Select section from database:
   - AISC (W, S, C, L, HSS)
   - Indian (ISMB, ISMC, ISJB)
   - European (IPE, HE, UB, UC)
3. Input loads
4. Design checks:
   - Flexure
   - Shear
   - Deflection
   - Local buckling

#### Steel Connections
1. Navigate to Design → Connections
2. Choose connection type:
   - Bolted
   - Welded
   - Moment connection
   - Shear connection
3. Design outputs:
   - Bolt size and spacing
   - Weld size
   - Plate thickness

### Foundation Design

#### Isolated Footing
1. Navigate to Design → Foundation → Isolated
2. Input:
   - Column loads
   - Soil bearing capacity
   - Footing dimensions
3. Design:
   - Flexural reinforcement
   - Shear check
   - Bearing pressure

#### Combined Footing
- For two or more columns
- Rectangular or trapezoidal shape

#### Mat Foundation
- For entire building
- Includes punching shear checks

---

## 📈 Results Visualization

### Force Diagrams
- **Moment Diagram**: Bending moment along member
- **Shear Diagram**: Shear force distribution
- **Axial Diagram**: Axial force variation

### Deflection
- **Deflection Curve**: Displacement along span
- **Limit Checks**: L/180, L/250, L/360, L/500
- **Status**: Pass/Fail indication

### Stress Analysis
- **Stress Contours**: Color-coded stress distribution
- **Maximum Values**: Peak tensile/compressive stress
- **Utilization Ratio**: Stress/Allowable stress

### Mode Shapes
- **Animated**: View vibration modes
- **Frequencies**: Natural frequencies (Hz)
- **Participation**: Mass participation factors

---

## 🔍 Serviceability Checks

### Deflection Check
1. Navigate to Checks → Deflection
2. Input:
   - Span length
   - Actual deflection
   - Member type
3. Results:
   - Allowable deflection
   - Utilization percentage
   - Pass/Fail status

### Crack Width Check
1. Navigate to Checks → Crack Width
2. Input:
   - Steel stress
   - Cover
   - Bar diameter and spacing
   - Exposure condition
3. Results:
   - Calculated crack width
   - Allowable crack width
   - Recommendations

### Vibration Check
1. Navigate to Checks → Vibration
2. Input:
   - Natural frequency
   - Floor type (office, residential, hospital)
3. Results:
   - Minimum frequency requirement
   - Peak acceleration
   - Comfort criteria

---

## 💾 Import/Export

### Import
- **DXF/DWG**: Import CAD drawings
- **IFC**: Import BIM models
- **Excel**: Import node/element data
- **CSV**: Import tabular data

### Export
- **Results**: Excel, CSV, PDF
- **Reports**: Comprehensive design reports
- **BBS**: Bar bending schedule
- **BOQ**: Bill of quantities
- **3D Model**: IFC, DXF formats

---

## ⚙️ Settings

### Design Codes
Configure default codes for:
- Concrete design
- Steel design
- Seismic analysis
- Wind analysis

### Units
Choose unit system:
- **SI**: kN, m, MPa
- **Imperial**: kip, ft, ksi
- **Custom**: Define your own

### Preferences
- Auto-save interval
- Grid spacing
- Display options
- Color schemes

---

## 🆘 Troubleshooting

### Common Issues

#### Analysis Not Running
- **Check**: All nodes have supports
- **Check**: Load cases are defined
- **Check**: No disconnected elements

#### Design Fails
- **Solution**: Increase member size
- **Solution**: Check material properties
- **Solution**: Verify load combinations

#### Slow Performance
- **Solution**: Reduce mesh density
- **Solution**: Limit number of elements
- **Solution**: Close unused tabs

---

## 📞 Support

### Getting Help
- **Documentation**: This guide
- **Video Tutorials**: Available in Help menu
- **Support Email**: support@strumind.com
- **Community Forum**: forum.strumind.com

### Keyboard Shortcuts
- **Ctrl + N**: New model
- **Ctrl + S**: Save
- **Ctrl + Z**: Undo
- **Ctrl + Y**: Redo
- **Delete**: Delete selected
- **Esc**: Cancel operation

---

## 🎓 Best Practices

### Modeling
1. Start with a simple model
2. Add complexity gradually
3. Use consistent units
4. Name elements logically
5. Group similar elements

### Analysis
1. Run static analysis first
2. Check for warnings
3. Verify reactions sum to loads
4. Review deformed shape
5. Check for unrealistic results

### Design
1. Use appropriate safety factors
2. Follow code requirements
3. Check all limit states
4. Review detailing
5. Generate comprehensive reports

---

## 🚀 Advanced Features

### AI Optimization
- Automatic section optimization
- Cost minimization
- Weight reduction
- ML-based suggestions

### Collaboration
- Real-time multi-user editing
- Comments and annotations
- Version control
- Change tracking

### Automation
- Batch analysis
- Parametric studies
- Template models
- Custom scripts

---

## 📊 Example Workflows

### Simple Beam Design
1. Create model with 2 nodes
2. Add beam element
3. Apply supports (pinned at ends)
4. Add UDL
5. Run static analysis
6. Design beam
7. Generate report

### Multi-Story Building
1. Import floor plan (DXF)
2. Extrude to create 3D model
3. Define load cases (DL, LL, EQ, Wind)
4. Run modal analysis
5. Run response spectrum
6. Design all members
7. Check serviceability
8. Generate BBS and BOQ

---

## 🎉 Tips & Tricks

1. **Use Templates**: Start with pre-built models
2. **Keyboard Shortcuts**: Speed up workflow
3. **Save Often**: Auto-save is your friend
4. **Check Units**: Verify before analysis
5. **Review Results**: Always validate output
6. **Learn Codes**: Understand design requirements
7. **Ask Questions**: Use support resources

---

**Happy Designing! 🏗️**

*StruMind - Empowering Engineers to Build Better Structures*
