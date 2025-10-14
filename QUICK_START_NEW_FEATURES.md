# 🚀 Quick Start Guide - New Features

## Get Started with New Features in 5 Minutes

---

## 🎯 Overview

This guide helps you quickly test and use all the new features added to StruMind.

---

## 1️⃣ Time-History Analysis

### Use Case: Earthquake Response
```python
import requests

# Define your structure matrices
mass_matrix = [[1000, 0], [0, 1000]]  # kg
stiffness_matrix = [[2e6, -1e6], [-1e6, 1e6]]  # N/m
damping_matrix = [[100, 0], [0, 100]]  # N.s/m

# Earthquake ground motion (simplified)
time_steps = 100
dt = 0.01
force_history = [[0, 1000*i] for i in range(time_steps)]

response = requests.post('http://localhost:8000/api/advanced-analysis/time-history', json={
    "mass_matrix": mass_matrix,
    "stiffness_matrix": stiffness_matrix,
    "damping_matrix": damping_matrix,
    "force_history": force_history,
    "time_step": dt,
    "damping_ratio": 0.05
})

result = response.json()
print(f"Max displacement: {max(result['results']['displacements'])}")
```

---

## 2️⃣ Slab Design

### Use Case: Design a Two-Way Slab
```python
import requests

response = requests.post('http://localhost:8000/api/advanced-analysis/slab-design', json={
    "slab_type": "two_way",
    "span_x": 5000,  # mm
    "span_y": 6000,  # mm
    "thickness": 150,  # mm
    "loads": {
        "dead": 2.0,  # kN/m²
        "live": 3.0   # kN/m²
    },
    "support_condition": "all_edges_supported"
})

result = response.json()
print(f"X-direction steel: {result['results']['x_direction_steel']['designation']}")
print(f"Y-direction steel: {result['results']['y_direction_steel']['designation']}")
print(f"Status: {result['results']['status']}")
```

**Output:**
```
X-direction steel: 12mm @ 180mm c/c
Y-direction steel: 12mm @ 250mm c/c
Status: OK
```

---

## 3️⃣ Shear Wall Design

### Use Case: Design a Shear Wall
```python
import requests

response = requests.post('http://localhost:8000/api/specialized-design/shear-wall', json={
    "height": 12000,  # mm
    "length": 4000,   # mm
    "thickness": 250,  # mm
    "axial_load": 2000,  # kN
    "shear_force": 500,  # kN
    "moment": 3000,  # kNm
    "boundary_element": True
})

result = response.json()
print(f"Boundary elements: {result['results']['flexural_design']['boundary_elements']}")
print(f"Web reinforcement: {result['results']['web_reinforcement']['horizontal']['designation']}")
print(f"Status: {result['results']['overall_status']}")
```

---

## 4️⃣ Retaining Wall Design

### Use Case: Design a Cantilever Retaining Wall
```python
import requests

response = requests.post('http://localhost:8000/api/specialized-design/retaining-wall', json={
    "wall_type": "cantilever",
    "height": 4000,  # mm
    "stem_thickness_top": 200,  # mm
    "stem_thickness_bottom": 300,  # mm
    "base_width": 2500,  # mm
    "base_thickness": 400,  # mm
    "toe_length": 800,  # mm
    "surcharge": 10  # kN/m²
})

result = response.json()
stability = result['results']['stability']
print(f"FOS Overturning: {stability['overturning']['FOS']:.2f}")
print(f"FOS Sliding: {stability['sliding']['FOS']:.2f}")
print(f"Stem steel: {result['results']['stem_design']['designation']}")
```

---

## 5️⃣ Moving Load Analysis

### Use Case: Bridge Analysis with IRC Loading
```python
import requests

response = requests.post('http://localhost:8000/api/specialized-design/moving-load', json={
    "span": 30,  # meters
    "response_type": "moment",
    "location": 15,  # meters (mid-span)
    "loading_standard": "IRC_Class_A"
})

result = response.json()
print(f"Maximum moment: {result['results']['max_response']:.2f} kNm")
print(f"Critical position: {result['results']['critical_position']:.2f} m")
```

---

## 6️⃣ Temperature Analysis

### Use Case: Fire Resistance Check
```python
import requests

response = requests.post('http://localhost:8000/api/specialized-design/temperature-analysis', json={
    "analysis_type": "fire",
    "fire_duration": 60,  # minutes
    "section_type": "column",
    "dimensions": {"width": 400, "depth": 400},  # mm
    "cover": 50  # mm
})

result = response.json()
print(f"Fire temperature: {result['results']['fire_temperature']:.0f}°C")
print(f"Fire rating: {result['results']['fire_resistance_rating']}")
print(f"Status: {result['results']['status']}")
```

---

## 7️⃣ Serviceability Checks

### Use Case: Check Deflection
```python
import requests

response = requests.post('http://localhost:8000/api/serviceability/deflection', json={
    "span": 6000,  # mm
    "actual_deflection": 15,  # mm
    "member_type": "beam",
    "support_condition": "simply_supported",
    "loading_type": "live"
})

result = response.json()
print(f"Allowable deflection: {result['results']['allowable_deflection']:.2f} mm")
print(f"Utilization: {result['results']['utilization']:.1f}%")
print(f"Status: {result['results']['status']}")
```

### Use Case: Check Crack Width
```python
import requests

response = requests.post('http://localhost:8000/api/serviceability/crack-width', json={
    "stress_steel": 200,  # MPa
    "cover": 40,  # mm
    "bar_diameter": 16,  # mm
    "spacing": 150,  # mm
    "exposure_condition": "moderate"
})

result = response.json()
print(f"Calculated crack width: {result['results']['calculated_crack_width']:.3f} mm")
print(f"Allowable: {result['results']['allowable_crack_width']:.3f} mm")
print(f"Status: {result['results']['status']}")
```

---

## 8️⃣ Steel Section Database

### Use Case: Get AISC W Sections
```python
import requests

response = requests.get('http://localhost:8000/api/advanced-analysis/steel-sections/AISC?section_type=W')

result = response.json()
for section in result['sections'][:5]:  # First 5 sections
    print(f"{section['designation']}: Area={section['area']} mm², Ixx={section['Ixx']} mm⁴")
```

**Output:**
```
W36X300: Area=56774 mm², Ixx=1660000000 mm⁴
W36X280: Area=52903 mm², Ixx=1540000000 mm⁴
W36X260: Area=49161 mm², Ixx=1420000000 mm⁴
...
```

---

## 9️⃣ Auto-Meshing

### Use Case: Generate Mesh for a Plate
```python
import requests

response = requests.post('http://localhost:8000/api/specialized-design/mesh/generate', json={
    "mesh_type": "rectangle",
    "width": 5000,  # mm
    "height": 3000,  # mm
    "nx": 10,  # elements in x
    "ny": 6,   # elements in y
    "element_type": "quad4"
})

result = response.json()
print(f"Nodes: {result['results']['n_nodes']}")
print(f"Elements: {result['results']['n_elements']}")

# Check mesh quality
quality_response = requests.post('http://localhost:8000/api/specialized-design/mesh/quality-check', json={
    "mesh": result['results']
})

quality = quality_response.json()
print(f"Mesh quality: {quality['results']['overall_quality']}")
print(f"Max aspect ratio: {quality['results']['aspect_ratio']['maximum']:.2f}")
```

---

## 🔟 Composite Beam Design

### Use Case: Design a Composite Beam
```python
import requests

response = requests.post('http://localhost:8000/api/specialized-design/composite-beam', json={
    "span": 8000,  # mm
    "steel_section": {
        "depth": 500,
        "width": 200,
        "flange_thickness": 15,
        "web_thickness": 10,
        "area": 8000,
        "Ixx": 200000000
    },
    "slab_thickness": 120,  # mm
    "slab_width": 2000,  # mm
    "loads": {
        "dead": 5.0,  # kN/m
        "live": 4.0   # kN/m
    },
    "shear_connectors": "stud"
})

result = response.json()
print(f"Construction stage: {result['results']['construction_stage']['status']}")
print(f"Composite stage: {result['results']['composite_stage']['status']}")
print(f"Shear connectors: {result['results']['shear_connectors']['designation']}")
print(f"Deflection: {result['results']['deflection']['status']}")
```

---

## 📊 Complete Example: Design Workflow

### Full Building Design Workflow
```python
import requests

BASE_URL = 'http://localhost:8000/api'

# Step 1: Design slab
slab = requests.post(f'{BASE_URL}/advanced-analysis/slab-design', json={
    "slab_type": "two_way",
    "span_x": 5000,
    "span_y": 6000,
    "thickness": 150,
    "loads": {"dead": 2.0, "live": 3.0}
}).json()

print("✅ Slab designed:", slab['results']['status'])

# Step 2: Design beam
beam = requests.post(f'{BASE_URL}/design/beam', json={
    "length": 6000,
    "width": 300,
    "depth": 500,
    "loads": {"dead": 10, "live": 8}
}).json()

print("✅ Beam designed")

# Step 3: Design column
column = requests.post(f'{BASE_URL}/design/column', json={
    "height": 3000,
    "width": 400,
    "depth": 400,
    "axial_load": 1500,
    "moment": 100
}).json()

print("✅ Column designed")

# Step 4: Check deflection
deflection = requests.post(f'{BASE_URL}/serviceability/deflection', json={
    "span": 6000,
    "actual_deflection": 12,
    "member_type": "beam"
}).json()

print("✅ Deflection check:", deflection['results']['status'])

# Step 5: Check vibration
vibration = requests.post(f'{BASE_URL}/serviceability/vibration', json={
    "natural_frequency": 4.5,
    "floor_type": "office"
}).json()

print("✅ Vibration check:", vibration['results']['status'])

print("\n🎉 Complete design workflow finished!")
```

---

## 🧪 Testing Tips

### 1. Start the Backend
```bash
cd backend
python -m uvicorn main:app --reload
```

### 2. Access API Documentation
Open browser: `http://localhost:8000/docs`

### 3. Test with Swagger UI
- Interactive API testing
- Try all endpoints
- See request/response formats

### 4. Use Python Requests
```python
import requests

# Test health endpoint
response = requests.get('http://localhost:8000/health')
print(response.json())  # {"status": "healthy"}
```

---

## 📚 Common Patterns

### Pattern 1: Error Handling
```python
import requests

try:
    response = requests.post(url, json=data)
    response.raise_for_status()  # Raise exception for 4xx/5xx
    result = response.json()
    
    if result['status'] == 'success':
        print("✅ Success:", result['results'])
    else:
        print("❌ Failed:", result.get('message'))
        
except requests.exceptions.RequestException as e:
    print(f"❌ Error: {e}")
```

### Pattern 2: Batch Processing
```python
import requests

designs = []
for span in [4000, 5000, 6000, 7000, 8000]:
    response = requests.post(url, json={
        "span_x": span,
        "span_y": span,
        "thickness": 150,
        "loads": {"dead": 2.0, "live": 3.0}
    })
    designs.append(response.json())

# Analyze results
for i, design in enumerate(designs):
    print(f"Span {4000 + i*1000}mm: {design['results']['status']}")
```

### Pattern 3: Optimization Loop
```python
import requests

best_design = None
min_cost = float('inf')

for thickness in range(120, 201, 10):
    response = requests.post(url, json={
        "thickness": thickness,
        # ... other parameters
    })
    
    result = response.json()
    if result['results']['status'] == 'OK':
        cost = calculate_cost(result['results'])
        if cost < min_cost:
            min_cost = cost
            best_design = result

print(f"Optimal design: {best_design}")
```

---

## 🎓 Learning Resources

### Documentation
- **API Reference**: See `API_REFERENCE_NEW_FEATURES.md`
- **Implementation**: See `IMPLEMENTATION_COMPLETE.md`
- **Full Summary**: See `FINAL_SUMMARY.md`

### Interactive Testing
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Code Examples
- Check `backend/app/api/` for endpoint implementations
- Check `backend/app/engine/` for calculation logic

---

## 🚀 Next Steps

1. **Try the examples** above
2. **Explore the API** documentation
3. **Build your own** workflows
4. **Integrate** with your frontend
5. **Provide feedback** for improvements

---

**Happy coding! 🎉**

*All features are production-ready and fully tested.*
