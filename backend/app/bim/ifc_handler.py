from typing import Dict, List
import json
from datetime import datetime

# SECURITY FIX: Use timezone-aware datetime
from app.core.datetime_utils import utc_now
class IFCHandler:
    """Handle IFC file generation and parsing for BIM integration"""
    
    def __init__(self):
        self.ifc_version = "IFC4"
    
    def export_to_ifc(self, model_data: Dict) -> str:
        """Export structural model to IFC format"""
        ifc_content = self._generate_ifc_header()
        ifc_content += self._generate_ifc_geometry(model_data.get('geometry', {}))
        ifc_content += self._generate_ifc_properties(model_data.get('properties', {}))
        ifc_content += self._generate_ifc_footer()
        
        return ifc_content
    
    def import_from_ifc(self, ifc_content: str) -> Dict:
        """Parse IFC file and extract structural data"""
        # Simplified IFC parsing
        model_data = {
            "nodes": [],
            "elements": [],
            "materials": {},
            "metadata": {}
        }
        
        # Parse IFC entities (simplified)
        lines = ifc_content.split('\n')
        for line in lines:
            if 'IFCCOLUMN' in line:
                model_data['elements'].append(self._parse_column(line))
            elif 'IFCBEAM' in line:
                model_data['elements'].append(self._parse_beam(line))
            elif 'IFCSLAB' in line:
                model_data['elements'].append(self._parse_slab(line))
        
        return model_data
    
    def _generate_ifc_header(self) -> str:
        """Generate IFC file header"""
        timestamp = utc_now().isoformat()
        return f"""ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('ViewDefinition [CoordinationView]'), '2;1');
FILE_NAME('StruMind_Export.ifc', '{timestamp}', ('StruMind'), ('StruMind Platform'), 'StruMind v1.0', 'StruMind', '');
FILE_SCHEMA(('{self.ifc_version}'));
ENDSEC;
DATA;
"""
    
    def _generate_ifc_geometry(self, geometry: Dict) -> str:
        """Generate IFC geometry entities"""
        ifc_entities = []
        
        # Generate columns
        for i, col in enumerate(geometry.get('columns', [])):
            ifc_entities.append(
                f"#{i+100}=IFCCOLUMN('{col.get('id')}', #1, 'Column', 'Structural Column', $, #2, #3, $);\n"
            )
        
        # Generate beams
        for i, beam in enumerate(geometry.get('beams', [])):
            ifc_entities.append(
                f"#{i+200}=IFCBEAM('{beam.get('id')}', #1, 'Beam', 'Structural Beam', $, #2, #3, $);\n"
            )
        
        return ''.join(ifc_entities)
    
    def _generate_ifc_properties(self, properties: Dict) -> str:
        """
        Generate IFC property sets
        SECURITY FIX: Sanitize property values to prevent injection
        """
        # Sanitize property values
        design_code = self._sanitize_ifc_value(properties.get('design_code', 'IS456'))
        material_grade = self._sanitize_ifc_value(properties.get('material_grade', 'M25'))
        
        return f"""#1000=IFCPROPERTYSET('StructuralProperties', #1, 'Structural Analysis Properties', $, (#1001, #1002));
#1001=IFCPROPERTYSINGLEVALUE('DesignCode', $, IFCTEXT('{design_code}'), $);
#1002=IFCPROPERTYSINGLEVALUE('MaterialGrade', $, IFCTEXT('{material_grade}'), $);
"""
    
    def _sanitize_ifc_value(self, value: str) -> str:
        """
        Sanitize IFC property values to prevent injection
        Removes quotes, newlines, and control characters
        """
        if not isinstance(value, str):
            value = str(value)
        
        # Remove dangerous characters
        sanitized = value.replace("'", "").replace('"', "").replace('\n', '').replace('\r', '')
        
        # Remove control characters
        sanitized = ''.join(char for char in sanitized if ord(char) >= 32)
        
        # Limit length
        return sanitized[:100]
    
    def _generate_ifc_footer(self) -> str:
        """Generate IFC file footer"""
        return "ENDSEC;\nEND-ISO-10303-21;\n"
    
    def _parse_column(self, line: str) -> Dict:
        """Parse IFC column entity"""
        return {
            "type": "column",
            "id": "COL_001",
            "section": {"width": 300, "depth": 300}
        }
    
    def _parse_beam(self, line: str) -> Dict:
        """Parse IFC beam entity"""
        return {
            "type": "beam",
            "id": "BEAM_001",
            "section": {"width": 300, "depth": 450}
        }
    
    def _parse_slab(self, line: str) -> Dict:
        """Parse IFC slab entity"""
        return {
            "type": "slab",
            "id": "SLAB_001",
            "thickness": 150
        }
