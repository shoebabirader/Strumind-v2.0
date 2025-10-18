# Backend API Endpoints Mapping

**Date:** October 16, 2025  
**Purpose:** Complete mapping of backend API endpoints for frontend integration

---

## 🎯 Base URL

```
Development: http://localhost:8000/api
Production: https://api.strumind.com/api
```

---

## 📋 Core Model Building APIs

### 1. Nodes API (`/api/nodes`)

**Endpoints:**
```
POST   /api/nodes/create          # Create new node
GET    /api/nodes/{id}            # Get node by ID
GET    /api/nodes                 # Get all nodes (query: project_id)
PUT    /api/nodes/{id}            # Update node
DELETE /api/nodes/{id}            # Delete node
```

**Request Body (Create):**
```json
{
  "project_id": 1,
  "node_id": "N1",
  "x": 0.0,        // mm
  "y": 0.0,        // mm
  "z": 0.0,        // mm
  "restraints": [true, true, true, false, false, false]  // [ux, uy, uz, rx, ry, rz]
}
```

**Response:**
```json
{
  "id": 1,
  "project_id": 1,
  "node_id": "N1",
  "x": 0.0,
  "y": 0.0,
  "z": 0.0,
  "restraints": [true, true, true, false, false, false]
}
```

---

### 2. Elements API (`/api/elements`)

**Endpoints:**
```
POST   /api/elements/create       # Create new element
GET    /api/elements/{id}         # Get element by ID
GET    /api/elements              # Get all elements (query: project_id)
PUT    /api/elements/{id}         # Update element
DELETE /api/elements/{id}         # Delete element
```

**Request Body (Create):**
```json
{
  "project_id": 1,
  "element_id": "E1",
  "node_i": "N1",
  "node_j": "N2",
  "element_type": "beam",  // beam, column, truss, brace
  "material_id": "M1",
  "section_type": "rectangular",
  "width": 0.3,    // m
  "height": 0.5    // m
}
```

---

### 3. Materials API (`/api/materials`)

**Endpoints:**
```
POST   /api/materials/create      # Create new material
GET    /api/materials/{id}        # Get material by ID
GET    /api/materials             # Get all materials
PUT    /api/materials/{id}        # Update material
DELETE /api/materials/{id}        # Delete material
GET    /api/materials/standard    # Get standard materials (M25, Fe415, etc.)
```

**Request Body (Create):**
```json
{
  "material_id": "M1",
  "name": "M25 Concrete",
  "type": "concrete",  // concrete, steel
  "E": 25000,          // MPa
  "nu": 0.2,           // Poisson's ratio
  "density": 2500,     // kg/m³
  "fc": 25,            // MPa (concrete)
  "fy": null           // MPa (steel)
}
```

---

### 4. Loads API (`/api/loads`)

**Endpoints:**
```
POST   /api/loads/create          # Create new load
GET    /api/loads/{id}            # Get load by ID
GET    /api/loads                 # Get all loads (query: project_id)
PUT    /api/loads/{id}            # Update load
DELETE /api/loads/{id}            # Delete load
```

**Request Body (Create):**
```json
{
  "project_id": 1,
  "load_id": "L1",
  "load_type": "nodal",  // nodal, distributed, point
  "node_id": "N1",       // for nodal loads
  "element_id": null,    // for element loads
  "fx": 0.0,             // kN
  "fy": -100.0,          // kN
  "fz": 0.0,             // kN
  "mx": 0.0,             // kN·m
  "my": 0.0,             // kN·m
  "mz": 0.0              // kN·m
}
```

---

## 🔬 Analysis APIs

### 5. Linear Analysis (`/api/analysis`)

**Endpoints:**
```
POST   /api/analysis/linear       # Run linear static analysis
POST   /api/analysis/modal        # Run modal analysis
POST   /api/analysis/nonlinear    # Run nonlinear analysis
```

**Request Body (Linear):**
```json
{
  "model_id": 1,
  "analysis_type": "static",
  "nodes": [...],
  "elements": [...],
  "loads": [...],
  "restraints": {...},
  "material_props": {...},
  "section_props": {...}
}
```

**Response:**
```json
{
  "success": true,
  "displacements": [
    {"node_id": "N1", "dx": 0.0, "dy": -0.005, "dz": 0.0, "rx": 0.0, "ry": 0.0, "rz": 0.0}
  ],
  "reactions": [
    {"node_id": "N1", "fx": 0.0, "fy": 100.0, "fz": 0.0, "mx": 0.0, "my": 0.0, "mz": 0.0}
  ],
  "element_forces": [
    {
      "element_id": "E1",
      "node_i": {"fx": 0.0, "fy": 50.0, "fz": 0.0, "mx": 0.0, "my": 0.0, "mz": 0.0},
      "node_j": {"fx": 0.0, "fy": 50.0, "fz": 0.0, "mx": 0.0, "my": 0.0, "mz": 0.0}
    }
  ]
}
```

---

### 6. Modal Analysis (`/api/analysis/modal`)

**Request Body:**
```json
{
  "model_id": 1,
  "num_modes": 10,
  "nodes": [...],
  "elements": [...],
  "material_props": {...}
}
```

**Response:**
```json
{
  "success": true,
  "frequencies": [2.5, 5.3, 8.1, ...],  // Hz
  "periods": [0.4, 0.19, 0.12, ...],    // seconds
  "mode_shapes": [[...], [...], ...],
  "participation_factors": [0.85, 0.12, 0.03, ...]
}
```

---

### 7. P-Delta Analysis (`/api/pdelta`)

**Endpoints:**
```
POST   /api/pdelta/analyze        # Run P-Delta analysis
```

**Request Body:**
```json
{
  "model_id": 1,
  "max_iterations": 50,
  "tolerance": 1e-6,
  "include_geometric": true,
  "nodes": [...],
  "elements": [...],
  "loads": [...]
}
```

---

### 8. Pushover Analysis (`/api/pushover`)

**Endpoints:**
```
POST   /api/pushover/analyze      # Run pushover analysis
```

**Request Body:**
```json
{
  "model_id": 1,
  "control_node": "N10",
  "load_pattern": {...},
  "target_displacement": 0.1,  // m
  "num_steps": 100
}
```

**Response:**
```json
{
  "success": true,
  "displacements": [0.0, 0.001, 0.002, ...],  // m
  "base_shear": [0.0, 100.0, 195.0, ...],     // kN
  "performance_point": {
    "displacement": 0.05,
    "base_shear": 850.0
  },
  "hinge_states": {...}
}
```

---

## 🌊 Seismic & Wind APIs

### 9. Seismic Analysis (`/api/seismic`)

**Endpoints:**
```
POST   /api/seismic/calculate     # Calculate seismic forces
POST   /api/seismic/response-spectrum  # Response spectrum analysis
```

**Request Body:**
```json
{
  "model_id": 1,
  "code": "IS1893",  // IS1893, ASCE7
  "zone": "IV",
  "importance_factor": 1.5,
  "soil_type": "II",
  "damping_ratio": 0.05,
  "response_reduction_factor": 5.0
}
```

**Response:**
```json
{
  "success": true,
  "base_shear": 1250.0,  // kN
  "design_spectrum": [...],
  "modal_responses": [...],
  "story_forces": [...]
}
```

---

### 10. Wind Analysis (`/api/wind`)

**Endpoints:**
```
POST   /api/wind/calculate        # Calculate wind forces
```

**Request Body:**
```json
{
  "model_id": 1,
  "code": "IS875",  // IS875, ASCE7
  "basic_wind_speed": 47.0,  // m/s
  "terrain_category": 2,
  "structure_class": "B",
  "height": 30.0,  // m
  "width": 20.0,   // m
  "depth": 15.0    // m
}
```

---

## 🏗️ Design APIs

### 11. Concrete Design (`/api/design/concrete`)

**Endpoints:**
```
POST   /api/design/concrete/beam       # Design concrete beam
POST   /api/design/concrete/column     # Design concrete column
POST   /api/design/concrete/slab       # Design concrete slab
```

**Request Body (Beam):**
```json
{
  "code": "IS456",
  "element_id": "E1",
  "moment": 150.0,    // kN·m
  "shear": 80.0,      // kN
  "width": 300,       // mm
  "depth": 500,       // mm
  "concrete_grade": "M25",
  "steel_grade": "Fe415"
}
```

**Response:**
```json
{
  "success": true,
  "flexure_check": "PASS",
  "shear_check": "PASS",
  "main_steel": {
    "area_required": 1200,  // mm²
    "bars": "4-20φ",
    "area_provided": 1256   // mm²
  },
  "shear_steel": {
    "spacing": 150,  // mm
    "bars": "8φ @ 150 c/c"
  },
  "utilization_ratio": 0.85
}
```

---

### 12. Steel Design (`/api/design/steel`)

**Endpoints:**
```
POST   /api/design/steel/beam         # Design steel beam
POST   /api/design/steel/column       # Design steel column
POST   /api/design/steel/connection   # Design steel connection
```

---

### 13. Foundation Design (`/api/foundation`)

**Endpoints:**
```
POST   /api/foundation/isolated       # Design isolated footing
POST   /api/foundation/combined       # Design combined footing
POST   /api/foundation/raft           # Design raft foundation
POST   /api/foundation/pile           # Design pile foundation
```

---

## 📊 Results & Reporting APIs

### 14. Reporting (`/api/reporting`)

**Endpoints:**
```
POST   /api/reporting/generate        # Generate analysis report
GET    /api/reporting/{report_id}     # Get report
GET    /api/reporting/download/{id}   # Download PDF report
```

---

## 🔄 Project Management APIs

### 15. Projects (`/api/projects`)

**Endpoints:**
```
POST   /api/projects/create           # Create new project
GET    /api/projects/{id}             # Get project
GET    /api/projects                  # List all projects
PUT    /api/projects/{id}             # Update project
DELETE /api/projects/{id}             # Delete project
```

---

### 16. Versioning (`/api/versioning`)

**Endpoints:**
```
POST   /api/versioning/save           # Save version
GET    /api/versioning/{project_id}   # Get versions
POST   /api/versioning/restore        # Restore version
```

---

## 🔌 Real-time APIs

### 17. WebSocket (`/ws`)

**Connection:**
```
ws://localhost:8000/ws/{client_id}
```

**Messages:**
```json
{
  "type": "analysis_progress",
  "data": {
    "progress": 45,
    "message": "Assembling stiffness matrix..."
  }
}
```

---

## 🎨 Advanced Features APIs

### 18. BIM Integration (`/api/bim`)

**Endpoints:**
```
POST   /api/bim/import/ifc            # Import IFC file
POST   /api/bim/export/ifc            # Export to IFC
```

---

### 19. ML Features (`/api/ml`)

**Endpoints:**
```
POST   /api/ml/auto-model             # Auto-generate model
POST   /api/ml/optimize               # Optimize design
POST   /api/ml/predict                # Predict behavior
```

---

### 20. Templates (`/api/templates`)

**Endpoints:**
```
GET    /api/templates                 # List templates
POST   /api/templates/apply           # Apply template
POST   /api/templates/save            # Save as template
```

---

## 📝 Summary

### Total Endpoints: 60+

**Core APIs (Essential):**
- Nodes: 5 endpoints
- Elements: 5 endpoints
- Materials: 6 endpoints
- Loads: 5 endpoints
- Analysis: 3 endpoints

**Advanced APIs:**
- Seismic: 2 endpoints
- Wind: 1 endpoint
- Design: 10+ endpoints
- Foundation: 4 endpoints
- Reporting: 3 endpoints

**Supporting APIs:**
- Projects: 5 endpoints
- Versioning: 3 endpoints
- WebSocket: 1 connection
- BIM: 2 endpoints
- ML: 3 endpoints
- Templates: 3 endpoints

---

## 🔗 Frontend Integration Priority

### Phase 1 (MVP):
1. ✅ Nodes API
2. ✅ Elements API
3. ✅ Materials API
4. ✅ Loads API
5. ✅ Linear Analysis API

### Phase 2:
6. Modal Analysis
7. P-Delta Analysis
8. Pushover Analysis
9. Seismic Analysis
10. Wind Analysis

### Phase 3:
11. Design APIs
12. Foundation Design
13. Reporting
14. Projects Management

### Phase 4:
15. BIM Integration
16. ML Features
17. Templates
18. Collaboration

---

**Date:** October 16, 2025  
**Status:** ✅ **Complete API Mapping for Frontend Integration**
