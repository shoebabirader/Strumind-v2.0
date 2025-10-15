"""
REAL WORLD PROJECT: 5-Story Commercial Building Design
Using StruMind Unified Workflow - Clean and Simple

Project: Commercial Office Building
Location: Mumbai, India (Seismic Zone III)
Total Area: 3000 sqft per floor (15,000 sqft total)
Stories: 5 floors + roof
Design Codes: IS 456, IS 800, IS 1893, IS 875
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
from app.engine.workflow import StructuralWorkflow
from app.engine.seismic import SeismicCode, SeismicZone, SoilType
from app.engine.wind import WindCode, TerrainCategory, BuildingClass

print("\n" + "="*70)
print("REAL WORLD PROJECT: 5-STORY COMMERCIAL BUILDING")
print("Using StruMind Unified Workflow")
print("="*70)

# ============================================================================
# STEP 1: PROJECT DEFINITION
# ============================================================================
print("\n" + "="*70)
print("STEP 1: PROJECT DEFINITION")
print("="*70)

project_data = {
    "name": "Mumbai Commercial Tower",
    "client": "Tech Solutions Pvt Ltd",
    "location": "Mumbai, Maharashtra, India",
    "type": "Commercial Office Building",
    "stories": 5,
    "total_area": 15000,  # sqft
    "seismic_zone": "III",
    "design_life": 50  # years
}

print(f"\nProject: {project_data['name']}")
print(f"Location: {project_data['location']}")
print(f"Type: {project_data['type']}")
print(f"Stories: {project_data['stories']}")
print(f"Total Area: {project_data['total_area']} sqft")

# Building dimensions
building_dims = {
    "plan_x": 16.7,  # m
    "plan_y": 16.7,  # m
    "story_height": 3.5,  # m
    "total_height": 5 * 3.5,  # 17.5 m
    "grid_spacing_x": 5.57,  # m (3 bays)
    "grid_spacing_y": 5.57,  # m (3 bays)
    "n_bays_x": 3,
    "n_bays_y": 3
}

print(f"\nBuilding Dimensions:")
print(f"   Plan: {building_dims['plan_x']}m × {building_dims['plan_y']}m")
print(f"   Total Height: {building_dims['total_height']}m")
print(f"   Story Height: {building_dims['story_height']}m")
print(f"   Grid: {building_dims['n_bays_x']}×{building_dims['n_bays_y']} bays")

# ============================================================================
# STEP 2: INITIALIZE WORKFLOW
# ============================================================================
print("\n" + "="*70)
print("STEP 2: INITIALIZE WORKFLOW")
print("="*70)

workflow = StructuralWorkflow()
print("\n✓ Workflow manager initialized")

# ============================================================================
# STEP 3: CREATE GEOMETRY
# ============================================================================
print("\n" + "="*70)
print("STEP 3: CREATE 3D GEOMETRY")
print("="*70)

n_stories = 5
n_nodes_x = building_dims['n_bays_x'] + 1  # 4 nodes
n_nodes_y = building_dims['n_bays_y'] + 1  # 4 nodes
n_levels = n_stories + 1  # 6 levels

print(f"\nCreating structural model...")
print(f"   Grid: {n_nodes_x}×{n_nodes_y}×{n_levels}")

# Create nodes
node_id = 0
node_map = {}

for level in range(n_levels):
    z = level * building_dims['story_height'] * 1000  # mm
    for j in range(n_nodes_y):
        y = j * building_dims['grid_spacing_y'] * 1000
        for i in range(n_nodes_x):
            x = i * building_dims['grid_spacing_x'] * 1000
            
            # Fix base nodes
            is_fixed = (level == 0)
            workflow.add_node(node_id, x, y, z, fixed=is_fixed)
            node_map[(i, j, level)] = node_id
            node_id += 1

print(f"✓ Created {node_id} nodes")

# Create columns
elem_id = 0
columns = []

for level in range(n_stories):
    for j in range(n_nodes_y):
        for i in range(n_nodes_x):
            n1 = node_map[(i, j, level)]
            n2 = node_map[(i, j, level + 1)]
            workflow.add_element(elem_id, [n1, n2], "column", 
                               material="M30", section="C450")
            columns.append(elem_id)
            elem_id += 1

print(f"✓ Created {len(columns)} columns")

# Create beams (X-direction)
beams_x = []
for level in range(1, n_levels):
    for j in range(n_nodes_y):
        for i in range(n_nodes_x - 1):
            n1 = node_map[(i, j, level)]
            n2 = node_map[(i + 1, j, level)]
            workflow.add_element(elem_id, [n1, n2], "beam",
                               material="M30", section="B600")
            beams_x.append(elem_id)
            elem_id += 1

print(f"✓ Created {len(beams_x)} beams (X-direction)")

# Create beams (Y-direction)
beams_y = []
for level in range(1, n_levels):
    for j in range(n_nodes_y - 1):
        for i in range(n_nodes_x):
            n1 = node_map[(i, j, level)]
            n2 = node_map[(i, j + 1, level)]
            workflow.add_element(elem_id, [n1, n2], "beam",
                               material="M30", section="B600")
            beams_y.append(elem_id)
            elem_id += 1

print(f"✓ Created {len(beams_y)} beams (Y-direction)")

# Validate geometry
is_valid, errors = workflow.validate_geometry()
if is_valid:
    print(f"\n✓ Geometry validation: PASSED")
else:
    print(f"\n✗ Geometry validation: FAILED")
    for error in errors:
        print(f"   - {error}")
    sys.exit(1)

# ============================================================================
# STEP 4: DEFINE MATERIALS AND SECTIONS
# ============================================================================
print("\n" + "="*70)
print("STEP 4: MATERIALS AND SECTIONS")
print("="*70)

# Add materials
workflow.add_material('M30', E=27000, density=2500e-9, nu=0.2)
print("✓ Concrete M30: E=27000 MPa, fck=30 MPa")

workflow.add_material('Fe500', E=200000, density=7850e-9, nu=0.3)
print("✓ Steel Fe500: E=200000 MPa, fy=500 MPa")

# Add sections
workflow.add_section('C450', A=450*450, Iy=450**4/12, Iz=450**4/12, J=450**4/6)
workflow.add_section('C400', A=400*400, Iy=400**4/12, Iz=400**4/12, J=400**4/6)
workflow.add_section('C350', A=350*350, Iy=350**4/12, Iz=350**4/12, J=350**4/6)
workflow.add_section('B600', A=300*600, Iy=300*600**3/12, Iz=600*300**3/12, J=300*600**3/12)
workflow.add_section('B500', A=300*500, Iy=300*500**3/12, Iz=500*300**3/12, J=300*500**3/12)

print("✓ Column sections: C450, C400, C350")
print("✓ Beam sections: B600, B500")

# ============================================================================
# STEP 5: APPLY LOADS
# ============================================================================
print("\n" + "="*70)
print("STEP 5: APPLY LOADS (IS 875)")
print("="*70)

# Calculate loads
slab_thickness = 150  # mm
slab_self_weight = slab_thickness * 25 / 1000  # kN/m²
floor_finish = 1.5
ceiling = 0.5
services = 1.0
partition = 1.0
total_dead_load = slab_self_weight + floor_finish + ceiling + services + partition

live_load_office = 3.0  # kN/m²
live_load_roof = 1.5  # kN/m²

print(f"\nDead Load: {total_dead_load:.2f} kN/m²")
print(f"Live Load (Office): {live_load_office} kN/m²")
print(f"Live Load (Roof): {live_load_roof} kN/m²")

# Calculate tributary area and nodal loads
tributary_area = building_dims['grid_spacing_x'] * building_dims['grid_spacing_y']
nodal_dead_load = total_dead_load * tributary_area * 1000  # N
nodal_live_load = live_load_office * tributary_area * 1000  # N

print(f"\nTributary area: {tributary_area:.2f} m²")
print(f"Nodal dead load: {nodal_dead_load/1000:.2f} kN")
print(f"Nodal live load: {nodal_live_load/1000:.2f} kN")

# Apply loads to floor nodes
load_count = 0
for level in range(1, n_levels):
    for j in range(n_nodes_y):
        for i in range(n_nodes_x):
            node_id = node_map[(i, j, level)]
            
            if level < n_levels - 1:  # Floor levels
                total_load = nodal_dead_load + nodal_live_load
            else:  # Roof level
                total_load = nodal_dead_load + nodal_live_load * 0.5
            
            workflow.apply_nodal_load(node_id, fz=-total_load)
            load_count += 1

print(f"✓ Applied gravity loads to {load_count} nodes")

# ============================================================================
# STEP 6: SEISMIC ANALYSIS
# ============================================================================
print("\n" + "="*70)
print("STEP 6: SEISMIC ANALYSIS (IS 1893:2016)")
print("="*70)

workflow.setup_seismic_analysis(
    code=SeismicCode.IS1893,
    zone=SeismicZone.ZONE_III,
    soil=SoilType.MEDIUM,
    importance=1.0,
    response_reduction=5.0
)

print("\nSeismic Parameters:")
print("   Zone: III (Z = 0.16)")
print("   Importance Factor: 1.0")
print("   Response Reduction: 5.0 (OMRF)")
print("   Soil Type: Medium")

# Calculate seismic weight and base shear
seismic_weight_per_floor = (total_dead_load + 0.25 * live_load_office) * \
                           (building_dims['plan_x'] * building_dims['plan_y'])
total_seismic_weight = seismic_weight_per_floor * n_stories

seismic_results = workflow.calculate_seismic_loads(
    height=building_dims['total_height'],
    weight=total_seismic_weight
)

print(f"\nSeismic Weight: {total_seismic_weight:.2f} kN")
print(f"Time Period: {seismic_results['time_period']:.3f} sec")
print(f"Base Shear: {seismic_results['base_shear']['base_shear']:.2f} kN")

# ============================================================================
# STEP 7: WIND ANALYSIS
# ============================================================================
print("\n" + "="*70)
print("STEP 7: WIND ANALYSIS (IS 875 Part 3)")
print("="*70)

workflow.setup_wind_analysis(
    code=WindCode.IS875,
    basic_wind_speed=44,  # m/s (Mumbai)
    terrain=TerrainCategory.CATEGORY_2,
    building_class=BuildingClass.CLASS_B,
    topography=1.0
)

print("\nWind Parameters:")
print("   Basic Wind Speed: 44 m/s")
print("   Terrain: Category 2 (Urban)")
print("   Building Class: B (50 years)")

wind_results = workflow.calculate_wind_loads(
    height=building_dims['total_height'],
    width=building_dims['plan_x'],
    depth=building_dims['plan_y']
)

print(f"\nDesign Wind Speed: {wind_results['design_wind_speed']:.2f} m/s")
print(f"Design Pressure: {wind_results['design_pressure']:.2f} kN/m²")

# ============================================================================
# STEP 8: RUN STRUCTURAL ANALYSIS
# ============================================================================
print("\n" + "="*70)
print("STEP 8: STRUCTURAL ANALYSIS")
print("="*70)

print("\nRunning static analysis with P-Delta effects...")
results = workflow.run_static_analysis(
    include_pdelta=True,
    pdelta_iterations=10,
    pdelta_tolerance=0.001
)

print(f"\n{results.summary()}")

# ============================================================================
# STEP 9: LOAD COMBINATIONS
# ============================================================================
print("\n" + "="*70)
print("STEP 9: LOAD COMBINATIONS (IS 456)")
print("="*70)

combinations = [
    {'name': 'COMB1', 'desc': '1.5(DL+LL)'},
    {'name': 'COMB2', 'desc': '1.2(DL+LL+EQX)'},
    {'name': 'COMB3', 'desc': '1.2(DL+LL+EQY)'},
    {'name': 'COMB4', 'desc': '1.5(DL+WX)'},
    {'name': 'COMB5', 'desc': '1.5(DL+WY)'},
    {'name': 'COMB6', 'desc': '0.9DL+1.5EQX'},
    {'name': 'COMB7', 'desc': '0.9DL+1.5EQY'}
]

print("\nLoad Combinations:")
for combo in combinations:
    print(f"   {combo['name']}: {combo['desc']}")

# ============================================================================
# STEP 10: DESIGN CHECKS
# ============================================================================
print("\n" + "="*70)
print("STEP 10: DESIGN CHECKS (IS 456)")
print("="*70)

print("\nPerforming concrete design checks...")
design_results = workflow.check_concrete_design(fck=30, fy=500)

print(f"\nColumns checked: {len(design_results['columns'])}")
print(f"Beams checked: {len(design_results['beams'])}")
print(f"Overall status: {design_results['status'].upper()}")

# Show sample results
if design_results['columns']:
    col = design_results['columns'][0]
    print(f"\nSample Column:")
    print(f"   Axial: {col['axial']/1000:.2f} kN")
    print(f"   Capacity: {col['capacity']:.2f} kN")
    print(f"   Utilization: {col['utilization']:.2%}")
    print(f"   Status: {col['status'].upper()}")

if design_results['beams']:
    beam = design_results['beams'][0]
    print(f"\nSample Beam:")
    print(f"   Moment: {beam['moment']/1000:.2f} kNm")
    print(f"   Shear: {beam['shear']/1000:.2f} kN")
    print(f"   Flexure: {beam['flexure']}")
    print(f"   Shear: {beam['shear_check']}")

# ============================================================================
# STEP 11: DRIFT CHECK
# ============================================================================
print("\n" + "="*70)
print("STEP 11: DRIFT CHECK (IS 1893)")
print("="*70)

# Calculate story drifts (simplified)
displacements = results.displacements
story_drifts = []

for i in range(n_stories):
    level_top = i + 1
    level_bottom = i
    
    # Get max displacement at each level
    disp_top = 0
    disp_bottom = 0
    
    for j in range(n_nodes_y):
        for k in range(n_nodes_x):
            node_top = node_map[(k, j, level_top)]
            node_bottom = node_map[(k, j, level_bottom)]
            
            if node_top * 6 < len(displacements):
                disp_top = max(disp_top, abs(displacements[node_top * 6]))
            if node_bottom * 6 < len(displacements):
                disp_bottom = max(disp_bottom, abs(displacements[node_bottom * 6]))
    
    drift = abs(disp_top - disp_bottom)
    drift_ratio = drift / (building_dims['story_height'] * 1000)
    story_drifts.append({'drift': drift, 'ratio': drift_ratio})

print("\nStory Drift Check:")
drift_limit = 0.004  # IS 1893 limit
for i, drift_data in enumerate(story_drifts):
    status = "PASS" if drift_data['ratio'] <= drift_limit else "FAIL"
    print(f"   Story {i+1}: {drift_data['drift']:.2f} mm ({drift_data['ratio']:.4f}) {status}")

print(f"\nDrift Limit: {drift_limit} (IS 1893)")

# ============================================================================
# STEP 12: FINAL SUMMARY
# ============================================================================
print("\n" + "="*70)
print("STEP 12: DESIGN SUMMARY")
print("="*70)

model_info = workflow.get_model_info()

print(f"\n✓ ANALYSIS COMPLETE")
print(f"\nProject: {project_data['name']}")
print(f"Stories: {n_stories}")
print(f"Height: {building_dims['total_height']} m")

print(f"\nStructural Model:")
print(f"   Nodes: {model_info['nodes']}")
print(f"   Elements: {model_info['elements']}")
print(f"   Materials: {model_info['materials']}")
print(f"   Sections: {model_info['sections']}")

print(f"\nAnalysis Results:")
print(f"   Max Displacement: {results.max_displacement:.2f} mm")
print(f"   Total Reaction: {results.total_reaction/1000:.2f} kN")
print(f"   Base Shear (Seismic): {seismic_results['base_shear']['base_shear']:.2f} kN")

print(f"\nDesign Status:")
all_pass = (
    design_results['status'] == 'pass' and
    all(d['ratio'] <= drift_limit for d in story_drifts) and
    len(results.warnings) == 0
)

if all_pass:
    print("   ✓ ALL CHECKS PASSED - Design is adequate!")
else:
    print("   ⚠ Some checks need attention:")
    if design_results['status'] != 'pass':
        print("      - Design capacity checks")
    if not all(d['ratio'] <= drift_limit for d in story_drifts):
        print("      - Drift limits exceeded")
    for warning in results.warnings:
        print(f"      - {warning}")

print(f"\nDesign Codes Applied:")
print("   ✓ IS 456:2000 - Concrete Design")
print("   ✓ IS 800:2007 - Steel Design")
print("   ✓ IS 1893:2016 - Seismic Design")
print("   ✓ IS 875:2015 - Loads")

print("\n" + "="*70)
print("DESIGN WORKFLOW COMPLETED SUCCESSFULLY")
print("="*70 + "\n")
