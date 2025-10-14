"""
Steel Section Database
AISC, Indian (IS), European, British sections
"""
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class SteelSection:
    """Steel section properties"""
    designation: str
    standard: str  # AISC, IS, BS, EU
    type: str  # W, S, C, L, HSS, ISMB, ISMC, IPE, HE, UB, UC
    depth: float  # mm
    width: float  # mm
    web_thickness: float  # mm
    flange_thickness: float  # mm
    area: float  # mm²
    weight: float  # kg/m
    Ixx: float  # mm⁴
    Iyy: float  # mm⁴
    Zxx: float  # mm³
    Zyy: float  # mm³
    rxx: float  # mm
    ryy: float  # mm

class SteelSectionDatabase:
    """Database of standard steel sections"""
    
    def __init__(self):
        self.sections: Dict[str, List[SteelSection]] = {
            'AISC': self._load_aisc_sections(),
            'IS': self._load_indian_sections(),
            'BS': self._load_british_sections(),
            'EU': self._load_european_sections()
        }
    
    def _load_aisc_sections(self) -> List[SteelSection]:
        """Load AISC W-shapes"""
        return [
            SteelSection(
                designation="W36X300",
                standard="AISC",
                type="W",
                depth=914.4,
                width=406.4,
                web_thickness=19.1,
                flange_thickness=38.1,
                area=57000,
                weight=447,
                Ixx=2.04e9,
                Iyy=4.42e8,
                Zxx=4.87e6,
                Zyy=2.44e6,
                rxx=377,
                ryy=139
            ),
            SteelSection(
                designation="W24X84",
                standard="AISC",
                type="W",
                depth=609.6,
                width=228.6,
                web_thickness=11.2,
                flange_thickness=17.3,
                area=15900,
                weight=125,
                Ixx=4.42e8,
                Iyy=5.53e7,
                Zxx=1.58e6,
                Zyy=5.08e5,
                rxx=253,
                ryy=59
            ),
            SteelSection(
                designation="W18X50",
                standard="AISC",
                type="W",
                depth=457.2,
                width=190.5,
                web_thickness=9.1,
                flange_thickness=14.2,
                area=9480,
                weight=74.4,
                Ixx=1.80e8,
                Iyy=3.83e7,
                Zxx=8.89e5,
                Zyy=4.26e5,
                rxx=184,
                ryy=64
            ),
            SteelSection(
                designation="W14X43",
                standard="AISC",
                type="W",
                depth=347.5,
                width=203.2,
                web_thickness=8.1,
                flange_thickness=13.0,
                area=8130,
                weight=63.8,
                Ixx=1.10e8,
                Iyy=3.68e7,
                Zxx=6.89e5,
                Zyy=3.93e5,
                rxx=146,
                ryy=67
            ),
            SteelSection(
                designation="W12X26",
                standard="AISC",
                type="W",
                depth=304.8,
                width=165.1,
                web_thickness=6.4,
                flange_thickness=9.9,
                area=4970,
                weight=39.0,
                Ixx=4.42e7,
                Iyy=1.47e7,
                Zxx=3.11e5,
                Zyy=1.93e5,
                rxx=94,
                ryy=54
            )
        ]
    
    def _load_indian_sections(self) -> List[SteelSection]:
        """Load Indian Standard sections (ISMB, ISMC, etc.)"""
        return [
            SteelSection(
                designation="ISMB 600",
                standard="IS",
                type="ISMB",
                depth=600,
                width=210,
                web_thickness=12.0,
                flange_thickness=20.8,
                area=15600,
                weight=122.6,
                Ixx=9.13e8,
                Iyy=3.70e7,
                Zxx=3.04e6,
                Zyy=3.52e5,
                rxx=242,
                ryy=49
            ),
            SteelSection(
                designation="ISMB 450",
                standard="IS",
                type="ISMB",
                depth=450,
                width=150,
                web_thickness=9.4,
                flange_thickness=17.4,
                area=9840,
                weight=77.2,
                Ixx=3.57e8,
                Iyy=1.26e7,
                Zxx=1.59e6,
                Zyy=1.68e5,
                rxx=191,
                ryy=36
            ),
            SteelSection(
                designation="ISMB 300",
                standard="IS",
                type="ISMB",
                depth=300,
                width=140,
                web_thickness=7.5,
                flange_thickness=12.4,
                area=5626,
                weight=44.2,
                Ixx=8.60e7,
                Iyy=6.41e6,
                Zxx=5.73e5,
                Zyy=9.16e4,
                rxx=124,
                ryy=34
            ),
            SteelSection(
                designation="ISMC 400",
                standard="IS",
                type="ISMC",
                depth=400,
                width=100,
                web_thickness=8.8,
                flange_thickness=15.3,
                area=6110,
                weight=48.0,
                Ixx=1.37e8,
                Iyy=3.74e6,
                Zxx=6.87e5,
                Zyy=7.48e4,
                rxx=150,
                ryy=25
            ),
            SteelSection(
                designation="ISMC 250",
                standard="IS",
                type="ISMC",
                depth=250,
                width=80,
                web_thickness=6.1,
                flange_thickness=11.5,
                area=3531,
                weight=27.7,
                Ixx=3.63e7,
                Iyy=1.53e6,
                Zxx=2.90e5,
                Zyy=3.82e4,
                rxx=101,
                ryy=21
            )
        ]
    
    def _load_british_sections(self) -> List[SteelSection]:
        """Load British Standard sections (UB, UC)"""
        return [
            SteelSection(
                designation="UB 914x419x388",
                standard="BS",
                type="UB",
                depth=920.5,
                width=420.5,
                web_thickness=21.4,
                flange_thickness=36.6,
                area=49400,
                weight=388,
                Ixx=2.54e9,
                Iyy=5.54e8,
                Zxx=6.28e6,
                Zyy=2.87e6,
                rxx=372,
                ryy=149
            ),
            SteelSection(
                designation="UB 533x210x92",
                standard="BS",
                type="UB",
                depth=533.1,
                width=209.3,
                web_thickness=10.1,
                flange_thickness=15.6,
                area=11700,
                weight=92,
                Ixx=3.55e8,
                Iyy=3.69e7,
                Zxx=1.40e6,
                Zyy=3.77e5,
                rxx=219,
                ryy=56
            ),
            SteelSection(
                designation="UC 356x406x634",
                standard="BS",
                type="UC",
                depth=474.6,
                width=424.0,
                web_thickness=47.6,
                flange_thickness=77.0,
                area=80800,
                weight=634,
                Ixx=2.69e9,
                Iyy=1.34e9,
                Zxx=1.24e7,
                Zyy=6.87e6,
                rxx=407,
                ryy=257
            )
        ]
    
    def _load_european_sections(self) -> List[SteelSection]:
        """Load European sections (IPE, HE)"""
        return [
            SteelSection(
                designation="IPE 600",
                standard="EU",
                type="IPE",
                depth=600,
                width=220,
                web_thickness=12.0,
                flange_thickness=19.0,
                area=15600,
                weight=122,
                Ixx=9.20e8,
                Iyy=3.39e7,
                Zxx=3.07e6,
                Zyy=3.08e5,
                rxx=243,
                ryy=47
            ),
            SteelSection(
                designation="HE 300 B",
                standard="EU",
                type="HE",
                depth=300,
                width=300,
                web_thickness=11.0,
                flange_thickness=19.0,
                area=14900,
                weight=117,
                Ixx=2.52e8,
                Iyy=8.56e7,
                Zxx=1.68e6,
                Zyy=5.71e5,
                rxx=130,
                ryy=76
            ),
            SteelSection(
                designation="IPE 400",
                standard="EU",
                type="IPE",
                depth=400,
                width=180,
                web_thickness=8.6,
                flange_thickness=13.5,
                area=8450,
                weight=66.3,
                Ixx=2.31e8,
                Iyy=1.32e7,
                Zxx=1.16e6,
                Zyy=1.46e5,
                rxx=165,
                ryy=39
            )
        ]
    
    def search_sections(self, standard: str, min_depth: float = 0,
                       max_depth: float = 10000, section_type: str = None) -> List[SteelSection]:
        """Search sections by criteria"""
        sections = self.sections.get(standard, [])
        
        filtered = [s for s in sections if min_depth <= s.depth <= max_depth]
        
        if section_type:
            filtered = [s for s in filtered if s.type == section_type]
        
        return filtered
    
    def get_section(self, designation: str, standard: str) -> Optional[SteelSection]:
        """Get specific section by designation"""
        sections = self.sections.get(standard, [])
        
        for section in sections:
            if section.designation == designation:
                return section
        
        return None
    
    def get_all_standards(self) -> List[str]:
        """Get list of available standards"""
        return list(self.sections.keys())
    
    def get_section_types(self, standard: str) -> List[str]:
        """Get available section types for a standard"""
        sections = self.sections.get(standard, [])
        return list(set(s.type for s in sections))
