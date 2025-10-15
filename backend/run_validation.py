"""
Simple validation runner - tests the fixed solver
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
from app.engine.geometry import GeometryEngine
from app.engine.analysis import StructuralAnalysis

def test_cantilever_beam():
    """Test 1: Cantilever beam with point load"""
    print("\n" + "="*70)
    print("TEST 1: CANTILEVER BEAM WITH POINT LOAD")
    print("="*70)
    
    # Problem setup
    L = 5000  # mm
    P = 10000  # N
    E = 200000  # MPa
    I = 1e7  # mm⁴
    A = 5000  # mm²
    
    # Analytical solution
    delta_analytical = (P * L**3) / (3 * E * I)
    moment_analytical = P * L
    
    print(f"\nProblem:")
    print(f"  Length: {L} mm")
    print(f"  Load: {P/1000} kN at tip")
    print(f"  E: {E} MPa, I: {I} mm⁴")
    
    print(f"\nAnalytical Solution:")
    print(f"  Deflection: {delta_analytical:.4f} mm")
    print(f"  Moment: {moment_analytical/1e6:.2f} kNm")
    
    try:
        # Create geometry
        geo = GeometryEngine()
        geo.add_node(0, 0, 0, 0)
        geo.add_node(1, L, 0, 0)
        geo.add_element(0, [0, 1], "beam")
        
        # Set boundary conditions
        geo.nodes[0].set_fixed()
        
        # Apply load
        geo.nodes[1].apply_load(fy=-P)
        
        # Create analysis
        analysis = StructuralAnalysis(geo)
        
        # Assemble stiffness
        analysis.assemble_stiffness_matrix(geo.materials, geo.sections)
        
        # Get loads and restraints
        loads = geo.get_load_vector()
        restraints = geo.get_restraints_dict()
        
        # Run analysis
        results = analysis.static_analysis(loads, restraints)
        
        # Get results
        delta_computed = abs(results['displacements'][7])  # Node 1, uy
        
        print(f"\nStruMind Results:")
        print(f"  Deflection: {delta_computed:.4f} mm")
        
        # Calculate error
        error = abs(delta_computed - delta_analytical) / delta_analytical * 100
        print(f"  Error: {error:.2f}%")
        
        if error < 1.0:
            print(f"\n✅ TEST PASSED (Error < 1%)")
            return True
        else:
            print(f"\n❌ TEST FAILED (Error {error:.2f}% > 1%)")
            return False
            
    except Exception as e:
        print(f"\n❌ TEST ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_simply_supported_beam():
    """Test 2: Simply supported beam"""
    print("\n" + "="*70)
    print("TEST 2: SIMPLY SUPPORTED BEAM")
    print("="*70)
    
    # Problem setup
    L = 6000  # mm
    P = 20000  # N (point load at center)
    E = 200000  # MPa
    I = 2e7  # mm⁴
    A = 8000  # mm²
    
    # Analytical solution (point load at center)
    delta_analytical = (P * L**3) / (48 * E * I)
    
    print(f"\nProblem:")
    print(f"  Span: {L} mm")
    print(f"  Load: {P/1000} kN at center")
    print(f"  E: {E} MPa, I: {I} mm⁴")
    
    print(f"\nAnalytical Solution:")
    print(f"  Deflection: {delta_analytical:.4f} mm")
    
    try:
        # Create geometry (3 nodes for center load)
        geo = GeometryEngine()
        geo.add_node(0, 0, 0, 0)
        geo.add_node(1, L/2, 0, 0)
        geo.add_node(2, L, 0, 0)
        geo.add_element(0, [0, 1], "beam")
        geo.add_element(1, [1, 2], "beam")
        
        # Set boundary conditions (simply supported)
        # For 2D beam in xy-plane, need to restrain out-of-plane DOFs
        # Left support: pin (restrain ux, uy, uz, rx, ry, rz)
        geo.nodes[0].restraints = [True, True, True, True, True, True]
        # Middle node: restrain out-of-plane (uz, rx, ry)
        geo.nodes[1].restraints = [False, False, True, True, True, False]
        # Right support: roller (restrain uy, uz, rx, ry, rz, free in x)
        geo.nodes[2].restraints = [False, True, True, True, True, True]
        
        # Apply load at center
        geo.nodes[1].apply_load(fy=-P)
        
        # Create analysis
        analysis = StructuralAnalysis(geo)
        
        # Assemble stiffness
        analysis.assemble_stiffness_matrix(geo.materials, geo.sections)
        
        # Get loads and restraints
        loads = geo.get_load_vector()
        restraints = geo.get_restraints_dict()
        
        # Run analysis
        results = analysis.static_analysis(loads, restraints)
        
        # Get results
        delta_computed = abs(results['displacements'][7])  # Node 1, uy
        
        print(f"\nStruMind Results:")
        print(f"  Deflection: {delta_computed:.4f} mm")
        
        # Calculate error
        error = abs(delta_computed - delta_analytical) / delta_analytical * 100
        print(f"  Error: {error:.2f}%")
        
        if error < 5.0:  # Allow 5% for discretization
            print(f"\n✅ TEST PASSED (Error < 5%)")
            return True
        else:
            print(f"\n❌ TEST FAILED (Error {error:.2f}% > 5%)")
            return False
            
    except Exception as e:
        print(f"\n❌ TEST ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_3d_torsion():
    """Test 3: 3D beam with torsion"""
    print("\n" + "="*70)
    print("TEST 3: 3D BEAM WITH TORSION")
    print("="*70)
    
    # Problem setup
    L = 5000  # mm
    T = 1e6  # Nmm
    E = 200000  # MPa
    G = E / 2.6  # MPa
    J = 3e7  # mm⁴
    
    # Analytical solution
    theta_analytical = (T * L) / (G * J)
    
    print(f"\nProblem:")
    print(f"  Length: {L} mm")
    print(f"  Torque: {T/1e6} kNm")
    print(f"  G: {G:.0f} MPa, J: {J} mm⁴")
    
    print(f"\nAnalytical Solution:")
    print(f"  Rotation: {theta_analytical:.6f} rad")
    
    try:
        # Create geometry
        geo = GeometryEngine()
        geo.add_node(0, 0, 0, 0)
        geo.add_node(1, L, 0, 0)
        geo.add_element(0, [0, 1], "beam")
        
        # Set boundary conditions
        geo.nodes[0].set_fixed()
        
        # Apply torsional moment
        geo.nodes[1].apply_load(mx=T)
        
        # Create analysis
        analysis = StructuralAnalysis(geo)
        
        # Assemble stiffness
        analysis.assemble_stiffness_matrix(geo.materials, geo.sections)
        
        # Get loads and restraints
        loads = geo.get_load_vector()
        restraints = geo.get_restraints_dict()
        
        # Run analysis
        results = analysis.static_analysis(loads, restraints)
        
        # Get results
        theta_computed = abs(results['displacements'][9])  # Node 1, rx
        
        print(f"\nStruMind Results:")
        print(f"  Rotation: {theta_computed:.6f} rad")
        
        # Calculate error
        error = abs(theta_computed - theta_analytical) / theta_analytical * 100
        print(f"  Error: {error:.2f}%")
        
        if error < 1.0:
            print(f"\n✅ TEST PASSED (Error < 1%)")
            return True
        else:
            print(f"\n❌ TEST FAILED (Error {error:.2f}% > 1%)")
            return False
            
    except Exception as e:
        print(f"\n❌ TEST ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all validation tests"""
    print("\n" + "🚀 "*35)
    print("STRUMIND VALIDATION SUITE - CRITICAL FIXES VERIFICATION")
    print("🚀 "*35)
    
    tests = [
        ("Cantilever Beam", test_cantilever_beam),
        ("Simply Supported Beam", test_simply_supported_beam),
        ("3D Torsion", test_3d_torsion)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\n❌ {name} CRASHED: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*70)
    print("VALIDATION SUMMARY")
    print("="*70)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
    
    passed_count = sum(1 for _, p in results if p)
    total = len(results)
    
    print(f"\n📊 Results: {passed_count}/{total} tests passed ({passed_count/total*100:.0f}%)")
    
    if passed_count == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Solver is accurate and ready for production")
        print("✅ Critical issues have been fixed")
        print("✅ Results match analytical solutions")
    else:
        print(f"\n⚠️  {total - passed_count} test(s) failed")
        print("❌ More work needed")
    
    return passed_count == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
