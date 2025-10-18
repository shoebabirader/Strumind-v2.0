"""
Test security functions
"""
import sys

def test_security():
    """Test security module functions"""
    results = []
    
    # Test 1: Import security module
    try:
        from app.core.security import (
            get_password_hash,
            verify_password,
            create_access_token,
            decode_access_token
        )
        results.append(("✅ Security module import", True, None))
    except Exception as e:
        results.append(("❌ Security module import", False, str(e)))
        return results
    
    # Test 2: Hash password
    try:
        password = "demo123"
        hashed = get_password_hash(password)
        results.append(("✅ get_password_hash", True, f"Hash length: {len(hashed)}"))
    except Exception as e:
        results.append(("❌ get_password_hash", False, str(e)))
        return results
    
    # Test 3: Verify correct password
    try:
        is_valid = verify_password(password, hashed)
        if is_valid:
            results.append(("✅ verify_password (correct)", True, None))
        else:
            results.append(("❌ verify_password (correct)", False, "Verification failed"))
    except Exception as e:
        results.append(("❌ verify_password (correct)", False, str(e)))
    
    # Test 4: Reject wrong password
    try:
        is_valid = verify_password("wrong", hashed)
        if not is_valid:
            results.append(("✅ verify_password (wrong)", True, "Rejected correctly"))
        else:
            results.append(("❌ verify_password (wrong)", False, "Accepted wrong password"))
    except Exception as e:
        results.append(("❌ verify_password (wrong)", False, str(e)))
    
    # Test 5: Create JWT token
    try:
        token = create_access_token(data={"sub": "testuser", "user_id": 1})
        results.append(("✅ create_access_token", True, f"Token length: {len(token)}"))
    except Exception as e:
        results.append(("❌ create_access_token", False, str(e)))
        return results
    
    # Test 6: Decode JWT token
    try:
        token_data = decode_access_token(token)
        if token_data.username == "testuser":
            results.append(("✅ decode_access_token", True, f"Username: {token_data.username}"))
        else:
            results.append(("❌ decode_access_token", False, "Wrong username decoded"))
    except Exception as e:
        results.append(("❌ decode_access_token", False, str(e)))
    
    return results

if __name__ == "__main__":
    print("=" * 60)
    print("SECURITY FUNCTIONS TESTS")
    print("=" * 60)
    print()
    
    results = test_security()
    
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
        print("✅ All security tests passed!")
        sys.exit(0)
    else:
        print("❌ Some security tests failed!")
        sys.exit(1)
