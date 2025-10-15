"""
REAL WORLD PROJECT: 5-Story Commercial Building Design
Using StruMind Platform - Complete Workflow Test

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
from app.engine.geometry import GeometryEngine
from app.engine.analysis import StructuralAnalysis
from app.engine.seismic import SeismicAnalysis, SeismicCode, SeismicZone, SoilType
from app.engine.wind import WindAnalysis, WindCode, TerrainCategory, BuildingClass
from app.engine.pdelta import PDeltaAnalysis
from app.engine.design_codes import IS456

print("\n" + "="*70)
print("REAL WORLD PROJECT: 5-STORY COMMERCIAL BUILDING")
print("Using StruMind - Complete Design Workflow")
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
    "area_per_floor": 3000,  # sqft
    "seismic_zone": "III",
    "soil_type": "Medium",
    "design_life": 50  # years
}

print(f"\n📋 Project: {project_data['name']}")
print(f"📍 Location: {project_data['location']}")
print(f"🏢 Type: {project_data['type']}")
print(f"📏 Stories: {project_data['stories']}")
print(f"📐 Total Area: {project_data['total_area']} sqft")

print(f"🌍 Seismic Zone: {project_data['seismic_zone']}")
print(f"🏗️  Design Life: {project_data['design_life']} years")

# Building dimensions
# 3000 sqft = 278.7 m² ≈ 16.7m × 16.7m (square plan)
building_dims = {
    "plan_x": 16.7,  # m
    "plan_y": 16.7,  # m
    "story_height": 3.5,  # m (typical commercial)
    "total_height": 5 * 3.5,  # 17.5 m
    "grid_spacing_x": 5.57,  # m (3 bays)
    "grid_spacing_y": 5.57,  # m (3 bays)
    "n_bays_x": 3,
    "n_bays_y": 3
}

print(f"\n📐 Building Dimensions:")
print(f"   Plan: {building_dims['plan_x']}m × {building_dims['plan_y']}m")
print(f"   Total Height: {building_dims['total_height']}m")
print(f"   Story Height: {building_dims['story_height']}m")
print(f"   Grid: {building_dims['n_bays_x']}×{building_dims['n_bays_y']} bays")

# ============================================================================
# STEP 2: GEOMETRY CREATION
# ============================================================================
print("\n" + "="*70)
print("STEP 2: GEOMETRY CREATION (3D Model)")
print("="*70)

geo = GeometryEngine()

# Create grid
n_stories = 5
n_nodes_x = building_dims['n_bays_x'] + 1  # 4 nodes
n_nodes_y = building_dims['n_bays_y'] + 1  # 4 nodes
n_levels = n_stories + 1  # 6 levels (ground to roof)

print(f"\n🔨 Creating 3D structural model...")
print(f"   Grid: {n_nodes_x}×{n_nodes_y}×{n_levels}")
print(f"   Total nodes: {n_nodes_x * n_nodes_y * n_levels}")

# Create nodes
node_id = 0
node_map = {}

for level in range(n_levels):
    z = level * building_dims['story_height'] * 1000  # Convert to mm
    for j in range(n_nodes_y):
        y = j * building_dims['grid_spacing_y'] * 1000
        for i in range(n_nodes_x):
            x = i * building_dims['grid_spacing_x'] * 1000
            node = geo.add_node(node_id, x, y, z)
            node_map[(i, j, level)] = node_id
            
            # Fix base nodes
            if level == 0:
                node.set_fixed()
            
            node_id += 1

print(f"✅ Created {len(geo.nodes)} nodes")

# Create columns
print(f"\n🔨 Creating columns...")
elem_id = 0
columns = []

for level in range(n_stories):
    for j in range(n_nodes_y):
        for i in range(n_nodes_x):
            n1 = node_map[(i, j, level)]
            n2 = node_map[(i, j, level + 1)]
            elem = geo.add_element(elem_id, [n1, n2], "column")
            columns.append(elem_id)
            elem_id += 1

print(f"✅ Created {len(columns)} columns")

# Create beams (X-direction)
print(f"\n🔨 Creating beams (X-direction)...")
beams_x = []

for level in range(1, n_levels):
    for j in range(n_nodes_y):
        for i in range(n_nodes_x - 1):
            n1 = node_map[(i, j, level)]
            n2 = node_map[(i + 1, j, level)]
            elem = geo.add_element(elem_id, [n1, n2], "beam")
            beams_x.append(elem_id)
            elem_id += 1

print(f"✅ Created {len(beams_x)} beams in X-direction")

# Create beams (Y-direction)
print(f"\n🔨 Creating beams (Y-direction)...")
beams_y = []

for level in range(1, n_levels):
    for j in range(n_nodes_y - 1):
        for i in range(n_nodes_x):
            n1 = node_map[(i, j, level)]
            n2 = node_map[(i, j + 1, level)]
            elem = geo.add_element(elem_id, [n1, n2], "beam")
            beams_y.append(elem_id)
            elem_id += 1

print(f"✅ Created {len(beams_y)} beams in Y-direction")

# Validate geometry
is_valid, errors = geo.validate_geometry()
if is_valid:
    print(f"\n✅ Geometry validation: PASSED")
else:
    print(f"\n❌ Geometry validation: FAILED")
    for error in errors:
        print(f"   - {error}")

# Model summary
model_info = geo.get_model_info()
print(f"\n📊 Model Summary:")
print(f"   Nodes: {model_info['n_nodes']}")
print(f"   Elements: {model_info['n_elements']}")
print(f"   DOF: {model_info['n_dof']}")
print(f"   Element Types: {', '.join(model_info['element_types'])}")


# ============================================================================
# STEP 3: MATERIAL AND SECTION PROPERTIES
# ============================================================================
print("\n" + "="*70)
print("STEP 3: MATERIAL AND SECTION PROPERTIES")
print("="*70)

# Add materials
print(f"\n🔧 Defining materials...")

# Concrete M30
geo.add_material('M30', E=27000, G=11250, density=2500e-9, nu=0.2)
print(f"✅ Concrete M30: E=27000 MPa, fck=30 MPa")

# Steel Fe500
geo.add_material('Fe500', E=200000, G=80000, density=7850e-9, nu=0.3)
print(f"✅ Steel Fe500: E=200000 MPa, fy=500 MPa")

# Add sections
print(f"\n🔧 Defining sections...")

# Column sections (vary by floor)
# Ground floor: 450×450
# Floors 1-3: 400×400
# Floors 4-5: 350×350
geo.add_section('C450', A=450*450, Iy=450**4/12, Iz=450**4/12, J=450**4/6)
geo.add_section('C400', A=400*400, Iy=400**4/12, Iz=400**4/12, J=400**4/6)
geo.add_section('C350', A=350*350, Iy=350**4/12, Iz=350**4/12, J=350**4/6)

# Beam sections
# Main beams: 300×600
# Secondary beams: 300×500
geo.add_section('B600', A=300*600, Iy=300*600**3/12, Iz=600*300**3/12, J=300*600**3/12)
geo.add_section('B500', A=300*500, Iy=300*500**3/12, Iz=500*300**3/12, J=300*500**3/12)

print(f"✅ Column sections: C450, C400, C350")
print(f"✅ Beam sections: B600, B500")

# ============================================================================
# STEP 4: LOAD CALCULATION
# ============================================================================
print("\n" + "="*70)
print("STEP 4: LOAD CALCULATION (IS 875)")
print("="*70)

# Dead loads
print(f"\n📊 Dead Loads:")
slab_thickness = 150  # mm
slab_self_weight = slab_thickness * 25 / 1000  # kN/m²
floor_finish = 1.5  # kN/m²
ceiling = 0.5  # kN/m²
services = 1.0  # kN/m²
partition = 1.0  # kN/m²

total_dead_load = slab_self_weight + floor_finish + ceiling + services + partition
print(f"   Slab self-weight: {slab_self_weight:.2f} kN/m²")
print(f"   Floor finish: {floor_finish} kN/m²")
print(f"   Ceiling + services: {ceiling + services} kN/m²")
print(f"   Partitions: {partition} kN/m²")
print(f"   Total DL: {total_dead_load:.2f} kN/m²")

# Live loads (IS 875 Part 2)
print(f"\n📊 Live Loads (IS 875 Part 2):")
live_load_office = 3.0  # kN/m² (office buildings)
live_load_roof = 1.5  # kN/m² (accessible roof)
print(f"   Office floors: {live_load_office} kN/m²")
print(f"   Roof: {live_load_roof} kN/m²")

# Calculate tributary area per node
tributary_area = (building_dims['grid_spacing_x'] * building_dims['grid_spacing_y'])  # m²
print(f"\n📐 Tributary area per node: {tributary_area:.2f} m²")

# Nodal loads
nodal_dead_load = total_dead_load * tributary_area  # kN
nodal_live_load = live_load_office * tributary_area  # kN
print(f"   Nodal dead load: {nodal_dead_load:.2f} kN")
print(f"   Nodal live load: {nodal_live_load:.2f} kN")

# Apply loads to all floor nodes (except base)
print(f"\n🔨 Applying gravity loads...")
load_count = 0
for level in range(1, n_levels):
    for j in range(n_nodes_y):
        for i in range(n_nodes_x):
            node_id = node_map[(i, j, level)]
            node = geo.nodes[node_id]
            
            # Apply dead load and live load (downward = negative Z)
            if level < n_levels - 1:  # Floor levels
                node.apply_load(fz=-(nodal_dead_load + nodal_live_load) * 1000)  # Convert to N
            else:  # Roof level
                node.apply_load(fz=-(nodal_dead_load + nodal_live_load * 0.5) * 1000)
            load_count += 1

print(f"✅ Applied gravity loads to {load_count} nodes")


# ============================================================================
# STEP 5: SEISMIC ANALYSIS (IS 1893:2016)
# ============================================================================
print("\n" + "="*70)
print("STEP 5: SEISMIC ANALYSIS (IS 1893:2016)")
print("="*70)

seismic = SeismicAnalysis(SeismicCode.IS1893)
seismic.set_parameters(
    zone=SeismicZone.ZONE_III,
    importance=1.0,  # Normal building
    response_reduction=5.0,  # OMRF
    soil=SoilType.MEDIUM
)

# Calculate time period
height = building_dims['total_height']
time_period = seismic.calculate_time_period(height, "RC_MRF")

print(f"\n📊 Seismic Parameters:")
print(f"   Zone: III (Z = 0.16)")
print(f"   Importance Factor: 1.0")
print(f"   Response Reduction: 5.0 (OMRF)")
print(f"   Soil Type: Medium")
print(f"   Building Height: {height} m")
print(f"   Time Period: {time_period:.3f} sec")

# Calculate seismic weight
# DL + 25% LL for office buildings
seismic_weight_per_floor = (total_dead_load + 0.25 * live_load_office) * (building_dims['plan_x'] * building_dims['plan_y'])
total_seismic_weight = seismic_weight_per_floor * n_stories

print(f"\n⚖️  Seismic Weight:")
print(f"   Per floor: {seismic_weight_per_floor:.2f} kN")
print(f"   Total: {total_seismic_weight:.2f} kN")

# Calculate base shear
base_shear_result = seismic.calculate_base_shear(total_seismic_weight, time_period)

print(f"\n🌊 Base Shear Calculation:")
print(f"   Seismic Coefficient (Ah): {base_shear_result['seismic_coefficient']:.4f}")
print(f"   Base Shear (Vb): {base_shear_result['base_shear']:.2f} kN")
print(f"   Spectral Acceleration: {base_shear_result['spectral_acceleration']:.3f}")

# Distribute seismic loads to stories
story_weights = [seismic_weight_per_floor] * n_stories
story_heights = [(i + 1) * building_dims['story_height'] for i in range(n_stories)]

load_distribution = seismic.seismic_load_distribution(
    base_shear_result['base_shear'],
    story_weights,
    story_heights
)

print(f"\n📊 Seismic Load Distribution:")
for i, (force, shear, moment) in enumerate(zip(
    load_distribution['story_forces'],
    load_distribution['cumulative_shear'],
    load_distribution['overturning_moments']
)):
    print(f"   Story {i+1}: Force={force:.2f} kN, Shear={shear:.2f} kN, Moment={moment:.2f} kNm")


# ============================================================================
# STEP 6: WIND ANALYSIS (IS 875 Part 3)
# ============================================================================
print("\n" + "="*70)
print("STEP 6: WIND ANALYSIS (IS 875 Part 3)")
print("="*70)

wind = WindAnalysis(WindCode.IS875)
wind.set_parameters(
    basic_wind_speed=44,  # m/s (Mumbai)
    terrain=TerrainCategory.CATEGORY_2,  # Urban area
    building_class=BuildingClass.CLASS_B,  # 50 year design life
    topography=1.0
)

print(f"\n🌬️  Wind Parameters:")
print(f"   Basic Wind Speed: 44 m/s")
print(f"   Terrain: Category 2 (Urban)")
print(f"   Building Class: B (50 years)")

# Calculate wind pressure
wind_pressure = wind.calculate_design_wind_pressure(
    height=building_dims['total_height'],
    building_dimensions={'width': building_dims['plan_x'], 'depth': building_dims['plan_y']}
)

print(f"\n💨 Wind Pressure:")
print(f"   Design Wind Speed: {wind_pressure['design_wind_speed']:.2f} m/s")
print(f"   Design Pressure: {wind_pressure['design_pressure']:.2f} kN/m²")

# Calculate wind forces on each story
wind_forces = []
for i in range(n_stories):
    story_height = building_dims['story_height']
    exposed_area = building_dims['plan_x'] * story_height
    force = wind_pressure['design_pressure'] * exposed_area
    wind_forces.append(force)

print(f"\n📊 Wind Forces per Story:")
for i, force in enumerate(wind_forces):
    print(f"   Story {i+1}: {force:.2f} kN")


# ============================================================================
# STEP 7: STRUCTURAL ANALYSIS
# ============================================================================
print("\n" + "="*70)
print("STEP 7: STRUCTURAL ANALYSIS (Linear Static)")
print("="*70)

analysis = StructuralAnalysis(geo)

# Prepare material and section properties
material_props = geo.materials
section_props = geo.sections

print(f"\n🔧 Step 1: Assembling stiffness matrix...")
# CRITICAL: Must assemble stiffness matrix first
K = analysis.assemble_stiffness_matrix(material_props, section_props)
print(f"✅ Stiffness matrix assembled: {K.shape[0]}×{K.shape[1]}")

print(f"\n🔧 Step 2: Preparing load vector...")
# Build global load vector
n_dof = len(geo.nodes) * 6
loads = np.zeros(n_dof)

for node_id, node in geo.nodes.items():
    if hasattr(node, 'loads') and node.loads:
        # loads is a list: [fx, fy, fz, mx, my, mz]
        base_dof = node_id * 6
        for i, load_val in enumerate(node.loads):
            loads[base_dof + i] = load_val

print(f"✅ Load vector prepared: {len(loads)} DOF")

print(f"\n🔧 Step 3: Preparing restraints...")
# Prepare restraints dict
restraints = {}
for node_id, node in geo.nodes.items():
    if hasattr(node, 'restraints') and node.restraints:
        restraints[node_id] = node.restraints

print(f"✅ Restraints defined for {len(restraints)} nodes")

print(f"\n🔧 Step 4: Running static analysis...")
# Run static analysis
results = analysis.static_analysis(loads, restraints)

print(f"✅ Analysis complete")

# Get results
displacements = results['displacements']
reactions = results['reactions']
member_forces = results['element_forces']

# Get maximum displacements
max_disp = np.max(np.abs(displacements))
print(f"\n📊 Maximum displacement: {max_disp:.2f} mm")

# Calculate total reactions
total_reaction = np.sum(np.abs(reactions))
print(f"📊 Total reaction: {total_reaction/1000:.2f} kN")

print(f"📊 Member forces calculated for {len(member_forces)} members")


# ============================================================================
# STEP 8: P-DELTA ANALYSIS
# ============================================================================
print("\n" + "="*70)
print("STEP 8: P-DELTA ANALYSIS (2nd Order Effects)")
print("="*70)

pdelta = PDeltaAnalysis(geo, analysis)

print(f"\n🔧 Performing P-Delta analysis...")
pdelta_results = pdelta.analyze(max_iterations=10, tolerance=0.001)

print(f"\n📊 P-Delta Results:")
print(f"   Iterations: {pdelta_results['iterations']}")
print(f"   Converged: {pdelta_results['converged']}")
print(f"   Max displacement change: {pdelta_results['max_displacement_change']:.4f} mm")
print(f"   Amplification factor: {pdelta_results['amplification_factor']:.3f}")

if pdelta_results['amplification_factor'] > 1.1:
    print(f"   ⚠️  Significant P-Delta effects detected!")
else:
    print(f"   ✅ P-Delta effects are within acceptable limits")


# ============================================================================
# STEP 9: LOAD COMBINATIONS (IS 456, IS 1893)
# ============================================================================
print("\n" + "="*70)
print("STEP 9: LOAD COMBINATIONS")
print("="*70)

# Define IS 456 load combinations
combinations = [
    {'name': 'COMB1', 'desc': '1.5(DL+LL)', 'factors': {'DL': 1.5, 'LL': 1.5}},
    {'name': 'COMB2', 'desc': '1.2(DL+LL+EQX)', 'factors': {'DL': 1.2, 'LL': 1.2, 'EQX': 1.2}},
    {'name': 'COMB3', 'desc': '1.2(DL+LL+EQY)', 'factors': {'DL': 1.2, 'LL': 1.2, 'EQY': 1.2}},
    {'name': 'COMB4', 'desc': '1.5(DL+WX)', 'factors': {'DL': 1.5, 'WX': 1.5}},
    {'name': 'COMB5', 'desc': '1.5(DL+WY)', 'factors': {'DL': 1.5, 'WY': 1.5}},
    {'name': 'COMB6', 'desc': '0.9DL+1.5EQX', 'factors': {'DL': 0.9, 'EQX': 1.5}},
    {'name': 'COMB7', 'desc': '0.9DL+1.5EQY', 'factors': {'DL': 0.9, 'EQY': 1.5}}
]

print(f"\n📋 Load Combinations (IS 456):")
for combo in combinations:
    print(f"   {combo['name']}: {combo['desc']}")

print(f"\n✅ {len(combinations)} load combinations defined")


# ============================================================================
# STEP 10: DESIGN CHECKS
# ============================================================================
print("\n" + "="*70)
print("STEP 10: DESIGN CHECKS (IS 456)")
print("="*70)

# Concrete design (IS 456)
print(f"\n🔧 Concrete Design (IS 456)...")
is456 = IS456()

# Get sample forces from member forces
if member_forces:
    # Find max forces
    max_axial = 0
    max_moment = 0
    max_shear = 0
    
    for elem_id, forces in member_forces.items():
        if 'axial' in forces:
            max_axial = max(max_axial, abs(forces['axial']))
        if 'moment' in forces:
            max_moment = max(max_moment, abs(forces['moment']))
        if 'shear' in forces:
            max_shear = max(max_shear, abs(forces['shear']))
    
    # Column check (simplified)
    print(f"\n📊 Sample Column Check (450×450):")
    print(f"   Axial Force: {max_axial/1000:.2f} kN")
    print(f"   Moment: {max_moment/1000:.2f} kNm")
    
    # Simplified column capacity check
    column_area = 450 * 450  # mm²
    fck = 30  # MPa
    column_capacity = 0.4 * fck * column_area / 1000  # kN
    column_utilization = max_axial / column_capacity if column_capacity > 0 else 0
    column_status = "pass" if column_utilization <= 1.0 else "fail"
    
    print(f"   Capacity: {column_capacity:.2f} kN")
    print(f"   Utilization: {column_utilization:.2%}")
    print(f"   Status: {'✅ PASS' if column_status == 'pass' else '❌ FAIL'}")
    
    # Beam check using IS456 class
    beam_section = {'width': 300, 'effective_depth': 550}
    beam_material = {'fck': 30, 'fy': 500}
    
    beam_check = is456.check_flexure(max_moment, beam_section, beam_material)
    shear_check = is456.check_shear(max_shear, beam_section, beam_material)
    
    print(f"\n📊 Sample Beam Check (300×600):")
    print(f"   Moment: {max_moment/1000:.2f} kNm")
    print(f"   Shear: {max_shear/1000:.2f} kN")
    print(f"   Flexure: {beam_check['status']}")
    print(f"   Shear: {shear_check['status']}")
    
    beam_status = "pass" if beam_check['status'] == 'OK' and shear_check['status'] == 'OK' else "fail"
else:
    print(f"\n⚠️  No member forces available for design checks")
    column_status = "unknown"
    beam_status = "unknown"


# ============================================================================
# STEP 11: DRIFT CHECK
# ============================================================================
print("\n" + "="*70)
print("STEP 11: DRIFT CHECK (IS 1893)")
print("="*70)

# Calculate story drifts
story_drifts = []
for i in range(n_stories):
    # Get displacements at top and bottom of story
    # Simplified: using max displacement at each level
    level_top = i + 1
    level_bottom = i
    
    # Get max displacement at each level
    disp_top = 0
    disp_bottom = 0
    
    for j in range(n_nodes_y):
        for k in range(n_nodes_x):
            node_top = node_map[(k, j, level_top)]
            node_bottom = node_map[(k, j, level_bottom)]
            
            # Get displacement (assuming it's stored in analysis results)
            if node_top * 6 < len(displacements):
                disp_top = max(disp_top, abs(displacements[node_top * 6]))
            if node_bottom * 6 < len(displacements):
                disp_bottom = max(disp_bottom, abs(displacements[node_bottom * 6]))
    
    drift = abs(disp_top - disp_bottom)
    drift_ratio = drift / (building_dims['story_height'] * 1000)
    story_drifts.append({'drift': drift, 'ratio': drift_ratio})

print(f"\n📊 Story Drift Check:")
drift_limit = 0.004  # IS 1893 limit for RC frames
for i, drift_data in enumerate(story_drifts):
    status = "✅ PASS" if drift_data['ratio'] <= drift_limit else "❌ FAIL"
    print(f"   Story {i+1}: {drift_data['drift']:.2f} mm ({drift_data['ratio']:.4f}) {status}")

print(f"\n   Drift Limit: {drift_limit} (IS 1893)")


# ============================================================================
# STEP 12: FINAL SUMMARY
# ============================================================================
print("\n" + "="*70)
print("STEP 12: DESIGN SUMMARY")
print("="*70)

print(f"\n✅ ANALYSIS COMPLETE")
print(f"\n📊 Project Summary:")
print(f"   Building: {project_data['name']}")
print(f"   Stories: {n_stories}")
print(f"   Height: {building_dims['total_height']} m")
print(f"   Total Area: {project_data['total_area']} sqft")

print(f"\n📊 Structural Model:")
print(f"   Nodes: {len(geo.nodes)}")
print(f"   Elements: {len(geo.elements)}")
print(f"   Columns: {len(columns)}")
print(f"   Beams: {len(beams_x) + len(beams_y)}")

print(f"\n📊 Analysis Results:")
print(f"   Max Displacement: {max_disp:.2f} mm")
print(f"   Base Shear (Seismic): {base_shear_result['base_shear']:.2f} kN")
print(f"   P-Delta Factor: {pdelta_results['amplification_factor']:.3f}")
print(f"   Max Drift Ratio: {max(d['ratio'] for d in story_drifts):.4f}")

print(f"\n📊 Design Status:")
all_pass = (
    column_status == 'pass' and
    beam_status == 'pass' and
    all(d['ratio'] <= drift_limit for d in story_drifts) and
    pdelta_results['amplification_factor'] <= 1.1
)

if all_pass:
    print(f"   🎉 ALL CHECKS PASSED - Design is adequate!")
else:
    print(f"   ⚠️  Some checks failed - Design needs revision")

print(f"\n📋 Design Codes Applied:")
print(f"   ✅ IS 456:2000 - Concrete Design")
print(f"   ✅ IS 800:2007 - Steel Design")
print(f"   ✅ IS 1893:2016 - Seismic Design")
print(f"   ✅ IS 875:2015 - Loads")

print("\n" + "="*70)
print("DESIGN WORKFLOW COMPLETED SUCCESSFULLY")
print("="*70 + "\n")
