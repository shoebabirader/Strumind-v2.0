"""
Test that the FastAPI app can start without errors
"""
import sys

def test_app_startup():
    """Test FastAPI app initialization"""
    results = []
    
    # Test 1: Import main app
    try:
        from main import app
        results.append(("✅ Import main app", True, None))
    except Exception as e:
        results.append(("❌ Import main app", False, str(e)))
        return results
    
    # Test 2: Check app type
    try:
        from fastapi import FastAPI
        if isinstance(app, FastAPI):
            results.append(("✅ App is FastAPI instance", True, None))
        else:
            results.append(("❌ App is FastAPI instance", False, f"Type: {type(app)}"))
    except Exception as e:
        results.append(("❌ App is FastAPI instance", False, str(e)))
    
    # Test 3: Check app has routes
    try:
        routes = [route.path for route in app.routes]
        if len(routes) > 0:
            results.append(("✅ App has routes", True, f"Routes: {len(routes)}"))
        else:
            results.append(("❌ App has routes", False, "No routes found"))
    except Exception as e:
        results.append(("❌ App has routes", False, str(e)))
    
    # Test 4: Check critical routes exist
    try:
        routes = [route.path for route in app.routes]
        critical_routes = ["/", "/health", "/api/auth/login", "/api/auth/register"]
        missing = [r for r in critical_routes if r not in routes]
        if not missing:
            results.append(("✅ Critical routes exist", True, None))
        else:
            results.append(("❌ Critical routes exist", False, f"Missing: {missing}"))
    except Exception as e:
        results.append(("❌ Critical routes exist", False, str(e)))
    
    # Test 5: Check middleware
    try:
        middleware_count = len(app.user_middleware)
        if middleware_count > 0:
            results.append(("✅ Middleware configured", True, f"Count: {middleware_count}"))
        else:
            results.append(("⚠️  Middleware configured", True, "No middleware (optional)"))
    except Exception as e:
        results.append(("❌ Middleware configured", False, str(e)))
    
    return results

if __name__ == "__main__":
    print("=" * 60)
    print("APP STARTUP TESTS")
    print("=" * 60)
    print()
    
    results = test_app_startup()
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    for name, success, info in results:
        print(f"{name}")
        if info:
            print(f"  {info}")
    
    print()
    print("=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("✅ All app startup tests passed!")
        sys.exit(0)
    else:
        print("❌ Some app startup tests failed!")
        sys.exit(1)
