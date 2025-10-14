"""
Import/Export Module
Support for DXF, Excel, CSV, and other formats
"""
import json
import csv
from typing import Dict, List
from io import StringIO, BytesIO

class ImportExport:
    """Handle various import/export formats"""
    
    def __init__(self):
        self.supported_formats = ['json', 'csv', 'excel', 'dxf', 'ifc']
        
    def export_to_csv(self, data: List[Dict], filename: str = None) -> str:
        """
        Export data to CSV format
        
        Args:
            data: List of dictionaries
            filename: Optional filename
        """
        if not data:
            return ""
        
        output = StringIO()
        
        # Get headers from first item
        headers = list(data[0].keys())
        
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
        
        csv_content = output.getvalue()
        output.close()
        
        return csv_content
    
    def import_from_csv(self, csv_content: str) -> List[Dict]:
        """
        Import data from CSV format
        
        Args:
            csv_content: CSV string content
        """
        input_stream = StringIO(csv_content)
        reader = csv.DictReader(input_stream)
        
        data = [row for row in reader]
        input_stream.close()
        
        return data
    
    def export_results_to_excel_format(self, results: Dict) -> Dict:
        """
        Format results for Excel export
        
        Args:
            results: Analysis results dictionary
        """
        excel_data = {
            'sheets': []
        }
        
        # Node displacements sheet
        if 'displacements' in results:
            displacement_data = []
            for node_id, disp in results['displacements'].items():
                displacement_data.append({
                    'Node': node_id,
                    'Ux (mm)': disp.get('ux', 0),
                    'Uy (mm)': disp.get('uy', 0),
                    'Uz (mm)': disp.get('uz', 0),
                    'Rx (rad)': disp.get('rx', 0),
                    'Ry (rad)': disp.get('ry', 0),
                    'Rz (rad)': disp.get('rz', 0)
                })
            
            excel_data['sheets'].append({
                'name': 'Displacements',
                'data': displacement_data
            })
        
        # Element forces sheet
        if 'forces' in results:
            force_data = []
            for elem_id, forces in results['forces'].items():
                force_data.append({
                    'Element': elem_id,
                    'Axial (kN)': forces.get('axial', 0),
                    'Shear-Y (kN)': forces.get('shear_y', 0),
                    'Shear-Z (kN)': forces.get('shear_z', 0),
                    'Torsion (kNm)': forces.get('torsion', 0),
                    'Moment-Y (kNm)': forces.get('moment_y', 0),
                    'Moment-Z (kNm)': forces.get('moment_z', 0)
                })
            
            excel_data['sheets'].append({
                'name': 'Element Forces',
                'data': force_data
            })
        
        # Reactions sheet
        if 'reactions' in results:
            reaction_data = []
            for node_id, reactions in results['reactions'].items():
                reaction_data.append({
                    'Node': node_id,
                    'Fx (kN)': reactions.get('fx', 0),
                    'Fy (kN)': reactions.get('fy', 0),
                    'Fz (kN)': reactions.get('fz', 0),
                    'Mx (kNm)': reactions.get('mx', 0),
                    'My (kNm)': reactions.get('my', 0),
                    'Mz (kNm)': reactions.get('mz', 0)
                })
            
            excel_data['sheets'].append({
                'name': 'Reactions',
                'data': reaction_data
            })
        
        return excel_data
    
    def export_to_dxf_format(self, model: Dict) -> Dict:
        """
        Format model data for DXF export
        
        Args:
            model: Model dictionary with nodes and elements
        """
        dxf_data = {
            'entities': []
        }
        
        # Export nodes as points
        if 'nodes' in model:
            for node_id, node_data in model['nodes'].items():
                dxf_data['entities'].append({
                    'type': 'POINT',
                    'layer': 'NODES',
                    'coordinates': [
                        node_data.get('x', 0),
                        node_data.get('y', 0),
                        node_data.get('z', 0)
                    ],
                    'attributes': {
                        'node_id': node_id
                    }
                })
        
        # Export elements as lines/polylines
        if 'elements' in model and 'nodes' in model:
            for elem_id, elem_data in model['elements'].items():
                elem_type = elem_data.get('type', 'frame')
                elem_nodes = elem_data.get('nodes', [])
                
                if elem_type == 'frame' and len(elem_nodes) >= 2:
                    # Line element
                    node1 = model['nodes'][elem_nodes[0]]
                    node2 = model['nodes'][elem_nodes[1]]
                    
                    dxf_data['entities'].append({
                        'type': 'LINE',
                        'layer': 'ELEMENTS',
                        'start': [node1.get('x', 0), node1.get('y', 0), node1.get('z', 0)],
                        'end': [node2.get('x', 0), node2.get('y', 0), node2.get('z', 0)],
                        'attributes': {
                            'element_id': elem_id,
                            'element_type': elem_type
                        }
                    })
                
                elif elem_type in ['shell', 'quad4', 'tri3']:
                    # Shell element as polyline
                    vertices = []
                    for node_id in elem_nodes:
                        node = model['nodes'][node_id]
                        vertices.append([
                            node.get('x', 0),
                            node.get('y', 0),
                            node.get('z', 0)
                        ])
                    
                    dxf_data['entities'].append({
                        'type': 'POLYLINE',
                        'layer': 'SHELLS',
                        'vertices': vertices,
                        'closed': True,
                        'attributes': {
                            'element_id': elem_id,
                            'element_type': elem_type
                        }
                    })
        
        return dxf_data
    
    def import_from_excel_format(self, excel_data: Dict) -> Dict:
        """
        Import model from Excel format
        
        Args:
            excel_data: Excel data dictionary
        """
        model = {
            'nodes': {},
            'elements': {},
            'loads': {}
        }
        
        for sheet in excel_data.get('sheets', []):
            sheet_name = sheet.get('name', '').lower()
            data = sheet.get('data', [])
            
            if 'node' in sheet_name:
                # Import nodes
                for row in data:
                    node_id = row.get('Node') or row.get('ID')
                    if node_id:
                        model['nodes'][node_id] = {
                            'x': float(row.get('X', 0)),
                            'y': float(row.get('Y', 0)),
                            'z': float(row.get('Z', 0))
                        }
            
            elif 'element' in sheet_name:
                # Import elements
                for row in data:
                    elem_id = row.get('Element') or row.get('ID')
                    if elem_id:
                        model['elements'][elem_id] = {
                            'type': row.get('Type', 'frame'),
                            'nodes': [
                                row.get('Node1') or row.get('NodeI'),
                                row.get('Node2') or row.get('NodeJ')
                            ],
                            'section': row.get('Section', '')
                        }
            
            elif 'load' in sheet_name:
                # Import loads
                for row in data:
                    load_id = row.get('Load') or row.get('ID')
                    if load_id:
                        model['loads'][load_id] = {
                            'type': row.get('Type', 'point'),
                            'node': row.get('Node'),
                            'element': row.get('Element'),
                            'fx': float(row.get('Fx', 0)),
                            'fy': float(row.get('Fy', 0)),
                            'fz': float(row.get('Fz', 0))
                        }
        
        return model
    
    def export_bbs_to_excel(self, bbs_data: List[Dict]) -> Dict:
        """
        Export Bar Bending Schedule to Excel format
        
        Args:
            bbs_data: BBS data list
        """
        excel_data = {
            'sheets': [{
                'name': 'Bar Bending Schedule',
                'data': []
            }]
        }
        
        for item in bbs_data:
            excel_data['sheets'][0]['data'].append({
                'Mark': item.get('mark', ''),
                'Diameter (mm)': item.get('diameter', 0),
                'Shape': item.get('shape', ''),
                'Length (mm)': item.get('length', 0),
                'Number': item.get('number', 0),
                'Total Length (m)': item.get('total_length', 0),
                'Weight (kg)': item.get('weight', 0),
                'Location': item.get('location', '')
            })
        
        # Add summary row
        total_weight = sum(item.get('weight', 0) for item in bbs_data)
        excel_data['sheets'][0]['data'].append({
            'Mark': 'TOTAL',
            'Weight (kg)': total_weight
        })
        
        return excel_data
    
    def export_boq_to_excel(self, boq_data: List[Dict]) -> Dict:
        """
        Export Bill of Quantities to Excel format
        
        Args:
            boq_data: BOQ data list
        """
        excel_data = {
            'sheets': [{
                'name': 'Bill of Quantities',
                'data': []
            }]
        }
        
        for item in boq_data:
            excel_data['sheets'][0]['data'].append({
                'Item': item.get('item', ''),
                'Description': item.get('description', ''),
                'Unit': item.get('unit', ''),
                'Quantity': item.get('quantity', 0),
                'Rate': item.get('rate', 0),
                'Amount': item.get('amount', 0)
            })
        
        # Add total
        total_amount = sum(item.get('amount', 0) for item in boq_data)
        excel_data['sheets'][0]['data'].append({
            'Item': 'TOTAL',
            'Amount': total_amount
        })
        
        return excel_data
    
    def export_design_summary(self, design_results: Dict) -> Dict:
        """
        Export design summary report
        
        Args:
            design_results: Design results dictionary
        """
        summary = {
            'project_info': design_results.get('project_info', {}),
            'design_summary': [],
            'checks': []
        }
        
        # Extract key design parameters
        for member_id, member_design in design_results.get('members', {}).items():
            summary['design_summary'].append({
                'Member': member_id,
                'Type': member_design.get('type', ''),
                'Section': member_design.get('section', ''),
                'Status': member_design.get('status', ''),
                'Utilization': member_design.get('utilization', 0)
            })
            
            # Extract checks
            for check_name, check_result in member_design.get('checks', {}).items():
                summary['checks'].append({
                    'Member': member_id,
                    'Check': check_name,
                    'Status': check_result.get('status', ''),
                    'Ratio': check_result.get('ratio', 0)
                })
        
        return summary
