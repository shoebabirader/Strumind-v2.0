"""
Moving Load Analysis Module
For bridges and structures with moving loads
"""
import numpy as np
from typing import Dict, List, Tuple

class MovingLoadAnalysis:
    """Moving load analysis for bridges"""
    
    def __init__(self):
        self.influence_lines = {}
        
    def generate_influence_line(self, span: float, n_stations: int,
                                response_type: str, location: float) -> Dict:
        """
        Generate influence line for a response at a specific location
        
        Args:
            span: Span length (m)
            n_stations: Number of stations
            response_type: 'moment', 'shear', 'reaction', 'deflection'
            location: Location where response is measured (m from left support)
        """
        stations = np.linspace(0, span, n_stations)
        influence_values = np.zeros(n_stations)
        
        a = location  # Distance from left support
        b = span - a  # Distance from right support
        
        if response_type == "moment":
            # Influence line for moment at location 'a'
            for i, x in enumerate(stations):
                if x <= a:
                    influence_values[i] = (b * x) / span
                else:
                    influence_values[i] = (a * (span - x)) / span
                    
        elif response_type == "shear":
            # Influence line for shear at location 'a'
            for i, x in enumerate(stations):
                if x < a:
                    influence_values[i] = b / span
                else:
                    influence_values[i] = -a / span
                    
        elif response_type == "reaction":
            # Influence line for reaction at left support
            if location == 0:
                influence_values = 1 - stations / span
            else:  # Right support
                influence_values = stations / span
                
        elif response_type == "deflection":
            # Influence line for deflection at location 'a'
            for i, x in enumerate(stations):
                if x <= a:
                    influence_values[i] = (b * x / (6 * span)) * (span**2 - b**2 - x**2)
                else:
                    influence_values[i] = (a * (span - x) / (6 * span)) * (span**2 - a**2 - (span - x)**2)
        
        return {
            "span": span,
            "response_type": response_type,
            "location": location,
            "stations": stations.tolist(),
            "influence_values": influence_values.tolist(),
            "max_positive": np.max(influence_values),
            "max_negative": np.min(influence_values)
        }
    
    def analyze_single_point_load(self, influence_line: Dict, load: float,
                                  load_position: float) -> float:
        """
        Calculate response for a single point load
        
        Args:
            influence_line: Influence line data
            load: Load magnitude (kN)
            load_position: Position of load (m)
        """
        stations = np.array(influence_line['stations'])
        values = np.array(influence_line['influence_values'])
        
        # Interpolate influence value at load position
        influence_at_load = np.interp(load_position, stations, values)
        
        response = load * influence_at_load
        
        return response
    
    def analyze_udl(self, influence_line: Dict, udl: float,
                   start_position: float, end_position: float) -> float:
        """
        Calculate response for uniformly distributed load
        
        Args:
            influence_line: Influence line data
            udl: UDL intensity (kN/m)
            start_position: Start of UDL (m)
            end_position: End of UDL (m)
        """
        stations = np.array(influence_line['stations'])
        values = np.array(influence_line['influence_values'])
        
        # Find stations within UDL range
        mask = (stations >= start_position) & (stations <= end_position)
        stations_in_range = stations[mask]
        values_in_range = values[mask]
        
        # Integrate using trapezoidal rule
        if len(stations_in_range) > 1:
            area = np.trapz(values_in_range, stations_in_range)
            response = udl * area
        else:
            response = 0
        
        return response
    
    def analyze_moving_load_train(self, span: float, response_type: str,
                                  location: float, load_train: List[Dict]) -> Dict:
        """
        Analyze moving load train (e.g., IRC loading, AASHTO truck)
        
        Args:
            span: Span length (m)
            response_type: Type of response
            location: Location where response is measured
            load_train: List of loads [{'load': kN, 'spacing': m}, ...]
        """
        # Generate influence line
        influence_line = self.generate_influence_line(span, 100, response_type, location)
        
        # Move load train across span
        n_positions = 100
        max_response = 0
        min_response = 0
        critical_position = 0
        
        # Calculate total length of load train
        train_length = sum(load['spacing'] for load in load_train[:-1])
        
        # Move from -train_length to span
        positions = np.linspace(-train_length, span, n_positions)
        responses = []
        
        for pos in positions:
            # Calculate response for this position
            total_response = 0
            current_pos = pos
            
            for load_data in load_train:
                load = load_data['load']
                
                # Check if load is on span
                if 0 <= current_pos <= span:
                    response = self.analyze_single_point_load(
                        influence_line, load, current_pos
                    )
                    total_response += response
                
                # Move to next load position
                if load_data != load_train[-1]:
                    current_pos += load_data['spacing']
            
            responses.append(total_response)
            
            # Track maximum and minimum
            if total_response > max_response:
                max_response = total_response
                critical_position = pos
            if total_response < min_response:
                min_response = total_response
        
        return {
            "span": span,
            "response_type": response_type,
            "location": location,
            "load_train": load_train,
            "max_response": max_response,
            "min_response": min_response,
            "critical_position": critical_position,
            "response_envelope": {
                "positions": positions.tolist(),
                "responses": responses
            }
        }
    
    def irc_class_a_loading(self, span: float, response_type: str,
                           location: float) -> Dict:
        """
        Analyze IRC Class A loading (Indian Roads Congress)
        
        Args:
            span: Span length (m)
            response_type: Type of response
            location: Location where response is measured
        """
        # IRC Class A: Train of wheel loads
        # Simplified: 114 kN, 114 kN, 68 kN, 68 kN at 1.1m, 3.2m, 1.2m spacing
        load_train = [
            {'load': 114, 'spacing': 1.1},
            {'load': 114, 'spacing': 3.2},
            {'load': 68, 'spacing': 1.2},
            {'load': 68, 'spacing': 0}
        ]
        
        result = self.analyze_moving_load_train(span, response_type, location, load_train)
        result['loading_standard'] = 'IRC_Class_A'
        
        return result
    
    def aashto_hs20_loading(self, span: float, response_type: str,
                           location: float) -> Dict:
        """
        Analyze AASHTO HS20-44 truck loading
        
        Args:
            span: Span length (m)
            response_type: Type of response
            location: Location where response is measured
        """
        # HS20-44: 35.6 kN, 142.4 kN, 142.4 kN at 4.27m, 4.27-9.14m spacing
        # Using 4.27m for critical case
        load_train = [
            {'load': 35.6, 'spacing': 4.27},
            {'load': 142.4, 'spacing': 4.27},
            {'load': 142.4, 'spacing': 0}
        ]
        
        result = self.analyze_moving_load_train(span, response_type, location, load_train)
        result['loading_standard'] = 'AASHTO_HS20'
        
        return result
    
    def envelope_results(self, results_list: List[Dict]) -> Dict:
        """
        Create envelope of multiple moving load analyses
        
        Args:
            results_list: List of analysis results
        """
        max_positive = max(r['max_response'] for r in results_list)
        max_negative = min(r['min_response'] for r in results_list)
        
        return {
            "envelope_type": "moving_load",
            "max_positive_response": max_positive,
            "max_negative_response": max_negative,
            "number_of_cases": len(results_list),
            "governing_case": max(results_list, key=lambda x: abs(x['max_response']))
        }
