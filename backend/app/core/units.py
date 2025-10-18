"""
Unit system management and conversion utilities
Supports SI, SI_mm, and Imperial unit systems
"""
from enum import Enum
from typing import Dict, Tuple, Optional
from .errors import UnitConversionError, InconsistentUnitsError


class UnitSystem(str, Enum):
    """Supported unit systems"""
    SI = "SI"  # meters, Newtons, Pascals
    SI_MM = "SI_mm"  # millimeters, Newtons, MPa (most common for structural)
    IMPERIAL = "Imperial"  # inches, pounds, psi


class LengthUnit(str, Enum):
    """Length units"""
    M = "m"
    MM = "mm"
    CM = "cm"
    IN = "in"
    FT = "ft"


class ForceUnit(str, Enum):
    """Force units"""
    N = "N"
    KN = "kN"
    LB = "lb"
    KIP = "kip"


class StressUnit(str, Enum):
    """Stress/Pressure units"""
    PA = "Pa"
    KPA = "kPa"
    MPA = "MPa"
    GPA = "GPa"
    PSI = "psi"
    KSI = "ksi"


class MassUnit(str, Enum):
    """Mass units"""
    KG = "kg"
    TONNE = "tonne"
    LB = "lb"


class UnitSystemDefinition:
    """Definition of a unit system"""
    
    SYSTEMS = {
        UnitSystem.SI: {
            'length': LengthUnit.M,
            'force': ForceUnit.N,
            'stress': StressUnit.PA,
            'mass': MassUnit.KG,
            'description': 'SI (meters, Newtons, Pascals)'
        },
        UnitSystem.SI_MM: {
            'length': LengthUnit.MM,
            'force': ForceUnit.N,
            'stress': StressUnit.MPA,
            'mass': MassUnit.KG,
            'description': 'SI with mm (millimeters, Newtons, MPa)'
        },
        UnitSystem.IMPERIAL: {
            'length': LengthUnit.IN,
            'force': ForceUnit.LB,
            'stress': StressUnit.PSI,
            'mass': MassUnit.LB,
            'description': 'Imperial (inches, pounds, psi)'
        }
    }
    
    @classmethod
    def get_system(cls, system: UnitSystem) -> Dict:
        """Get unit system definition"""
        return cls.SYSTEMS.get(system, cls.SYSTEMS[UnitSystem.SI_MM])


class UnitConverter:
    """Unit conversion utilities"""
    
    # Conversion factors to base units (SI: m, N, Pa, kg)
    LENGTH_TO_M = {
        LengthUnit.M: 1.0,
        LengthUnit.MM: 0.001,
        LengthUnit.CM: 0.01,
        LengthUnit.IN: 0.0254,
        LengthUnit.FT: 0.3048,
    }
    
    FORCE_TO_N = {
        ForceUnit.N: 1.0,
        ForceUnit.KN: 1000.0,
        ForceUnit.LB: 4.44822,
        ForceUnit.KIP: 4448.22,
    }
    
    STRESS_TO_PA = {
        StressUnit.PA: 1.0,
        StressUnit.KPA: 1e3,
        StressUnit.MPA: 1e6,
        StressUnit.GPA: 1e9,
        StressUnit.PSI: 6894.76,
        StressUnit.KSI: 6.89476e6,
    }
    
    MASS_TO_KG = {
        MassUnit.KG: 1.0,
        MassUnit.TONNE: 1000.0,
        MassUnit.LB: 0.453592,
    }
    
    @classmethod
    def convert_length(cls, value: float, from_unit: LengthUnit, to_unit: LengthUnit) -> float:
        """Convert length between units"""
        if from_unit == to_unit:
            return value
        
        if from_unit not in cls.LENGTH_TO_M or to_unit not in cls.LENGTH_TO_M:
            raise UnitConversionError(from_unit, to_unit)
        
        # Convert to meters, then to target unit
        value_in_m = value * cls.LENGTH_TO_M[from_unit]
        return value_in_m / cls.LENGTH_TO_M[to_unit]
    
    @classmethod
    def convert_force(cls, value: float, from_unit: ForceUnit, to_unit: ForceUnit) -> float:
        """Convert force between units"""
        if from_unit == to_unit:
            return value
        
        if from_unit not in cls.FORCE_TO_N or to_unit not in cls.FORCE_TO_N:
            raise UnitConversionError(from_unit, to_unit)
        
        # Convert to Newtons, then to target unit
        value_in_n = value * cls.FORCE_TO_N[from_unit]
        return value_in_n / cls.FORCE_TO_N[to_unit]
    
    @classmethod
    def convert_stress(cls, value: float, from_unit: StressUnit, to_unit: StressUnit) -> float:
        """Convert stress/pressure between units"""
        if from_unit == to_unit:
            return value
        
        if from_unit not in cls.STRESS_TO_PA or to_unit not in cls.STRESS_TO_PA:
            raise UnitConversionError(from_unit, to_unit)
        
        # Convert to Pascals, then to target unit
        value_in_pa = value * cls.STRESS_TO_PA[from_unit]
        return value_in_pa / cls.STRESS_TO_PA[to_unit]
    
    @classmethod
    def convert_mass(cls, value: float, from_unit: MassUnit, to_unit: MassUnit) -> float:
        """Convert mass between units"""
        if from_unit == to_unit:
            return value
        
        if from_unit not in cls.MASS_TO_KG or to_unit not in cls.MASS_TO_KG:
            raise UnitConversionError(from_unit, to_unit)
        
        # Convert to kg, then to target unit
        value_in_kg = value * cls.MASS_TO_KG[from_unit]
        return value_in_kg / cls.MASS_TO_KG[to_unit]
    
    @classmethod
    def convert_moment(cls, value: float, from_length: LengthUnit, from_force: ForceUnit,
                      to_length: LengthUnit, to_force: ForceUnit) -> float:
        """Convert moment (force × length)"""
        # Convert force
        value = cls.convert_force(value, from_force, to_force)
        # Convert length
        value = cls.convert_length(value, from_length, to_length)
        return value
    
    @classmethod
    def convert_area(cls, value: float, from_unit: LengthUnit, to_unit: LengthUnit) -> float:
        """Convert area (length²)"""
        conversion_factor = cls.LENGTH_TO_M[from_unit] / cls.LENGTH_TO_M[to_unit]
        return value * (conversion_factor ** 2)
    
    @classmethod
    def convert_moment_of_inertia(cls, value: float, from_unit: LengthUnit, to_unit: LengthUnit) -> float:
        """Convert moment of inertia (length⁴)"""
        conversion_factor = cls.LENGTH_TO_M[from_unit] / cls.LENGTH_TO_M[to_unit]
        return value * (conversion_factor ** 4)


class ProjectUnits:
    """Manage units for a project"""
    
    def __init__(self, unit_system: UnitSystem = UnitSystem.SI_MM):
        self.system = unit_system
        self.definition = UnitSystemDefinition.get_system(unit_system)
        self.length_unit = self.definition['length']
        self.force_unit = self.definition['force']
        self.stress_unit = self.definition['stress']
        self.mass_unit = self.definition['mass']
    
    def get_display_units(self) -> Dict[str, str]:
        """Get display units for UI"""
        return {
            'length': self.length_unit,
            'force': self.force_unit,
            'stress': self.stress_unit,
            'mass': self.mass_unit,
            'moment': f"{self.force_unit}·{self.length_unit}",
            'area': f"{self.length_unit}²",
            'moment_of_inertia': f"{self.length_unit}⁴",
            'density': f"{self.mass_unit}/{self.length_unit}³"
        }
    
    def convert_to_system(self, value: float, quantity_type: str, 
                         from_unit: str) -> float:
        """Convert value to project unit system"""
        if quantity_type == 'length':
            return UnitConverter.convert_length(value, from_unit, self.length_unit)
        elif quantity_type == 'force':
            return UnitConverter.convert_force(value, from_unit, self.force_unit)
        elif quantity_type == 'stress':
            return UnitConverter.convert_stress(value, from_unit, self.stress_unit)
        elif quantity_type == 'mass':
            return UnitConverter.convert_mass(value, from_unit, self.mass_unit)
        else:
            raise ValueError(f"Unknown quantity type: {quantity_type}")
    
    def format_value(self, value: float, quantity_type: str, decimals: int = 2) -> str:
        """Format value with units for display"""
        units = self.get_display_units()
        unit_str = units.get(quantity_type, "")
        return f"{value:.{decimals}f} {unit_str}"


# Common material properties in different unit systems
class MaterialProperties:
    """Standard material properties"""
    
    # Young's modulus (MPa for SI_mm, psi for Imperial)
    STEEL_E = {
        UnitSystem.SI_MM: 200000,  # MPa
        UnitSystem.SI: 200e9,  # Pa
        UnitSystem.IMPERIAL: 29e6,  # psi
    }
    
    CONCRETE_E = {
        UnitSystem.SI_MM: lambda fck: 5000 * (fck ** 0.5),  # MPa, IS 456
        UnitSystem.SI: lambda fck: 5000e6 * ((fck/1e6) ** 0.5),  # Pa
        UnitSystem.IMPERIAL: lambda fc: 57000 * ((fc) ** 0.5),  # psi, ACI 318
    }
    
    # Density (kg/m³ for SI, lb/in³ for Imperial)
    STEEL_DENSITY = {
        UnitSystem.SI_MM: 7850,  # kg/m³
        UnitSystem.SI: 7850,  # kg/m³
        UnitSystem.IMPERIAL: 0.284,  # lb/in³
    }
    
    CONCRETE_DENSITY = {
        UnitSystem.SI_MM: 2500,  # kg/m³
        UnitSystem.SI: 2500,  # kg/m³
        UnitSystem.IMPERIAL: 0.0868,  # lb/in³
    }
    
    # Poisson's ratio (dimensionless)
    STEEL_NU = 0.3
    CONCRETE_NU = 0.2
    
    @classmethod
    def get_steel_properties(cls, unit_system: UnitSystem) -> Dict:
        """Get steel material properties"""
        return {
            'E': cls.STEEL_E[unit_system],
            'nu': cls.STEEL_NU,
            'density': cls.STEEL_DENSITY[unit_system],
            'fy': 250 if unit_system != UnitSystem.IMPERIAL else 36000,  # MPa or psi
        }
    
    @classmethod
    def get_concrete_properties(cls, unit_system: UnitSystem, fck: float) -> Dict:
        """Get concrete material properties"""
        E_func = cls.CONCRETE_E[unit_system]
        E = E_func(fck) if callable(E_func) else E_func
        
        return {
            'E': E,
            'nu': cls.CONCRETE_NU,
            'density': cls.CONCRETE_DENSITY[unit_system],
            'fck': fck,
        }
