"""
Results Processing and Visualization Data Generation
"""
import numpy as np
from typing import Dict, List

class ResultsProcessor:
    """Process analysis results for visualization"""
    
    def __init__(self):
        self.results = {}
        
    def generate_moment_diagram(self, element_id: str, moments: List[float],
                               stations: List[float]) -> Dict:
        """Generate moment diagram data"""
        max_moment = max(abs(m) for m in moments) if moments else 0
        max_pos_moment = max(moments) if moments else 0
        max_neg_moment = min(moments) if moments else 0
        
        zero_crossings = []
        for i in range(len(moments) - 1):
            if moments[i] * moments[i+1] < 0:
                x = stations[i] - moments[i] * (stations[i+1] - stations[i]) / (moments[i+1] - moments[i])
                zero_crossings.append(x)
        
        return {
            "element_id": element_id,
            "type": "moment",
            "stations": stations,
            "values": moments,
            "max_positive": max_pos_moment,
            "max_negative": max_neg_moment,
            "max_absolute": max_moment,
            "zero_crossings": zero_crossings,
            "unit": "kNm"
        }
    
    def generate_shear_diagram(self, element_id: str, shears: List[float],
                              stations: List[float]) -> Dict:
        """Generate shear force diagram data"""
        max_shear = max(abs(s) for s in shears) if shears else 0
        max_pos_shear = max(shears) if shears else 0
        max_neg_shear = min(shears) if shears else 0
        
        return {
            "element_id": element_id,
            "type": "shear",
            "stations": stations,
            "values": shears,
            "max_positive": max_pos_shear,
            "max_negative": max_neg_shear,
            "max_absolute": max_shear,
            "unit": "kN"
        }
    
    def generate_deflection_curve(self, element_id: str, deflections: List[float],
                                 stations: List[float], span: float) -> Dict:
        """Generate deflection curve data"""
        max_deflection = max(abs(d) for d in deflections) if deflections else 0
        max_pos_deflection = max(deflections) if deflections else 0
        max_neg_deflection = min(deflections) if deflections else 0
        
        span_mm = span * 1000
        limit_l_250 = span_mm / 250
        limit_l_300 = span_mm / 300
        limit_l_500 = span_mm / 500
        
        deflection_check = {
            "L/250": max_deflection <= limit_l_250,
            "L/300": max_deflection <= limit_l_300,
            "L/500": max_deflection <= limit_l_500
        }
        
        return {
            "element_id": element_id,
            "type": "deflection",
            "stations": stations,
            "values": deflections,
            "max_positive": max_pos_deflection,
            "max_negative": max_neg_deflection,
            "max_absolute": max_deflection,
            "limits": {
                "L/250": limit_l_250,
                "L/300": limit_l_300,
                "L/500": limit_l_500
            },
            "checks": deflection_check,
            "span": span,
            "unit": "mm"
        }
