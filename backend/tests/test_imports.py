"""
Test that all critical imports work without errors
"""
import sys
import traceback

def test_imports():
    """Test all critical imports"""
    results = []
    
    # Test 1: Core imports
    try:
        from app.core.config import settings
        results.append(("✅ Config import", True, None))
    except Exception as e:
        results.append(("❌ Config import", False, str(e)))
    
    # Test 2: Security imports
    try:
        from app.core.security import get_password_hash, verify_password
        results.append(("✅ Security import", True, None))
    except Exception as e:
        results.append(("❌ Security import", False, str(e)))
    
    # Test 3: Database imports
    try:
        from app.core.database import init_db
        results.append(("✅ Database import", True, None))
    except Exception as e:
        results.append(("❌ Database import", False, str(e)))
    
    # Test 4: Main app import
    try:
        from main import app
        results.append(("✅ Main app import", True, None))
    except Exception as e:
        results.append(("❌ Main app import", False, str(e)))
    
    # Test 5: Auth API import
    try:
        from app.api.auth import router
        results.append(("✅ Auth API import", True, None))
    except Exception as e:
        results.append(("❌ Auth API import", False, str(e)))
    
    # Test 6: Security middleware import
    try:
        from app.core.security_middleware import SecurityHeadersMiddleware
        results.append(("✅ Security middleware import", True, None))
    except Exception as e:
        results.append(("❌ Security middleware import", False, str(e)))
    
    return results

if __name__ == "__main__":
    print("=" * 60)
    print("BACKEND IMPORT TESTS")
    print("=" * 60)
    print()
    
    results = test_imports()
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    for name, success, error in results:
        print(f"{name}")
        if error:
            print(f"  Error: {error}")
    
    print()
    print("=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("✅ All imports successful!")
        sys.exit(0)
    else:
        print("❌ Some imports failed!")
        sys.exit(1)
