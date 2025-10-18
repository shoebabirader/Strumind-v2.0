"""
Test bcrypt functionality
"""
import sys

def test_bcrypt():
    """Test bcrypt password hashing"""
    results = []
    
    # Test 1: Import bcrypt
    try:
        import bcrypt
        version = bcrypt.__version__
        results.append(("✅ bcrypt import", True, f"Version: {version}"))
    except Exception as e:
        results.append(("❌ bcrypt import", False, str(e)))
        return results
    
    # Test 2: Import passlib
    try:
        from passlib.context import CryptContext
        results.append(("✅ passlib import", True, None))
    except Exception as e:
        results.append(("❌ passlib import", False, str(e)))
        return results
    
    # Test 3: Create password context
    try:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        results.append(("✅ CryptContext creation", True, None))
    except Exception as e:
        results.append(("❌ CryptContext creation", False, str(e)))
        return results
    
    # Test 4: Hash a password
    try:
        test_password = "test123"
        hashed = pwd_context.hash(test_password)
        results.append(("✅ Password hashing", True, f"Hash length: {len(hashed)}"))
    except Exception as e:
        results.append(("❌ Password hashing", False, str(e)))
        return results
    
    # Test 5: Verify password
    try:
        is_valid = pwd_context.verify(test_password, hashed)
        if is_valid:
            results.append(("✅ Password verification", True, "Correct password verified"))
        else:
            results.append(("❌ Password verification", False, "Verification failed"))
    except Exception as e:
        results.append(("❌ Password verification", False, str(e)))
    
    # Test 6: Reject wrong password
    try:
        is_valid = pwd_context.verify("wrong_password", hashed)
        if not is_valid:
            results.append(("✅ Wrong password rejection", True, "Wrong password rejected"))
        else:
            results.append(("❌ Wrong password rejection", False, "Wrong password accepted"))
    except Exception as e:
        results.append(("❌ Wrong password rejection", False, str(e)))
    
    return results

if __name__ == "__main__":
    print("=" * 60)
    print("BCRYPT FUNCTIONALITY TESTS")
    print("=" * 60)
    print()
    
    results = test_bcrypt()
    
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
        print("✅ All bcrypt tests passed!")
        sys.exit(0)
    else:
        print("❌ Some bcrypt tests failed!")
        sys.exit(1)
