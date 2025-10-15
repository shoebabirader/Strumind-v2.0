"""
Validation Test Suite - Benchmark Problems
Compares StruMind results with analytical solutions and industry software
"""
import numpy as np
import pytest
from app.engine.geometry import GeometryEngine, Node, Element
from app.engine.analysis import StructuralAnalysis

class TestValidationBenchmarks:
    """
    Comprehensive validation against known solutions
    
    References:
    - Timoshenko & Young: Theory of Structures
    - AISC Steel Construction Manual
    - Verification Manual for ETABS/SAP2000
    """
    
    def test_cantilever_beam_point_load(self):
        """
        Benchmark 1: Cantilever beam with point load at tip
        
        Analytical solution:
        - Deflection at tip: δ = PL³/(3EI)
        - Moment at fixed end: M = PL
        - Shear at fixed end: V = P
        """
        # Problem setup
        L = 5000  # mm
        P = 10000  # N (10 kN)
        E = 200000  # MPa
        I = 1e7  # mm⁴
        A = 5000  # mm²
        
        # Create geometry
        geo = GeometryEngine()
        geo.add_node(0, 0, 0, 0)  # Fixed end
        geo.add_node(1, L, 0, 0)  # Free end
        geo.add_element(0, [0, 1], "beam")
        
        # Create analysis
        analysis = StructuralAnalysis(geo)
        
        # Material and section properties
        material_props = {'default': {'E': E, 'G': E / 2.6}}
        section_props = {'default': {'A': A, 'Iy': I, 'Iz': I, 'J': I/2}}
        
        # Assemble stiffness
        analysis.assemble_stiffness_matrix(material_props, section_props)
        
        # Apply loads (point load at node 1, y-direction)
        n_dof = 2 * 6  # 2 nodes × 6 DOF
        loads = np.zeros(n_dof)
        loads[7] = -P  # Node 1, uy direction (downward)
        
        # Boundary conditions (node 0 fully fixed)
        restraints = {0: [True, True, True, True, True, True]}
        
        # Run analysis
        results = analysis.static_analysis(loads, restraints)
        
        # Analytical solution
        delta_analytical = (P * L**3) / (3 * E * I)
        
        # Get computed deflection at tip (node 1, uy)
        delta_computed = abs(results['displacements'][7])
        
        # Verify (within 1% tolerance)
        error = abs(delta_computed - delta_analytical) / delta_analytical
        print(f"\nBenchmark 1: Cantilever Beam")
        print(f"Analytical deflection: {delta_analytical:.4f} mm")
        print(f"Computed deflection: {delta_computed:.4f} mm")
        print(f"Error: {error*100:.2f}%")
        
        assert error < 0.01, f"Error {error*100:.2f}% exceeds 1% tolerance"
        
        # Verify moment at fixed end
        elem_forces = results['element_forces'][0]
        moment_computed = abs(elem_forces['node_1']['moment_z'])
        moment_analytical = P * L
        
        error_moment = abs(moment_computed - moment_analytical) / moment_analytical
        print(f"Analytical moment: {moment_analytical:.0f} Nmm")
        print(f"Computed moment: {moment_computed:.0f} Nmm")
        print(f"Error: {error_moment*100:.2f}%")
        
        assert error_moment < 0.01, f"Moment error {error_moment*100:.2f}% exceeds 1%"
    
    def test_simply_supported_beam_udl(self):
        """
        Benchmark 2: Simply supported beam with uniform distributed load
        
        Analytical solution:
        - Max deflection at center: δ = 5wL⁴/(384EI)
        - Max moment at center: M = wL²/8
        - Reactions: R = wL/2
        """
        # Problem setup
        L = 6000  # mm
        w = 5  # N/mm (5 kN/m)
        E = 200000  # MPa
        I = 2e7  # mm⁴
        A = 8000  # mm²
        
        # Create geometry (10 elements for better accuracy)
        geo = GeometryEngine()
        n_elem = 10
        for i in range(n_elem + 1):
            x = i * L / n_elem
            geo.add_node(i, x, 0, 0)
        
        for i in range(n_elem):
            geo.add_element(i, [i, i+1], "beam")
        
        # Create analysis
        analysis = StructuralAnalysis(geo)
        
        # Material and section properties
        material_props = {'default': {'E': E, 'G': E / 2.6}}
        section_props = {'default': {'A': A, 'Iy': I, 'Iz': I, 'J': I/2}}
        
        # Assemble stiffness
        analysis.assemble_stiffness_matrix(material_props, section_props)
        
        # Apply distributed load (convert to nodal loads)
        n_dof = (n_elem + 1) * 6
        loads = np.zeros(n_dof)
        
        # Nodal loads from UDL (using trapezoidal rule)
        load_per_node = w * (L / n_elem)
        for i in range(1, n_elem):
            loads[i * 6 + 1] = -load_per_node  # uy direction
        # End nodes get half
        loads[1] = -load_per_node / 2
        loads[n_elem * 6 + 1] = -load_per_node / 2
        
        # Boundary conditions (simply supported)
        restraints = {
            0: [False, True, True, False, False, False],  # Pin at left
            n_elem: [False, True, True, False, False, False]  # Roller at right
        }
        
        # Run analysis
        results = analysis.static_analysis(loads, restraints)
        
        # Analytical solution
        delta_analytical = (5 * w * L**4) / (384 * E * I)
        
        # Get computed deflection at center
        center_node = n_elem // 2
        delta_computed = abs(results['displacements'][center_node * 6 + 1])
        
        # Verify
        error = abs(delta_computed - delta_analytical) / delta_analytical
        print(f"\nBenchmark 2: Simply Supported Beam with UDL")
        print(f"Analytical deflection: {delta_analytical:.4f} mm")
        print(f"Computed deflection: {delta_computed:.4f} mm")
        print(f"Error: {error*100:.2f}%")
        
        # Allow 5% error due to discretization
        assert error < 0.05, f"Error {error*100:.2f}% exceeds 5% tolerance"
    
    def test_portal_frame(self):
        """
        Benchmark 3: Simple portal frame with horizontal load
        
        Tests:
        - 2D frame behavior
        - Moment distribution
        - Sway deflection
        """
        # Problem setup
        H = 4000  # mm (height)
        L = 6000  # mm (span)
        P = 50000  # N (50 kN horizontal load)
        E = 200000  # MPa
        
        # Column properties
        A_col = 10000  # mm²
        I_col = 5e7  # mm⁴
        
        # Beam properties
        A_beam = 12000  # mm²
        I_beam = 8e7  # mm⁴
        
        # Create geometry
        geo = GeometryEngine()
        geo.add_node(0, 0, 0, 0)      # Left base
        geo.add_node(1, L, 0, 0)      # Right base
        geo.add_node(2, 0, H, 0)      # Left top
        geo.add_node(3, L, H, 0)      # Right top
        
        # Elements
        geo.add_element(0, [0, 2], "column")  # Left column
        geo.add_element(1, [1, 3], "column")  # Right column
        geo.add_element(2, [2, 3], "beam")    # Top beam
        
        # Create analysis
        analysis = StructuralAnalysis(geo)
        
        # Material properties
        material_props = {'default': {'E': E, 'G': E / 2.6}}
        
        # Section properties (different for columns and beam)
        section_props = {
            0: {'A': A_col, 'Iy': I_col, 'Iz': I_col, 'J': I_col/2},
            1: {'A': A_col, 'Iy': I_col, 'Iz': I_col, 'J': I_col/2},
            2: {'A': A_beam, 'Iy': I_beam, 'Iz': I_beam, 'J': I_beam/2}
        }
        
        # Assemble stiffness
        analysis.assemble_stiffness_matrix(material_props, section_props)
        
        # Apply horizontal load at left top
        n_dof = 4 * 6
        loads = np.zeros(n_dof)
        loads[2 * 6] = P  # Node 2, ux direction
        
        # Boundary conditions (both bases fixed)
        restraints = {
            0: [True, True, True, True, True, True],
            1: [True, True, True, True, True, True]
        }
        
        # Run analysis
        results = analysis.static_analysis(loads, restraints)
        
        # Get sway deflection at top
        sway_left = results['displacements'][2 * 6]
        sway_right = results['displacements'][3 * 6]
        
        print(f"\nBenchmark 3: Portal Frame")
        print(f"Sway at left top: {sway_left:.4f} mm")
        print(f"Sway at right top: {sway_right:.4f} mm")
        
        # Verify both tops move together (rigid beam assumption)
        sway_diff = abs(sway_left - sway_right)
        assert sway_diff < 0.1, f"Sway difference {sway_diff:.4f} mm too large"
        
        # Verify positive sway (in direction of load)
        assert sway_left > 0, "Sway should be positive"
        
        # Verify reasonable magnitude (rough check)
        # For a portal frame, sway should be in range of PH³/(12EI) order
        expected_order = (P * H**3) / (12 * E * I_col)
        assert 0.1 * expected_order < sway_left < 10 * expected_order, \
            f"Sway {sway_left:.2f} mm outside expected range"
    
    def test_3d_frame_torsion(self):
        """
        Benchmark 4: 3D frame with torsional loading
        
        Tests:
        - 3D behavior
        - Torsional stiffness
        - Coordinate transformation
        """
        # Problem setup
        L = 5000  # mm
        T = 1e6  # Nmm (torsional moment)
        E = 200000  # MPa
        G = E / 2.6  # MPa
        
        # Section properties (square tube)
        A = 5000  # mm²
        I = 2e7  # mm⁴
        J = 3e7  # mm⁴ (torsion constant)
        
        # Create geometry (cantilever in 3D)
        geo = GeometryEngine()
        geo.add_node(0, 0, 0, 0)      # Fixed end
        geo.add_node(1, L, 0, 0)      # Free end
        geo.add_element(0, [0, 1], "beam")
        
        # Create analysis
        analysis = StructuralAnalysis(geo)
        
        # Properties
        material_props = {'default': {'E': E, 'G': G}}
        section_props = {'default': {'A': A, 'Iy': I, 'Iz': I, 'J': J}}
        
        # Assemble stiffness
        analysis.assemble_stiffness_matrix(material_props, section_props)
        
        # Apply torsional moment at free end
        n_dof = 2 * 6
        loads = np.zeros(n_dof)
        loads[9] = T  # Node 1, rx (torsion about x-axis)
        
        # Boundary conditions
        restraints = {0: [True, True, True, True, True, True]}
        
        # Run analysis
        results = analysis.static_analysis(loads, restraints)
        
        # Analytical solution for torsional rotation
        theta_analytical = (T * L) / (G * J)  # radians
        
        # Get computed rotation
        theta_computed = abs(results['displacements'][9])
        
        # Verify
        error = abs(theta_computed - theta_analytical) / theta_analytical
        print(f"\nBenchmark 4: 3D Frame with Torsion")
        print(f"Analytical rotation: {theta_analytical:.6f} rad")
        print(f"Computed rotation: {theta_computed:.6f} rad")
        print(f"Error: {error*100:.2f}%")
        
        assert error < 0.01, f"Error {error*100:.2f}% exceeds 1% tolerance"
    
    def test_modal_analysis_cantilever(self):
        """
        Benchmark 5: Modal analysis of cantilever beam
        
        Analytical solution for first natural frequency:
        f₁ = (λ₁²/2π) × √(EI/mL⁴)
        where λ₁ = 1.875 for cantilever
        """
        # Problem setup
        L = 5000  # mm
        E = 200000  # MPa = 200000 N/mm²
        I = 1e7  # mm⁴
        A = 5000  # mm²
        rho = 7850e-9  # kg/mm³ (steel: 7850 kg/m³)
        
        # Create geometry
        geo = GeometryEngine()
        n_elem = 10
        for i in range(n_elem + 1):
            x = i * L / n_elem
            geo.add_node(i, x, 0, 0)
        
        for i in range(n_elem):
            geo.add_element(i, [i, i+1], "beam")
        
        # Create analysis
        analysis = StructuralAnalysis(geo)
        
        # Properties
        material_props = {'default': {'E': E, 'G': E/2.6, 'density': rho}}
        section_props = {'default': {'A': A, 'Iy': I, 'Iz': I, 'J': I/2}}
        
        # Assemble matrices
        analysis.assemble_stiffness_matrix(material_props, section_props)
        
        # Boundary conditions
        restraints = {0: [True, True, True, True, True, True]}
        
        # Run modal analysis
        modal_results = analysis.modal_analysis(
            material_props, section_props, restraints, n_modes=3
        )
        
        # Analytical solution for first frequency
        m = rho * A  # mass per unit length (kg/mm)
        lambda1 = 1.875
        f1_analytical = (lambda1**2 / (2 * np.pi)) * np.sqrt((E * I) / (m * L**4))
        
        # Get computed first frequency
        f1_computed = modal_results['frequencies'][0]
        
        # Verify
        error = abs(f1_computed - f1_analytical) / f1_analytical
        print(f"\nBenchmark 5: Modal Analysis")
        print(f"Analytical frequency: {f1_analytical:.4f} Hz")
        print(f"Computed frequency: {f1_computed:.4f} Hz")
        print(f"Error: {error*100:.2f}%")
        
        # Allow 10% error due to discretization
        assert error < 0.10, f"Error {error*100:.2f}% exceeds 10% tolerance"
        
        # Verify frequencies are in ascending order
        freqs = modal_results['frequencies']
        assert all(freqs[i] < freqs[i+1] for i in range(len(freqs)-1)), \
            "Frequencies should be in ascending order"


def run_all_benchmarks():
    """Run all validation benchmarks and generate report"""
    print("="*70)
    print("STRUMIND VALIDATION SUITE - BENCHMARK PROBLEMS")
    print("="*70)
    
    test = TestValidationBenchmarks()
    
    benchmarks = [
        ("Cantilever Beam - Point Load", test.test_cantilever_beam_point_load),
        ("Simply Supported Beam - UDL", test.test_simply_supported_beam_udl),
        ("Portal Frame - Horizontal Load", test.test_portal_frame),
        ("3D Frame - Torsion", test.test_3d_frame_torsion),
        ("Modal Analysis - Cantilever", test.test_modal_analysis_cantilever)
    ]
    
    results = []
    for name, test_func in benchmarks:
        try:
            test_func()
            results.append((name, "PASS", None))
        except AssertionError as e:
            results.append((name, "FAIL", str(e)))
        except Exception as e:
            results.append((name, "ERROR", str(e)))
    
    # Print summary
    print("\n" + "="*70)
    print("VALIDATION SUMMARY")
    print("="*70)
    
    for name, status, error in results:
        symbol = "✅" if status == "PASS" else "❌"
        print(f"{symbol} {name}: {status}")
        if error:
            print(f"   Error: {error}")
    
    # Overall result
    passed = sum(1 for _, status, _ in results if status == "PASS")
    total = len(results)
    
    print(f"\n{passed}/{total} benchmarks passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL VALIDATION BENCHMARKS PASSED!")
        print("✅ Solver is accurate and ready for production use")
    else:
        print(f"\n⚠️  {total - passed} benchmark(s) failed")
        print("❌ Solver needs more work before production use")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_benchmarks()
    exit(0 if success else 1)
