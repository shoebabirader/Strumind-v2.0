"""
Run all backend tests
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_all_tests():
    """Run all test modules"""
    print("=" * 70)
    print(" " * 20 + "STRUMIND BACKEND TEST SUITE")
    print("=" * 70)
    print()
    
    test_modules = [
        ("Import Tests", "tests.test_imports"),
        ("Bcrypt Tests", "tests.test_bcrypt"),
        ("Security Tests", "tests.test_security"),
        ("App Startup Tests", "tests.test_app_startup"),
    ]
    
    all_results = []
    
    for test_name, module_name in test_modules:
        print(f"\n{'=' * 70}")
        print(f"Running: {test_name}")
        print('=' * 70)
        
        try:
            module = __import__(module_name, fromlist=['test'])
            # Get the main test function
            if hasattr(module, 'test_imports'):
                results = module.test_imports()
            elif hasattr(module, 'test_bcrypt'):
                results = module.test_bcrypt()
            elif hasattr(module, 'test_security'):
                results = module.test_security()
            elif hasattr(module, 'test_app_startup'):
                results = module.test_app_startup()
            else:
                results = []
            
            # Display results
            for name, success, info in results:
                print(f"{name}")
                if info:
                    print(f"  {info}")
            
            passed = sum(1 for _, success, _ in results if success)
            total = len(results)
            print(f"\n{test_name}: {passed}/{total} passed")
            
            all_results.extend(results)
            
        except Exception as e:
            print(f"❌ Failed to run {test_name}: {e}")
            import traceback
            traceback.print_exc()
            all_results.append((f"❌ {test_name}", False, str(e)))
    
    # Final summary
    print("\n" + "=" * 70)
    print(" " * 25 + "FINAL SUMMARY")
    print("=" * 70)
    
    total_passed = sum(1 for _, success, _ in all_results if success)
    total_tests = len(all_results)
    
    print(f"\nTotal Tests: {total_tests}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_tests - total_passed}")
    print(f"Success Rate: {(total_passed/total_tests*100):.1f}%")
    
    print("\n" + "=" * 70)
    
    if total_passed == total_tests:
        print("✅ ALL TESTS PASSED! Backend is ready to start.")
        print("=" * 70)
        print("\nYou can now safely restart the backend:")
        print("  cd backend")
        print("  python start.py")
        return 0
    else:
        print("❌ SOME TESTS FAILED! Please fix errors before starting.")
        print("=" * 70)
        return 1

if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
