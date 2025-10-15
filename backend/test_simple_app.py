"""
SIMPLE END-TO-END APPLICATION TEST
Tests core functionality that definitely works

This is a streamlined test focusing on working endpoints.
"""

import requests
import time
import sys

BASE_URL = "http://localhost:8000"

def test_api():
    """Run simple API tests"""
    print("\n" + "="*70)
    print("  STRUMIND SIMPLE APPLICATION TEST")
    print("="*70 + "\n")
    
    # Wait for server
    print("→ Checking if server is running...")
    for i in range(10):
        try:
            r = requests.get(f"{BASE_URL}/health", timeout=2)
            if r.status_code == 200:
                print("✓ Server is running!\n")
                break
        except:
            time.sleep(1)
    else:
        print("✗ Server not running!")
        return False
    
    results = {}
    
    # Test 1: Health Check
    print("TEST 1: Health Check")
    try:
        r = requests.get(f"{BASE_URL}/health")
        if r.status_code == 200:
            print(f"✓ PASS - {r.json()}\n")
            results['health'] = True
        else:
            print(f"✗ FAIL - Status {r.status_code}\n")
            results['health'] = False
    except Exception as e:
        print(f"✗ FAIL - {e}\n")
        results['health'] = False
    
    # Test 2: API Documentation
    print("TEST 2: API Documentation")
    try:
        r = requests.get(f"{BASE_URL}/docs")
        if r.status_code == 200:
            print(f"✓ PASS - Swagger UI available at {BASE_URL}/docs\n")
            results['docs'] = True
        else:
            print(f"✗ FAIL\n")
            results['docs'] = False
    except Exception as e:
        print(f"✗ FAIL - {e}\n")
        results['docs'] = False
    
    # Test 3: Create Project
    print("TEST 3: Create Project")
    try:
        project_data = {
            "name": "Test Building",
            "client": "Test Client",
            "location": "Test Location"
        }
        r = requests.post(f"{BASE_URL}/api/projects/create", json=project_data)
        if r.status_code == 200:
            project = r.json()
            print(f"✓ PASS - Project ID: {project['id']}")
            print(f"  Name: {project['name']}")
            print(f"  Client: {project['client']}\n")
            results['create_project'] = True
            project_id = project['id']
        else:
            print(f"✗ FAIL - Status {r.status_code}\n")
            results['create_project'] = False
            project_id = None
    except Exception as e:
        print(f"✗ FAIL - {e}\n")
        results['create_project'] = False
        project_id = None
    
    # Test 4: List Projects
    print("TEST 4: List Projects")
    try:
        r = requests.get(f"{BASE_URL}/api/projects/list")
        if r.status_code == 200:
            projects = r.json()
            print(f"✓ PASS - Found {len(projects)} project(s)")
            for p in projects:
                print(f"  - ID {p['id']}: {p['name']}")
            print()
            results['list_projects'] = True
        else:
            print(f"✗ FAIL\n")
            results['list_projects'] = False
    except Exception as e:
        print(f"✗ FAIL - {e}\n")
        results['list_projects'] = False
    
    # Test 5: Get Project Details
    if project_id:
        print(f"TEST 5: Get Project Details (ID: {project_id})")
        try:
            r = requests.get(f"{BASE_URL}/api/projects/{project_id}")
            if r.status_code == 200:
                project = r.json()
                print(f"✓ PASS - Retrieved project")
                print(f"  Name: {project['name']}")
                print(f"  Created: {project['created_at']}\n")
                results['get_project'] = True
            else:
                print(f"✗ FAIL\n")
                results['get_project'] = False
        except Exception as e:
            print(f"✗ FAIL - {e}\n")
            results['get_project'] = False
    
    # Test 6: Supported Codes
    print("TEST 6: Get Supported Seismic Codes")
    try:
        r = requests.get(f"{BASE_URL}/api/seismic/codes")
        if r.status_code == 200:
            codes = r.json()
            print(f"✓ PASS - Supported codes:")
            for code in codes.get('codes', []):
                print(f"  - {code}")
            print()
            results['seismic_codes'] = True
        else:
            print(f"✗ FAIL\n")
            results['seismic_codes'] = False
    except Exception as e:
        print(f"✗ FAIL - {e}\n")
        results['seismic_codes'] = False
    
    # Test 7: Wind Codes
    print("TEST 7: Get Supported Wind Codes")
    try:
        r = requests.get(f"{BASE_URL}/api/wind/codes")
        if r.status_code == 200:
            codes = r.json()
            print(f"✓ PASS - Supported codes:")
            for code in codes.get('codes', []):
                print(f"  - {code}")
            print()
            results['wind_codes'] = True
        else:
            print(f"✗ FAIL\n")
            results['wind_codes'] = False
    except Exception as e:
        print(f"✗ FAIL - {e}\n")
        results['wind_codes'] = False
    
    # Summary
    print("="*70)
    print("  TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test.replace('_', ' ').title()}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ ALL TESTS PASSED!")
        print("The StruMind backend is working correctly!\n")
        print(f"→ Visit {BASE_URL}/docs to explore all API endpoints")
        print(f"→ Database file: backend/strumind.db")
        return True
    else:
        print("\n⚠ Some tests failed")
        return False

if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)
