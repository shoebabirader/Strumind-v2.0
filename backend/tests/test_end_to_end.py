"""
End-to-End Testing Script for StruMind
Tests complete workflow: Model → Analyze → Design
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_health():
    """Test if backend is running"""
    print_section("1. Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Backend is healthy:", response.json())
            return True
        else:
            print("❌ Backend health check failed")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        return False

def test_slab_design():
    """Test slab design endpoint"""
    print_section("2. Slab Design Test")
    
    data = {
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
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/advanced-analysis/slab-design",
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Slab design successful!")
            print(f"   X-direction steel: {result['results']['x_direction_steel']['designation']}")
            print(f"   Y-direction steel: {result['results']['y_direction_steel']['designation']}")
            print(f"   Status: {result['results']['status']}")
            return True
        else:
            print(f"❌ Slab design failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_shear_wall_design():
    """Test shear wall design endpoint"""
    print_section("3. Shear Wall Design Test")
    
    data = {
        "height": 12000,
        "length": 4000,
        "thickness": 250,
        "axial_load": 2000,
        "shear_force": 500,
        "moment": 3000,
        "boundary_element": True
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/specialized-design/shear-wall",
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Shear wall design successful!")
            print(f"   Classification: {result['results']['classification']}")
            print(f"   Status: {result['results'].get('overall_status', 'OK')}")
            return True
        else:
            print(f"❌ Shear wall design failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_deflection_check():
    """Test deflection serviceability check"""
    print_section("4. Deflection Check Test")
    
    data = {
        "span": 6000,
        "actual_deflection": 15,
        "member_type": "beam",
        "support_condition": "simply_supported",
        "loading_type": "live"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/serviceability/deflection",
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Deflection check successful!")
            print(f"   Allowable: {result['results']['allowable_deflection']:.2f} mm")
            print(f"   Actual: {result['results']['actual_deflection']:.2f} mm")
            print(f"   Utilization: {result['results']['utilization']:.1f}%")
            print(f"   Status: {result['results']['status']}")
            return True
        else:
            print(f"❌ Deflection check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_steel_sections():
    """Test steel sections database"""
    print_section("5. Steel Sections Database Test")
    
    try:
        response = requests.get(f"{BASE_URL}/api/advanced-analysis/steel-sections/AISC?section_type=W")
        
        if response.status_code == 200:
            result = response.json()
            sections = result['sections']
            print(f"✅ Retrieved {len(sections)} AISC W sections")
            if sections:
                print(f"   Example: {sections[0]['designation']}")
                print(f"   Area: {sections[0]['area']} mm²")
            return True
        else:
            print(f"❌ Steel sections query failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_moving_load():
    """Test moving load analysis"""
    print_section("6. Moving Load Analysis Test")
    
    data = {
        "span": 30,
        "response_type": "moment",
        "location": 15,
        "loading_standard": "IRC_Class_A"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/specialized-design/moving-load",
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Moving load analysis successful!")
            print(f"   Max response: {result['results']['max_response']:.2f} kNm")
            print(f"   Critical position: {result['results']['critical_position']:.2f} m")
            return True
        else:
            print(f"❌ Moving load analysis failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_temperature_analysis():
    """Test temperature analysis"""
    print_section("7. Temperature Analysis Test")
    
    data = {
        "analysis_type": "uniform",
        "delta_T": 30,
        "material": "concrete",
        "length": 50000,
        "area": 300000,
        "restraint": "fixed"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/specialized-design/temperature-analysis",
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Temperature analysis successful!")
            print(f"   Thermal stress: {result['results']['thermal_stress']:.2f} MPa")
            print(f"   Thermal force: {result['results']['thermal_force']:.2f} kN")
            return True
        else:
            print(f"❌ Temperature analysis failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_mesh_generation():
    """Test mesh generation"""
    print_section("8. Mesh Generation Test")
    
    data = {
        "mesh_type": "rectangle",
        "width": 5000,
        "height": 3000,
        "nx": 10,
        "ny": 6,
        "element_type": "quad4"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/specialized-design/mesh/generate",
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Mesh generation successful!")
            print(f"   Nodes: {result['results']['n_nodes']}")
            print(f"   Elements: {result['results']['n_elements']}")
            return True
        else:
            print(f"❌ Mesh generation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def run_all_tests():
    """Run all end-to-end tests"""
    print("\n" + "🚀 "*30)
    print("  StruMind End-to-End Testing")
    print("🚀 "*30)
    
    tests = [
        ("Health Check", test_health),
        ("Slab Design", test_slab_design),
        ("Shear Wall Design", test_shear_wall_design),
        ("Deflection Check", test_deflection_check),
        ("Steel Sections", test_steel_sections),
        ("Moving Load", test_moving_load),
        ("Temperature Analysis", test_temperature_analysis),
        ("Mesh Generation", test_mesh_generation),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
            time.sleep(0.5)  # Small delay between tests
        except Exception as e:
            print(f"❌ Test '{name}' crashed: {e}")
            results.append((name, False))
    
    # Summary
    print_section("Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 All tests passed! StruMind is working perfectly!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
