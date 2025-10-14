# 🚀 API Reference - New Features

## Quick Reference Guide for All New Endpoints

---

## 1. Advanced Analysis API

**Base URL:** `/api/advanced-analysis`

### Time-History Analysis
```http
POST /api/advanced-analysis/time-history
Content-Type: application/json

{
  "mass_matrix": [[...]],
  "stiffness_matrix": [[...]],
  "damping_matrix": [[...]],
  "force_history": [[...]],
  "time_step": 0.01,
  "damping_ratio": 0.05
}
```

### Buckling Analysis
```http
POST /api/advanced-analysis/buckling
Content-Type: application/json

{
  "stiffness_matrix": [[...]],
  "geometric_stiffness_matrix": [[...]],
  "n_modes": 10
}
```

### Load Combinations
```http
POST /api/advanced-analysis/load-combinations
Content-Type: application/json

{
  "load_cases": {
    "DL": 1.0,
    "LL": 1.0,
    "EQX": 1.0
  },
  "code": "IS875"
}
```

### Envelope Results
```http
POST /api/advanced-analysis/envelope
Content-Type: application/json

{
  "combination_results": {
    "Combo1": [1.0, 2.0, 3.0],
    "Combo2": [1.5, 2.5, 3.5]
  }
}
```

### Steel Sections Database
```http
GET /api/advanced-analysis/steel-sections/{standard}?section_type=W

# Examples:
GET /api/advanced-analysis/steel-sections/AISC?section_type=W
GET /api/advanced-analysis/steel-sections/IS?section_type=ISMB
GET /api/advanced-analysis/steel-sections/EU?section_type=IPE
```

### Slab Design
```http
POST /api/advanced-analysis/slab-design
Content-Type: application/json

{
  "slab_type": "two_way",
  "span_x": 5000,
  "span_y": 6000,
  "thickness": 150,
  "loads": {
    "dead": 2.0,
    "live": 3.0
  },
  "support_condition": "all_edges_supported"
}
```

### Results Visualization
```http
POST /api/advanced-analysis/results/moment-diagram
POST /api/advanced-analysis/results/shear-diagram
POST /api/advanced-analysis/results/deflection-curve

Content-Type: application/json
{
  "element_id": "E1",
  "result_type": "moment",
  "stations": [0, 0.25, 0.5, 0.75, 1.0],
  "values": [0, 50, 75, 50, 0],
  "span": 6000
}
```

---

## 2. Specialized Design API

**Base URL:** `/api/specialized-design`

### Shear Wall Design
```http
POST /api/specialized-design/shear-wall
Content-Type: application/json

{
  "height": 12000,
  "length": 4000,
  "thickness": 250,
  "axial_load": 2000,
  "shear_force": 500,
  "moment": 3000,
  "boundary_element": true
}
```

### Coupling Beam Design
```http
POST /api/specialized-design/coupling-beam
Content-Type: application/json

{
  "span": 2000,
  "depth": 600,
  "width": 300,
  "shear_force": 300,
  "moment": 200
}
```

### Retaining Wall Design
```http
POST /api/specialized-design/retaining-wall
Content-Type: application/json

{
  "wall_type": "cantilever",
  "height": 4000,
  "stem_thickness_top": 200,
  "stem_thickness_bottom": 300,
  "base_width": 2500,
  "base_thickness": 400,
  "toe_length": 800,
  "surcharge": 10
}
```

### Staircase Design
```http
POST /api/specialized-design/staircase
Content-Type: application/json

{
  "stair_type": "dog_legged",
  "flight_length": 3000,
  "flight_width": 1200,
  "waist_thickness": 150,
  "riser": 150,
  "tread": 300,
  "loads": {
    "dead": 1.0,
    "live": 3.0
  }
}
```

### Composite Beam Design
```http
POST /api/specialized-design/composite-beam
Content-Type: application/json

{
  "span": 8000,
  "steel_section": {
    "depth": 500,
    "width": 200,
    "area": 8000,
    "Ixx": 200000000
  },
  "slab_thickness": 120,
  "slab_width": 2000,
  "loads": {
    "dead": 5.0,
    "live": 4.0
  },
  "shear_connectors": "stud"
}
```

### Composite Column Design
```http
POST /api/specialized-design/composite-column
Content-Type: application/json

{
  "height": 4000,
  "steel_section": {
    "area": 8000,
    "Ixx": 200000000
  },
  "concrete_dimensions": {
    "width": 400,
    "depth": 400
  },
  "axial_load": 2000,
  "moment": 150
}
```

### Moving Load Analysis
```http
POST /api/specialized-design/moving-load
Content-Type: application/json

{
  "span": 30,
  "response_type": "moment",
  "location": 15,
  "loading_standard": "IRC_Class_A"
}

# Or with custom load train:
{
  "span": 30,
  "response_type": "moment",
  "location": 15,
  "load_train": [
    {"load": 100, "spacing": 2},
    {"load": 150, "spacing": 3},
    {"load": 100, "spacing": 0}
  ]
}
```

### Temperature Analysis
```http
POST /api/specialized-design/temperature-analysis
Content-Type: application/json

# Uniform temperature:
{
  "analysis_type": "uniform",
  "delta_T": 30,
  "material": "concrete",
  "length": 50000,
  "area": 300000,
  "restraint": "fixed"
}

# Temperature gradient:
{
  "analysis_type": "gradient",
  "T_top": 40,
  "T_bottom": 20,
  "depth": 500,
  "material": "concrete",
  "length": 10000,
  "I": 200000000
}

# Fire exposure:
{
  "analysis_type": "fire",
  "fire_duration": 60,
  "section_type": "column",
  "dimensions": {"width": 400, "depth": 400},
  "cover": 50
}

# Seasonal effects:
{
  "analysis_type": "seasonal",
  "T_summer": 45,
  "T_winter": 5,
  "length": 100000,
  "material": "steel",
  "expansion_joint_spacing": 30000
}
```

### Meshing
```http
# Generate mesh:
POST /api/specialized-design/mesh/generate
Content-Type: application/json

{
  "mesh_type": "rectangle",
  "width": 5000,
  "height": 3000,
  "nx": 10,
  "ny": 6,
  "element_type": "quad4"
}

# Refine mesh:
POST /api/specialized-design/mesh/refine
Content-Type: application/json

{
  "mesh": {...},
  "refinement_factor": 2
}

# Check mesh quality:
POST /api/specialized-design/mesh/quality-check
Content-Type: application/json

{
  "mesh": {...}
}
```

---

## 3. Serviceability Checks API

**Base URL:** `/api/serviceability`

### Deflection Check
```http
POST /api/serviceability/deflection
Content-Type: application/json

{
  "span": 6000,
  "actual_deflection": 15,
  "member_type": "beam",
  "support_condition": "simply_supported",
  "loading_type": "live"
}
```

### Crack Width Check
```http
POST /api/serviceability/crack-width
Content-Type: application/json

{
  "stress_steel": 200,
  "cover": 40,
  "bar_diameter": 16,
  "spacing": 150,
  "exposure_condition": "moderate"
}
```

### Vibration Check
```http
POST /api/serviceability/vibration
Content-Type: application/json

{
  "natural_frequency": 4.5,
  "floor_type": "office",
  "damping_ratio": 0.05
}
```

### Punching Shear Check
```http
POST /api/serviceability/punching-shear
Content-Type: application/json

{
  "column_size": 400,
  "slab_thickness": 200,
  "column_load": 1500,
  "fck": 25
}
```

### Fatigue Check
```http
POST /api/serviceability/fatigue
Content-Type: application/json

{
  "stress_range": 80,
  "n_cycles": 2000000,
  "material": "steel",
  "detail_category": "C"
}
```

### Slenderness Check
```http
POST /api/serviceability/slenderness
Content-Type: application/json

{
  "length": 4000,
  "radius_of_gyration": 100,
  "member_type": "column",
  "end_conditions": "pinned_pinned"
}
```

---

## 📊 Response Format

All endpoints return responses in this format:

```json
{
  "status": "success",
  "results": {
    // Specific results based on endpoint
    "status": "OK" or "FAIL",
    "utilization": 85.5,
    // ... other fields
  }
}
```

Error responses:
```json
{
  "detail": "Error message here"
}
```

---

## 🔧 Common Parameters

### Material Properties
- `fck`: Concrete strength (MPa) - default: 25
- `fy`: Steel yield strength (MPa) - default: 415
- `Es`: Steel modulus (MPa) - default: 200000
- `Ec`: Concrete modulus (MPa) - calculated

### Units
- **Length**: mm (millimeters)
- **Force**: kN (kilonewtons)
- **Moment**: kNm (kilonewton-meters)
- **Stress**: MPa (megapascals)
- **Temperature**: °C (Celsius)

### Design Codes
- `IS456` - Indian Standard (RC)
- `IS800` - Indian Standard (Steel)
- `ACI318` - American (RC)
- `AISC360` - American (Steel)
- `EC2` - Eurocode (RC)
- `EC3` - Eurocode (Steel)
- `BS8110` - British Standard (RC)
- `BS5950` - British Standard (Steel)

---

## 🎯 Usage Examples

### Example 1: Design a Two-Way Slab
```javascript
const response = await fetch('/api/advanced-analysis/slab-design', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    slab_type: "two_way",
    span_x: 5000,
    span_y: 6000,
    thickness: 150,
    loads: { dead: 2.0, live: 3.0 },
    support_condition: "all_edges_supported"
  })
});

const result = await response.json();
console.log(result.results.x_direction_steel.designation);
// Output: "12mm @ 150mm c/c"
```

### Example 2: Check Deflection
```javascript
const response = await fetch('/api/serviceability/deflection', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    span: 6000,
    actual_deflection: 15,
    member_type: "beam",
    loading_type: "live"
  })
});

const result = await response.json();
console.log(result.results.status); // "OK" or "FAIL"
console.log(result.results.utilization); // 90.0 (%)
```

### Example 3: Analyze Moving Load
```javascript
const response = await fetch('/api/specialized-design/moving-load', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    span: 30,
    response_type: "moment",
    location: 15,
    loading_standard: "IRC_Class_A"
  })
});

const result = await response.json();
console.log(result.results.max_response); // Maximum moment
console.log(result.results.critical_position); // Position of max response
```

---

## 📚 Additional Resources

- Full API Documentation: `/docs` (Swagger UI)
- Interactive API: `/redoc` (ReDoc)
- GitHub: [repository link]
- Support: [support email]

---

**All endpoints are now live and ready to use! 🚀**
