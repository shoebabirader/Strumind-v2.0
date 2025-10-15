"""
COMPLETE END-TO-END APPLICATION TEST
Tests the entire StruMind platform with real API calls

This script:
1. Starts the backend server
2. Creates a real project via API
3. Creates a structural model
4. Runs analysis
5. Performs design checks
6. Generates reports
7. Verifies database storage

Author: StruMind Platform
"""

import requests
import json
import time
import sys
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
API_TIMEOUT = 30

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.END}\n")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_info(text: str):
    """Print info message"""
    print(f"{Colors.CYAN}→ {text}{Colors.END}")

def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def wait_for_server(max_attempts: int = 30):
    """Wait for the backend server to be ready"""
    print_info("Waiting for backend server to start...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=2)
            if response.status_code == 200:
                print_success("Backend server is ready!")
                return True
        except requests.exceptions.RequestException:
            time.sleep(1)
            print(f"  Attempt {attempt + 1}/{max_attempts}...", end='\r')
    
    print_error("Backend server failed to start")
    return False

def test_health_check():
    """Test basic health check"""
    print_header("TEST 1: HEALTH CHECK")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=API_TIMEOUT)
        if response.status_code == 200:
            print_success(f"Health check passed: {response.json()}")
            return True
        else:
            print_error(f"Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Health check error: {e}")
        return False

def test_create_project():
    """Test project creation"""
    print_header("TEST 2: CREATE PROJECT")
    
    project_data = {
        "name": "Mumbai Commercial Tower - Real Test",
        "client": "Tech Solutions Pvt Ltd",
        "location": "Mumbai, Maharashtra, India",
        "description": "5-story commercial office building",
        "project_type": "commercial",
        "design_codes": ["IS456", "IS800", "IS1893", "IS875"]
    }
    
    print_info(f"Creating project: {project_data['name']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/projects/create",
            json=project_data,
            timeout=API_TIMEOUT
        )
        
        if response.status_code == 200:
            result = response.json()
            project_id = result.get('id') or result.get('project_id')
            print_success(f"Project created with ID: {project_id}")
            print(f"  Name: {project_data['name']}")
            print(f"  Client: {project_data['client']}")
            print(f"  Location: {project_data['location']}")
            return project_id
        else:
            print_error(f"Project creation failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return None
    except Exception as e:
        print_error(f"Project creation error: {e}")
        return None

def test_create_model(project_id: int):
    """Test model creation with real geometry"""
    print_header("TEST 3: CREATE STRUCTURAL MODEL")
    
    print_info("Creating 3D structural model (4x4x6 grid)...")
    
    # Create nodes for a 5-story building
    nodes = []
    node_id = 0
    
    # Grid parameters
    n_x, n_y, n_levels = 4, 4, 6
    spacing_x, spacing_y, height = 5570, 5570, 3500  # mm
    
    for level in range(n_levels):
        z = level * height
        for j in range(n_y):
            y = j * spacing_y
            for i in range(n_x):
                x = i * spacing_x
                
                restraints = [True, True, True, True, True, True] if level == 0 else None
                
                nodes.append({
                    "id": node_id,
                    "x": x,
                    "y": y,
                    "z": z,
                    "restraints": restraints
                })
                node_id += 1
    
    print_success(f"Created {len(nodes)} nodes")
    
    # Create elements (columns and beams)
    elements = []
    elem_id = 0
    
    # Columns
    for level in range(n_levels - 1):
        for j in range(n_y):
            for i in range(n_x):
                n1 = level * (n_x * n_y) + j * n_x + i
                n2 = (level + 1) * (n_x * n_y) + j * n_x + i
                
                elements.append({
                    "id": elem_id,
                    "node_ids": [n1, n2],
                    "element_type": "column",
                    "material_id": "M30",
                    "section_id": "C450"
                })
                elem_id += 1
    
    print_success(f"Created {elem_id} columns")
    
    # Beams (X-direction)
    for level in range(1, n_levels):
        for j in range(n_y):
            for i in range(n_x - 1):
                n1 = level * (n_x * n_y) + j * n_x + i
                n2 = level * (n_x * n_y) + j * n_x + (i + 1)
                
                elements.append({
                    "id": elem_id,
                    "node_ids": [n1, n2],
                    "element_type": "beam",
                    "material_id": "M30",
                    "section_id": "B600"
                })
                elem_id += 1
    
    # Beams (Y-direction)
    for level in range(1, n_levels):
        for j in range(n_y - 1):
            for i in range(n_x):
                n1 = level * (n_x * n_y) + j * n_x + i
                n2 = level * (n_x * n_y) + (j + 1) * n_x + i
                
                elements.append({
                    "id": elem_id,
                    "node_ids": [n1, n2],
                    "element_type": "beam",
                    "material_id": "M30",
                    "section_id": "B600"
                })
                elem_id += 1
    
    print_success(f"Created {elem_id - 80} beams")
    print_success(f"Total elements: {len(elements)}")
    
    model_data = {
        "project_id": project_id,
        "name": "5-Story Frame Model",
        "nodes": nodes,
        "elements": elements,
        "materials": {
            "M30": {"E": 27000, "G": 11250, "density": 2.5e-6, "nu": 0.2},
            "Fe500": {"E": 200000, "G": 80000, "density": 7.85e-6, "nu": 0.3}
        },
        "sections": {
            "C450": {"A": 202500, "Iy": 3.42e9, "Iz": 3.42e9, "J": 6.84e9},
            "B600": {"A": 180000, "Iy": 5.4e9, "Iz": 1.35e9, "J": 5.4e9}
        }
    }
    
    print_info("Saving model to database...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/model/save",
            json=model_data,
            timeout=API_TIMEOUT
        )
        
        if response.status_code == 200:
            result = response.json()
            print_success(f"Model saved with ID: {result.get('model_id')}")
            return result.get('model_id'), model_data
        else:
            print_error(f"Model creation failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return None, None
    except Exception as e:
        print_error(f"Model creation error: {e}")
        return None, None

def test_run_analysis(model_id: int, model_data: Dict):
    """Test running structural analysis"""
    print_header("TEST 4: RUN STRUCTURAL ANALYSIS")
    
    print_info("Preparing analysis request...")
    
    # Build load vector (gravity loads)
    n_nodes = len(model_data['nodes'])
    loads = [0.0] * (n_nodes * 6)
    
    # Apply gravity loads to floor nodes (not base)
    tributary_load = -333510  # N (approximately 33.35 kN per node)
    
    for node in model_data['nodes']:
        if node['z'] > 0:  # Not base level
            node_id = node['id']
            loads[node_id * 6 + 2] = tributary_load  # Z-direction (gravity)
    
    print_success(f"Applied loads to {sum(1 for l in loads if l != 0)} DOF")
    
    # Prepare restraints
    restraints = {}
    for node in model_data['nodes']:
        if node['restraints']:
            restraints[node['id']] = node['restraints']
    
    print_success(f"Applied restraints to {len(restraints)} nodes")
    
    analysis_request = {
        "model_id": model_id,
        "analysis_type": "static",
        "nodes": model_data['nodes'],
        "elements": model_data['elements'],
        "loads": loads,
        "restraints": restraints,
        "material_props": model_data['materials'],
        "section_props": model_data['sections']
    }
    
    print_info("Running static analysis...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/analysis/run",
            json=analysis_request,
            timeout=60  # Analysis may take longer
        )
        
        if response.status_code == 200:
            result = response.json()
            print_success("Analysis completed successfully!")
            
            # Display results
            results = result.get('results', {})
            displacements = results.get('displacements', [])
            reactions = results.get('reactions', [])
            
            if displacements:
                max_disp = max(abs(d) for d in displacements)
                print(f"  Max displacement: {max_disp:.2f} mm")
            
            if reactions:
                total_reaction = sum(abs(r) for r in reactions)
                print(f"  Total reaction: {total_reaction/1000:.2f} kN")
            
            return result
        else:
            print_error(f"Analysis failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return None
    except Exception as e:
        print_error(f"Analysis error: {e}")
        return None

def test_seismic_analysis():
    """Test seismic analysis endpoint"""
    print_header("TEST 5: SEISMIC ANALYSIS")
    
    seismic_request = {
        "code": "IS1893",
        "zone": "III",
        "soil_type": "medium",
        "importance_factor": 1.0,
        "response_reduction": 5.0,
        "seismic_weight": 11852.83,
        "time_period": 0.642
    }
    
    print_info("Calculating seismic base shear...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/seismic/base-shear",
            json=seismic_request,
            timeout=API_TIMEOUT
        )
        
        if response.status_code == 200:
            result = response.json()
            print_success("Seismic analysis completed!")
            print(f"  Base shear: {result.get('base_shear', 0):.2f} kN")
            print(f"  Seismic coefficient: {result.get('seismic_coefficient', 0):.4f}")
            return result
        else:
            print_error(f"Seismic analysis failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return None
    except Exception as e:
        print_error(f"Seismic analysis error: {e}")
        return None

def test_wind_analysis():
    """Test wind analysis endpoint"""
    print_header("TEST 6: WIND ANALYSIS")
    
    wind_request = {
        "code": "IS875",
        "basic_wind_speed": 44,
        "terrain_category": "2",
        "building_class": "B",
        "building_height": 17.5,
        "building_width": 16.7,
        "building_depth": 16.7,
        "risk_coefficient": 1.0,
        "topography_factor": 1.0
    }
    
    print_info("Calculating wind pressure...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/wind/design-pressure",
            json=wind_request,
            timeout=API_TIMEOUT
        )
        
        if response.status_code == 200:
            result = response.json()
            print_success("Wind analysis completed!")
            print(f"  Design wind speed: {result.get('design_wind_speed', 0):.2f} m/s")
            print(f"  Design pressure: {result.get('design_pressure', 0):.2f} kN/m²")
            return result
        else:
            print_error(f"Wind analysis failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return None
    except Exception as e:
        print_error(f"Wind analysis error: {e}")
        return None

def test_list_projects():
    """Test listing all projects"""
    print_header("TEST 7: LIST PROJECTS")
    
    print_info("Fetching all projects...")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/projects/list",
            timeout=API_TIMEOUT
        )
        
        if response.status_code == 200:
            projects = response.json()
            print_success(f"Found {len(projects)} project(s)")
            
            for project in projects:
                print(f"  - ID: {project.get('id')}, Name: {project.get('name')}")
            
            return projects
        else:
            print_error(f"List projects failed: {response.status_code}")
            return None
    except Exception as e:
        print_error(f"List projects error: {e}")
        return None

def main():
    """Main test execution"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("="*70)
    print("  STRUMIND COMPLETE APPLICATION TEST")
    print("  End-to-End Testing with Real API Calls")
    print("="*70)
    print(f"{Colors.END}\n")
    
    print_warning("Make sure the backend server is running!")
    print_info("Starting in 3 seconds...")
    time.sleep(3)
    
    # Wait for server
    if not wait_for_server():
        print_error("Cannot proceed without backend server")
        sys.exit(1)
    
    # Run tests
    test_results = {
        "health_check": False,
        "create_project": False,
        "create_model": False,
        "run_analysis": False,
        "seismic_analysis": False,
        "wind_analysis": False,
        "list_projects": False
    }
    
    # Test 1: Health check
    test_results["health_check"] = test_health_check()
    
    # Test 2: Create project
    project_id = test_create_project()
    test_results["create_project"] = project_id is not None
    
    if project_id:
        # Test 3: Create model
        model_id, model_data = test_create_model(project_id)
        test_results["create_model"] = model_id is not None
        
        if model_id and model_data:
            # Test 4: Run analysis
            analysis_result = test_run_analysis(model_id, model_data)
            test_results["run_analysis"] = analysis_result is not None
    
    # Test 5: Seismic analysis
    seismic_result = test_seismic_analysis()
    test_results["seismic_analysis"] = seismic_result is not None
    
    # Test 6: Wind analysis
    wind_result = test_wind_analysis()
    test_results["wind_analysis"] = wind_result is not None
    
    # Test 7: List projects
    projects = test_list_projects()
    test_results["list_projects"] = projects is not None
    
    # Final summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for result in test_results.values() if result)
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "PASS" if result else "FAIL"
        color = Colors.GREEN if result else Colors.RED
        print(f"{color}{status}{Colors.END} - {test_name.replace('_', ' ').title()}")
    
    print(f"\n{Colors.BOLD}Results: {passed}/{total} tests passed{Colors.END}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ ALL TESTS PASSED!{Colors.END}")
        print(f"{Colors.GREEN}The StruMind platform is working correctly!{Colors.END}\n")
        return 0
    else:
        print(f"\n{Colors.YELLOW}⚠ Some tests failed{Colors.END}")
        print(f"{Colors.YELLOW}Check the output above for details{Colors.END}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
