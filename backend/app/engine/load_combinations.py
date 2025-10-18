"""
Load combination generator for various design codes
Implements automatic generation of load combinations per IS 456, ACI 318, Eurocode, etc.
"""
from typing import Dict, List, Optional
from enum import Enum


class DesignCode(str, Enum):
    """Supported design codes"""
    IS456 = "IS456"  # Indian Standard
    ACI318 = "ACI318"  # American Concrete Institute
    EUROCODE = "EC2"  # Eurocode 2
    BS8110 = "BS8110"  # British Standard


class LoadType(str, Enum):
    """Load types"""
    DEAD = "dead"
    LIVE = "live"
    WIND = "wind"
    EARTHQUAKE = "earthquake"
    SNOW = "snow"
    TEMPERATURE = "temperature"
    SETTLEMENT = "settlement"


class LimitState(str, Enum):
    """Limit states"""
    ULTIMATE = "ultimate"  # ULS
    SERVICEABILITY = "serviceability"  # SLS


class LoadCombination:
    """Represents a single load combination"""
    
    def __init__(self, name: str, factors: Dict[str, float], 
                 limit_state: LimitState, description: str = ""):
        self.name = name
        self.factors = factors
        self.limit_state = limit_state
        self.description = description
    
    def apply(self, load_cases: Dict[str, any]) -> any:
        """
        Apply combination factors to load cases
        
        Args:
            load_cases: Dict of {load_type: load_vector}
        
        Returns:
            Combined load vector
        """
        combined = None
        
        for load_type, factor in self.factors.items():
            if load_type in load_cases and load_cases[load_type] is not None:
                load = load_cases[load_type]
                
                if combined is None:
                    combined = factor * load
                else:
                    combined = combined + factor * load
        
        return combined
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'factors': self.factors,
            'limit_state': self.limit_state,
            'description': self.description
        }


class LoadCombinationGenerator:
    """Generate load combinations per design codes"""
    
    @staticmethod
    def generate_is456_combinations(load_types: List[str]) -> List[LoadCombination]:
        """
        Generate load combinations per IS 456:2000
        
        Clause 36.4: Load Combinations and Increase in Permissible Stresses
        """
        combinations = []
        
        has_dead = LoadType.DEAD in load_types
        has_live = LoadType.LIVE in load_types
        has_wind = LoadType.WIND in load_types
        has_eq = LoadType.EARTHQUAKE in load_types
        
        # Ultimate Limit State (ULS) combinations
        
        # 1. DL + LL
        if has_dead and has_live:
            combinations.append(LoadCombination(
                name="ULS1_DL+LL",
                factors={LoadType.DEAD: 1.5, LoadType.LIVE: 1.5},
                limit_state=LimitState.ULTIMATE,
                description="1.5(DL + LL)"
            ))
        
        # 2. DL + EQ
        if has_dead and has_eq:
            combinations.append(LoadCombination(
                name="ULS2_DL+EQ",
                factors={LoadType.DEAD: 1.5, LoadType.EARTHQUAKE: 1.5},
                limit_state=LimitState.ULTIMATE,
                description="1.5(DL + EQ)"
            ))
        
        # 3. DL + LL + EQ
        if has_dead and has_live and has_eq:
            combinations.append(LoadCombination(
                name="ULS3_DL+LL+EQ",
                factors={LoadType.DEAD: 1.2, LoadType.LIVE: 1.2, LoadType.EARTHQUAKE: 1.2},
                limit_state=LimitState.ULTIMATE,
                description="1.2(DL + LL + EQ)"
            ))
        
        # 4. DL + WL (Wind in different directions)
        if has_dead and has_wind:
            combinations.append(LoadCombination(
                name="ULS4_DL+WL",
                factors={LoadType.DEAD: 1.5, LoadType.WIND: 1.5},
                limit_state=LimitState.ULTIMATE,
                description="1.5(DL + WL)"
            ))
            
            # 5. DL - WL (Wind reversal)
            combinations.append(LoadCombination(
                name="ULS5_DL-WL",
                factors={LoadType.DEAD: 1.5, LoadType.WIND: -1.5},
                limit_state=LimitState.ULTIMATE,
                description="1.5(DL - WL)"
            ))
        
        # 6. 0.9DL + 1.5WL (Uplift case)
        if has_dead and has_wind:
            combinations.append(LoadCombination(
                name="ULS6_0.9DL+1.5WL",
                factors={LoadType.DEAD: 0.9, LoadType.WIND: 1.5},
                limit_state=LimitState.ULTIMATE,
                description="0.9DL + 1.5WL (Uplift)"
            ))
            
            combinations.append(LoadCombination(
                name="ULS7_0.9DL-1.5WL",
                factors={LoadType.DEAD: 0.9, LoadType.WIND: -1.5},
                limit_state=LimitState.ULTIMATE,
                description="0.9DL - 1.5WL (Uplift)"
            ))
        
        # 7. DL + LL + WL
        if has_dead and has_live and has_wind:
            combinations.append(LoadCombination(
                name="ULS8_DL+LL+WL",
                factors={LoadType.DEAD: 1.2, LoadType.LIVE: 1.2, LoadType.WIND: 1.2},
                limit_state=LimitState.ULTIMATE,
                description="1.2(DL + LL + WL)"
            ))
            
            combinations.append(LoadCombination(
                name="ULS9_DL+LL-WL",
                factors={LoadType.DEAD: 1.2, LoadType.LIVE: 1.2, LoadType.WIND: -1.2},
                limit_state=LimitState.ULTIMATE,
                description="1.2(DL + LL - WL)"
            ))
        
        # Serviceability Limit State (SLS) combinations
        
        # 1. DL + LL
        if has_dead and has_live:
            combinations.append(LoadCombination(
                name="SLS1_DL+LL",
                factors={LoadType.DEAD: 1.0, LoadType.LIVE: 1.0},
                limit_state=LimitState.SERVICEABILITY,
                description="DL + LL"
            ))
        
        # 2. DL + 0.8LL
        if has_dead and has_live:
            combinations.append(LoadCombination(
                name="SLS2_DL+0.8LL",
                factors={LoadType.DEAD: 1.0, LoadType.LIVE: 0.8},
                limit_state=LimitState.SERVICEABILITY,
                description="DL + 0.8LL"
            ))
        
        return combinations

    
    @staticmethod
    def generate_aci318_combinations(load_types: List[str]) -> List[LoadCombination]:
        """
        Generate load combinations per ACI 318-19
        
        Section 5.3: Required Strength
        """
        combinations = []
        
        has_dead = LoadType.DEAD in load_types
        has_live = LoadType.LIVE in load_types
        has_wind = LoadType.WIND in load_types
        has_eq = LoadType.EARTHQUAKE in load_types
        
        # U = 1.4D
        if has_dead:
            combinations.append(LoadCombination(
                name="ACI1_1.4D",
                factors={LoadType.DEAD: 1.4},
                limit_state=LimitState.ULTIMATE,
                description="U = 1.4D"
            ))
        
        # U = 1.2D + 1.6L
        if has_dead and has_live:
            combinations.append(LoadCombination(
                name="ACI2_1.2D+1.6L",
                factors={LoadType.DEAD: 1.2, LoadType.LIVE: 1.6},
                limit_state=LimitState.ULTIMATE,
                description="U = 1.2D + 1.6L"
            ))
        
        # U = 1.2D + 1.0L + 1.0W
        if has_dead and has_live and has_wind:
            combinations.append(LoadCombination(
                name="ACI3_1.2D+1.0L+1.0W",
                factors={LoadType.DEAD: 1.2, LoadType.LIVE: 1.0, LoadType.WIND: 1.0},
                limit_state=LimitState.ULTIMATE,
                description="U = 1.2D + 1.0L + 1.0W"
            ))
        
        # U = 1.2D + 1.0L + 1.0E
        if has_dead and has_live and has_eq:
            combinations.append(LoadCombination(
                name="ACI4_1.2D+1.0L+1.0E",
                factors={LoadType.DEAD: 1.2, LoadType.LIVE: 1.0, LoadType.EARTHQUAKE: 1.0},
                limit_state=LimitState.ULTIMATE,
                description="U = 1.2D + 1.0L + 1.0E"
            ))
        
        # U = 0.9D + 1.0W
        if has_dead and has_wind:
            combinations.append(LoadCombination(
                name="ACI5_0.9D+1.0W",
                factors={LoadType.DEAD: 0.9, LoadType.WIND: 1.0},
                limit_state=LimitState.ULTIMATE,
                description="U = 0.9D + 1.0W"
            ))
        
        # U = 0.9D + 1.0E
        if has_dead and has_eq:
            combinations.append(LoadCombination(
                name="ACI6_0.9D+1.0E",
                factors={LoadType.DEAD: 0.9, LoadType.EARTHQUAKE: 1.0},
                limit_state=LimitState.ULTIMATE,
                description="U = 0.9D + 1.0E"
            ))
        
        return combinations
    
    @staticmethod
    def generate_eurocode_combinations(load_types: List[str]) -> List[LoadCombination]:
        """
        Generate load combinations per Eurocode (EN 1990)
        
        Section 6.4: Ultimate Limit States
        """
        combinations = []
        
        has_dead = LoadType.DEAD in load_types
        has_live = LoadType.LIVE in load_types
        has_wind = LoadType.WIND in load_types
        has_eq = LoadType.EARTHQUAKE in load_types
        
        # Partial factors
        gamma_G = 1.35  # Permanent actions (unfavorable)
        gamma_G_fav = 1.0  # Permanent actions (favorable)
        gamma_Q = 1.5  # Variable actions
        psi_0 = 0.7  # Combination factor
        
        # EQU: Loss of equilibrium
        # STR/GEO: Structural failure or excessive deformation
        
        # Combination 1: 1.35G + 1.5Q
        if has_dead and has_live:
            combinations.append(LoadCombination(
                name="EC1_1.35G+1.5Q",
                factors={LoadType.DEAD: gamma_G, LoadType.LIVE: gamma_Q},
                limit_state=LimitState.ULTIMATE,
                description="1.35G + 1.5Q"
            ))
        
        # Combination 2: 1.35G + 1.5W + 1.05Q
        if has_dead and has_wind and has_live:
            combinations.append(LoadCombination(
                name="EC2_1.35G+1.5W+1.05Q",
                factors={LoadType.DEAD: gamma_G, LoadType.WIND: gamma_Q, LoadType.LIVE: psi_0 * gamma_Q},
                limit_state=LimitState.ULTIMATE,
                description="1.35G + 1.5W + 1.05Q"
            ))
        
        # Combination 3: 1.0G + 1.5W (Uplift)
        if has_dead and has_wind:
            combinations.append(LoadCombination(
                name="EC3_1.0G+1.5W",
                factors={LoadType.DEAD: gamma_G_fav, LoadType.WIND: gamma_Q},
                limit_state=LimitState.ULTIMATE,
                description="1.0G + 1.5W (Uplift)"
            ))
        
        # Seismic combination: G + 0.3Q + E
        if has_dead and has_eq:
            factors = {LoadType.DEAD: 1.0, LoadType.EARTHQUAKE: 1.0}
            if has_live:
                factors[LoadType.LIVE] = 0.3
            
            combinations.append(LoadCombination(
                name="EC4_G+0.3Q+E",
                factors=factors,
                limit_state=LimitState.ULTIMATE,
                description="G + 0.3Q + E (Seismic)"
            ))
        
        # Serviceability combinations
        # Characteristic: G + Q
        if has_dead and has_live:
            combinations.append(LoadCombination(
                name="EC_SLS1_G+Q",
                factors={LoadType.DEAD: 1.0, LoadType.LIVE: 1.0},
                limit_state=LimitState.SERVICEABILITY,
                description="G + Q (Characteristic)"
            ))
        
        # Quasi-permanent: G + 0.3Q
        if has_dead and has_live:
            combinations.append(LoadCombination(
                name="EC_SLS2_G+0.3Q",
                factors={LoadType.DEAD: 1.0, LoadType.LIVE: 0.3},
                limit_state=LimitState.SERVICEABILITY,
                description="G + 0.3Q (Quasi-permanent)"
            ))
        
        return combinations
    
    @staticmethod
    def generate_combinations(code: DesignCode, load_types: List[str]) -> List[LoadCombination]:
        """
        Generate load combinations for specified design code
        
        Args:
            code: Design code
            load_types: List of load types present in the model
        
        Returns:
            List of LoadCombination objects
        """
        if code == DesignCode.IS456:
            return LoadCombinationGenerator.generate_is456_combinations(load_types)
        elif code == DesignCode.ACI318:
            return LoadCombinationGenerator.generate_aci318_combinations(load_types)
        elif code == DesignCode.EUROCODE:
            return LoadCombinationGenerator.generate_eurocode_combinations(load_types)
        else:
            # Default to IS 456
            return LoadCombinationGenerator.generate_is456_combinations(load_types)
    
    @staticmethod
    def generate_wind_directions(base_combination: LoadCombination, 
                                n_directions: int = 8) -> List[LoadCombination]:
        """
        Generate combinations for wind in multiple directions
        
        Args:
            base_combination: Base combination with wind
            n_directions: Number of wind directions (typically 8)
        
        Returns:
            List of combinations for each direction
        """
        combinations = []
        angles = [i * 360 / n_directions for i in range(n_directions)]
        
        for i, angle in enumerate(angles):
            new_comb = LoadCombination(
                name=f"{base_combination.name}_W{int(angle)}",
                factors=base_combination.factors.copy(),
                limit_state=base_combination.limit_state,
                description=f"{base_combination.description} (Wind @ {int(angle)}°)"
            )
            combinations.append(new_comb)
        
        return combinations
    
    @staticmethod
    def generate_seismic_directions(base_combination: LoadCombination) -> List[LoadCombination]:
        """
        Generate combinations for seismic in ±X and ±Y directions
        
        Returns:
            List of combinations for EQX+, EQX-, EQY+, EQY-
        """
        combinations = []
        directions = [
            ("EQX+", 1.0, 0.0),
            ("EQX-", -1.0, 0.0),
            ("EQY+", 0.0, 1.0),
            ("EQY-", 0.0, -1.0),
            ("EQX+0.3Y", 1.0, 0.3),
            ("EQX-0.3Y", -1.0, 0.3),
            ("0.3X+EQY", 0.3, 1.0),
            ("0.3X-EQY", 0.3, -1.0),
        ]
        
        for dir_name, factor_x, factor_y in directions:
            factors = base_combination.factors.copy()
            
            # Modify earthquake factor
            if LoadType.EARTHQUAKE in factors:
                eq_factor = factors[LoadType.EARTHQUAKE]
                # Split into X and Y components
                factors[f"{LoadType.EARTHQUAKE}_x"] = eq_factor * factor_x
                factors[f"{LoadType.EARTHQUAKE}_y"] = eq_factor * factor_y
                del factors[LoadType.EARTHQUAKE]
            
            new_comb = LoadCombination(
                name=f"{base_combination.name}_{dir_name}",
                factors=factors,
                limit_state=base_combination.limit_state,
                description=f"{base_combination.description} ({dir_name})"
            )
            combinations.append(new_comb)
        
        return combinations


class EnvelopeGenerator:
    """Generate envelope of results from multiple load combinations"""
    
    @staticmethod
    def generate_envelope(combination_results: Dict[str, Dict]) -> Dict:
        """
        Generate envelope (max/min) of results
        
        Args:
            combination_results: Dict of {combination_name: results_dict}
        
        Returns:
            Dict with max/min values for each result type
        """
        envelope = {
            'max': {},
            'min': {},
            'governing_combinations': {}
        }
        
        if not combination_results:
            return envelope
        
        # Get result keys from first combination
        first_result = next(iter(combination_results.values()))
        result_keys = first_result.keys()
        
        # Initialize max/min
        for key in result_keys:
            envelope['max'][key] = float('-inf')
            envelope['min'][key] = float('inf')
            envelope['governing_combinations'][key] = {'max': None, 'min': None}
        
        # Find max/min for each result type
        for comb_name, results in combination_results.items():
            for key, value in results.items():
                if isinstance(value, (int, float)):
                    if value > envelope['max'][key]:
                        envelope['max'][key] = value
                        envelope['governing_combinations'][key]['max'] = comb_name
                    
                    if value < envelope['min'][key]:
                        envelope['min'][key] = value
                        envelope['governing_combinations'][key]['min'] = comb_name
        
        return envelope
    
    @staticmethod
    def identify_critical_members(utilization_ratios: Dict[str, float], 
                                  threshold: float = 0.95) -> List[str]:
        """
        Identify members with high utilization ratios
        
        Args:
            utilization_ratios: Dict of {member_id: UR}
            threshold: UR threshold for critical members
        
        Returns:
            List of critical member IDs
        """
        critical = []
        
        for member_id, ur in utilization_ratios.items():
            if ur >= threshold:
                critical.append(member_id)
        
        return sorted(critical, key=lambda x: utilization_ratios[x], reverse=True)
