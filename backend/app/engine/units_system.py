"""
Standardized unit system for structural analysis
Base units: meters (m), Newtons (N), Pascals (Pa), kilograms (kg)

This module provides utilities for converting between different unit systems
and ensuring dimensional consistency throughout the analysis engine.
"""

class UnitConverter:
    """
    Convert between different unit systems
    
    Base SI units:
    - Length: meters (m)
    - Force: Newtons (N)
    - Stress: Pascals (Pa)
    - Mass: kilograms (kg)
    """
    
    # Length conversions
    MM_TO_M = 1e-3
    M_TO_MM = 1e3
    CM_TO_M = 1e-2
    M_TO_CM = 1e2
    
    # Force conversions
    KN_TO_N = 1e3
    N_TO_KN = 1e-3
    
    # Stress conversions
    MPA_TO_PA = 1e6
    PA_TO_MPA = 1e-6
    GPA_TO_PA = 1e9
    PA_TO_GPA = 1e-9
    
    # Area conversions
    MM2_TO_M2 = 1e-6
    M2_TO_MM2 = 1e6
    CM2_TO_M2 = 1e-4
    M2_TO_CM2 = 1e4
    
    # Moment of inertia conversions
    MM4_TO_M4 = 1e-12
    M4_TO_MM4 = 1e12
    CM4_TO_M4 = 1e-8
    M4_TO_CM4 = 1e8
    
    # Density conversions
    KG_MM3_TO_KG_M3 = 1e9
    KG_M3_TO_KG_MM3 = 1e-9
    
    @staticmethod
    def standardize_material(E_MPa, nu, density_kg_m3, fy_MPa=None, fu_MPa=None):
        """
        Convert material properties to SI base units
        
        Args:
            E_MPa: Young's modulus in MPa
            nu: Poisson's ratio (dimensionless)
            density_kg_m3: Density in kg/m³
            fy_MPa: Yield stress in MPa (optional)
            fu_MPa: Ultimate stress in MPa (optional)
        
        Returns:
            dict: Material properties in SI base units
        """
        result = {
            'E': E_MPa * UnitConverter.MPA_TO_PA,  # Pa
            'nu': nu,  # dimensionless
            'density': density_kg_m3  # kg/m³
        }
        
        if fy_MPa is not None:
            result['fy'] = fy_MPa * UnitConverter.MPA_TO_PA  # Pa
        
        if fu_MPa is not None:
            result['fu'] = fu_MPa * UnitConverter.MPA_TO_PA  # Pa
        
        return result
    
    @staticmethod
    def standardize_section(A_mm2, Iy_mm4, Iz_mm4, J_mm4):
        """
        Convert section properties to SI base units
        
        Args:
            A_mm2: Cross-sectional area in mm²
            Iy_mm4: Moment of inertia about y-axis in mm⁴
            Iz_mm4: Moment of inertia about z-axis in mm⁴
            J_mm4: Torsional constant in mm⁴
        
        Returns:
            dict: Section properties in SI base units
        """
        return {
            'A': A_mm2 * UnitConverter.MM2_TO_M2,  # m²
            'Iy': Iy_mm4 * UnitConverter.MM4_TO_M4,  # m⁴
            'Iz': Iz_mm4 * UnitConverter.MM4_TO_M4,  # m⁴
            'J': J_mm4 * UnitConverter.MM4_TO_M4  # m⁴
        }
    
    @staticmethod
    def standardize_coordinates(x_mm, y_mm, z_mm):
        """
        Convert coordinates to meters
        
        Args:
            x_mm, y_mm, z_mm: Coordinates in millimeters
        
        Returns:
            tuple: Coordinates in meters (x_m, y_m, z_m)
        """
        return (
            x_mm * UnitConverter.MM_TO_M,
            y_mm * UnitConverter.MM_TO_M,
            z_mm * UnitConverter.MM_TO_M
        )
    
    @staticmethod
    def standardize_forces(fx_kN, fy_kN, fz_kN, mx_kNm=0, my_kNm=0, mz_kNm=0):
        """
        Convert forces and moments to SI base units
        
        Args:
            fx_kN, fy_kN, fz_kN: Forces in kN
            mx_kNm, my_kNm, mz_kNm: Moments in kN·m
        
        Returns:
            dict: Forces in N and moments in N·m
        """
        return {
            'fx': fx_kN * UnitConverter.KN_TO_N,  # N
            'fy': fy_kN * UnitConverter.KN_TO_N,  # N
            'fz': fz_kN * UnitConverter.KN_TO_N,  # N
            'mx': mx_kNm * UnitConverter.KN_TO_N,  # N·m (kN·m = 1000 N·m)
            'my': my_kNm * UnitConverter.KN_TO_N,  # N·m
            'mz': mz_kNm * UnitConverter.KN_TO_N  # N·m
        }
    
    @staticmethod
    def to_engineering_units(displacement_m=None, force_N=None, stress_Pa=None, moment_Nm=None):
        """
        Convert SI base units to common engineering units for display
        
        Args:
            displacement_m: Displacement in meters
            force_N: Force in Newtons
            stress_Pa: Stress in Pascals
            moment_Nm: Moment in Newton-meters
        
        Returns:
            dict: Values in engineering units (mm, kN, MPa, kN·m)
        """
        result = {}
        
        if displacement_m is not None:
            result['displacement_mm'] = displacement_m * UnitConverter.M_TO_MM
        
        if force_N is not None:
            result['force_kN'] = force_N * UnitConverter.N_TO_KN
        
        if stress_Pa is not None:
            result['stress_MPa'] = stress_Pa * UnitConverter.PA_TO_MPA
        
        if moment_Nm is not None:
            result['moment_kNm'] = moment_Nm * UnitConverter.N_TO_KN
        
        return result


# Standard material properties in SI units
STANDARD_MATERIALS = {
    'concrete_M25': {
        'E': 25000 * UnitConverter.MPA_TO_PA,  # 25 GPa
        'nu': 0.2,
        'density': 2500,  # kg/m³
        'fck': 25 * UnitConverter.MPA_TO_PA  # 25 MPa
    },
    'steel_Fe415': {
        'E': 200000 * UnitConverter.MPA_TO_PA,  # 200 GPa
        'nu': 0.3,
        'density': 7850,  # kg/m³
        'fy': 415 * UnitConverter.MPA_TO_PA,  # 415 MPa
        'fu': 500 * UnitConverter.MPA_TO_PA  # 500 MPa
    },
    'steel_Fe500': {
        'E': 200000 * UnitConverter.MPA_TO_PA,  # 200 GPa
        'nu': 0.3,
        'density': 7850,  # kg/m³
        'fy': 500 * UnitConverter.MPA_TO_PA,  # 500 MPa
        'fu': 545 * UnitConverter.MPA_TO_PA  # 545 MPa
    }
}
