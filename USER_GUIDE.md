# StruMind User Guide

## Getting Started

### Creating Your First Model

#### Step 1: Start a New Project
1. Open StruMind at `http://localhost:3000`
2. Click "New Project" or select from existing projects
3. Choose a quick start template or start blank

#### Step 2: Model Builder - Nodes Tab

**Adding Nodes:**
```
Click "+ Add Node" button
Enter coordinates:
- X: 0 mm (horizontal)
- Y: 0 mm (vertical)
- Z: 0 mm (depth)

Define Restraints:
☑ Ux - Restrain X translation
☑ Uy - Restrain Y translation
☑ Uz - Restrain Z translation
☑ Rx - Restrain X rotation
☑ Ry - Restrain Y rotation
☑ Rz - Restrain Z rotation
```

**Example: Simple Portal Frame**
```
Node 1: (0, 0, 0) - Fixed support [All restraints checked]
Node 2: (0, 3000, 0) - Free [No restraints]
Node 3: (5000, 3000, 0) - Free [No restraints]
Node 4: (5000, 0, 0) - Fixed support [All restraints checked]
```

#### Step 3: Model Builder - Elements Tab

**Creating Elements:**
1. Go to Nodes tab and select nodes by checking boxes
2. Switch to Elements tab
3. Click "+ Add Element"
4. Select element type: Beam, Column, Truss, Slab, or Shell
5. Assign material from dropdown
6. Assign section from dropdown

**Example: Portal Frame Elements**
```
Element 1: Column
- Nodes: 1, 2
- Material: Concrete M25
- Section: 300x300

Element 2: Beam
- Nodes: 2, 3
- Material: Concrete M25
- Section: 300x450

Element 3: Column
- Nodes: 3, 4
- Material: Concrete M25
- Section: 300x300
```

#### Step 4: Model Builder - Materials Tab

**Pre-defined Materials:**
- Concrete M25 (E = 25 GPa, ν = 0.2, ρ = 2500 kg/m³)
- Steel Fe415 (E = 200 GPa, ν = 0.3, ρ = 7850 kg/m³)

**Adding Custom Material:**
1. Click "+ Add Material"
2. Enter properties:
   - Name: "Concrete M30"
   - Young's Modulus: 27e9 Pa
   - Poisson's Ratio: 0.2
   - Density: 2500 kg/m³
   - Grade: M30

#### Step 5: Model Builder - Sections Tab

**Pre-defined Sections:**
- 300x450 (Rectangular beam)
- 300x300 (Square column)

**Adding Custom Section:**
1. Click "+ Add Section"
2. Select type: Rectangular, Circular, I-section, Custom
3. Enter dimensions:
   - Width: 400 mm
   - Depth: 600 mm

#### Step 6: Loads Tab

**Adding Loads:**
1. Click "+ Add Load"
2. Select load type:
   - Point Load (applied at nodes)
   - Distributed Load (applied on elements)
   - Moment (applied at nodes)
3. Enter node/element number
4. Select direction: X, Y, Z, MX, MY, MZ
5. Enter magnitude in kN or kNm
6. Select load case

**Example: Dead Load on Beam**
```
Type: Distributed Load
Element: 2
Direction: Y (downward)
Magnitude: -10 kN/m
Load Case: Dead Load
```

**Creating Load Cases:**
1. Click "+ Add Load Case"
2. Enter name: "Wind Load X"
3. Add loads for this case

#### Step 7: Analysis Tab

**Running Analysis:**
1. Switch to Analysis tab
2. Select analysis type:
   - Static Analysis (forces and displacements)
   - Modal Analysis (natural frequencies)
   - Pushover Analysis (capacity curve)
   - Time-History Analysis (seismic response)
3. Click "Run Analysis"
4. View results in 3D viewer or tables

**Analysis Results Include:**
- Node displacements (Ux, Uy, Uz, Rx, Ry, Rz)
- Element forces (Axial, Shear, Moment)
- Support reactions
- Natural frequencies (modal analysis)

#### Step 8: Design Tab

**Generating Design:**
1. Switch to Design tab
2. Select design code:
   - IS 456 (Indian RC)
   - ACI 318 (American RC)
   - IS 800 (Indian Steel)
   - AISC (American Steel)
3. Click "Generate Design"
4. Review design output:
   - Required reinforcement
   - Section adequacy checks
   - Code compliance status

**AI Optimization:**
1. Click "AI Optimize"
2. AI suggests optimal sections and reinforcement
3. Review suggestions with confidence scores
4. Accept or modify recommendations

#### Step 9: Detailing Tab

**Generating Drawings:**
1. Switch to Detailing tab
2. Click "Generate Drawings"
3. Select output format: DXF, PDF, or IFC

**Bar Bending Schedule (BBS):**
1. Click "Export BBS"
2. View table with:
   - Bar mark
   - Diameter
   - Length
   - Quantity
   - Shape code

**Bill of Quantities (BOQ):**
1. Click "Generate BOQ"
2. View quantities:
   - Concrete volume (m³)
   - Steel weight (kg)
   - Formwork area (m²)
   - Estimated cost

#### Step 10: BIM Integration

**Exporting to IFC:**
1. Switch to BIM tab
2. Click "Export to IFC"
3. Download IFC file
4. Import into Revit/Tekla/ArchiCAD

**Importing from IFC:**
1. Click "Import IFC"
2. Select IFC file from BIM software
3. Model automatically created with all properties

**3D Visualization:**
1. Switch to Model tab
2. Click "3D Viewer" button
3. Use mouse to:
   - Left click + drag: Rotate
   - Right click + drag: Pan
   - Scroll: Zoom
4. View stress contours and deformations

## Using Quick Templates

### Simple Frame Template
- 2D portal frame
- 2 columns (3m height)
- 1 beam (5m span)
- Fixed supports at base
- Ready for load application

### Building Frame Template
- 3D multi-story building
- 3 stories (3m each)
- 2x2 bays (5m x 5m)
- 36 nodes, 27 columns
- Ready for analysis

### Truss Template
- 2D truss structure
- 3 nodes forming triangle
- Steel members
- Suitable for roof trusses

### Grid Floor Template
- 4x4 grid of beams
- 16 nodes
- Orthogonal beam layout
- Typical floor system

### Bridge Template
- Simple bridge span
- 3 nodes (20m total span)
- Large beam sections
- Fixed supports at ends

## AI Assistant Usage

### Getting Design Suggestions
```
User: "Suggest section for 5m beam with 50 kNm moment"
AI: {
  "section": "300x450mm",
  "reinforcement": "4-20mm + 8mm @ 150mm",
  "confidence": 0.92
}
```

### Error Checking
```
User: "Check my model for errors"
AI: Detects:
- Duplicate nodes at (0, 0, 0)
- Zero-length element #5
- Load magnitude unusually high
```

### Auto-Modeling
```
User: "Create a 3-story building frame"
AI: Generates complete geometry with:
- Nodes at grid intersections
- Columns and beams
- Typical sections assigned
```

## Keyboard Shortcuts (Planned)

- `Ctrl + N` - New project
- `Ctrl + S` - Save model
- `Ctrl + O` - Open project
- `Delete` - Delete selected items
- `Ctrl + Z` - Undo
- `Ctrl + Y` - Redo
- `Space` - Toggle 3D viewer

## Tips & Best Practices

### Modeling
1. **Start with templates** for common structures
2. **Define restraints carefully** - fixed vs pinned
3. **Use consistent units** - mm for geometry, kN for loads
4. **Check node connectivity** before analysis
5. **Name load cases clearly** for organization

### Analysis
1. **Run static analysis first** to check basic behavior
2. **Verify support reactions** sum to applied loads
3. **Check for warnings** about singular matrices
4. **Use modal analysis** to understand dynamic behavior
5. **Review deformed shape** for reasonableness

### Design
1. **Select appropriate code** for your region
2. **Review AI suggestions** before accepting
3. **Check all limit states** (flexure, shear, deflection)
4. **Optimize iteratively** for cost savings
5. **Document design decisions** in comments

### Collaboration
1. **Use comments** to communicate with team
2. **Save frequently** to avoid data loss
3. **Export regularly** for backup
4. **Review change history** before major edits
5. **Test in staging** before production use

## Troubleshooting

### Model Won't Analyze
- Check for disconnected nodes
- Verify all elements have materials/sections
- Ensure at least one restraint exists
- Check for zero-length elements

### Design Fails
- Verify analysis completed successfully
- Check if forces exceed section capacity
- Review code-specific requirements
- Try AI optimization for suggestions

### Export Issues
- Ensure model is saved first
- Check file permissions
- Verify export format compatibility
- Try different export format

### Performance Issues
- Reduce number of elements for large models
- Close unused tabs
- Clear browser cache
- Use Chrome/Edge for best performance

## Support

- Documentation: See FEATURES.md for complete feature list
- API Docs: http://localhost:8000/docs
- Issues: GitHub Issues
- Email: support@strumind.com (example)

## Video Tutorials (Coming Soon)

1. Getting Started - First Model
2. Advanced Modeling Techniques
3. Load Application Best Practices
4. Analysis and Results Interpretation
5. Design Code Compliance
6. BIM Integration Workflow
7. AI Assistant Features
8. Collaboration and Sharing
