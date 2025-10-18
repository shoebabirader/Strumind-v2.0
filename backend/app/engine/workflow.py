"""
Unified Structural Analysis Workflow Manager

This module provides a high-level interface that coordinates all analysis engines
and ensures proper execution sequence. It abstracts away the complexity of managing
multiple engines and their interdependencies.

Author: StruMind Platform
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field

from .geometry import GeometryEngine
from .analysis import StructuralAnalysis
from .seismic import SeismicAnalysis, SeismicCode, SeismicZone, SoilType
from .wind import WindAnalysis, WindCode, TerrainCategory, BuildingClass
from .pdelta import PDeltaAnalysis
from .design_codes import IS456ConcreteDesign


@dataclass
class LoadCase:
    """Represents a single load case"""
    name: str
    type: str  # 'dead', 'live', 'seismic', 'wind', 'temperature'
    loads: np.ndarray = field(default_factory=lambda: np.array([]))
    factor: float = 1.0
    description: str = ""


@dataclass
class LoadCombination:
    """Represents a load combination"""
    name: str
    description: str
    load_cases: Dict[str, float]  # {load_case_name: factor}


@dataclass
class AnalysisResults:
    """Container for analysis results"""
    displacements: np.ndarray
    reactions: np.ndarray
    member_forces: Dict[int, Dict[str, float]]
    max_displacement: float
    total_reaction: float
    status: str = "success"
    warnings: List[str] = field(default_factory=list)
    
    def summary(self) -> str:
        """Generate a summary string"""
        return f"""
Analysis Results Summary:
------------------------
Status: {self.status}
Max Displacement: {self.max_displacement:.2f} mm
Total Reaction: {self.total_reaction/1000:.2f} kN
Member Forces: {len(self.member_forces)} members analyzed
Warnings: {len(self.warnings)}
"""


class StructuralWorkflow:
    """
    Unified workflow manager for structural analysis.
    
    This class coordinates all analysis engines and provides a simple,
    consistent interface for performing structural analysis.
    
    Usage:
        workflow = StructuralWorkflow()
        workflow.create_geometry(...)
        workflow.define_materials(...)
        workflow.apply_loads(...)
        results = workflow.run_analysis()
    """
    
    def __init__(self):
        """Initialize the workflow manager"""
        self.geometry = GeometryEngine()
        self.analyzer = None
        self.load_cases: Dict[str, LoadCase] = {}
        self.combinations: List[LoadCombination] = []
        
        # Analysis engines
        self.seismic_engine = None
        self.wind_engine = None
        self.pdelta_engine = None
        
        # State tracking
        self._geometry_ready = False
        self._materials_ready = False
        self._loads_ready = False
        self._stiffness_assembled = False
        
        # Results storage
        self.results: Dict[str, AnalysisResults] = {}
        
    # ========================================================================
    # GEOMETRY METHODS
    # ========================================================================
    
    def add_node(self, node_id: int, x: float, y: float, z: float, 
                 fixed: bool = False) -> None:
        """
        Add a node to the model
        
        Args:
            node_id: Unique node identifier
            x, y, z: Coordinates in mm
            fixed: If True, fix all DOFs
        """
        node = self.geometry.add_node(node_id, x, y, z)
        if fixed:
            node.set_fixed()
        self._geometry_ready = False
        
    def add_element(self, elem_id: int, node_ids: List[int], 
                   elem_type: str, material: str = None, 
                   section: str = None) -> None:
        """
        Add an element to the model
        
        Args:
            elem_id: Unique element identifier
            node_ids: List of node IDs defining the element
            elem_type: 'beam', 'column', 'truss', etc.
            material: Material name (optional)
            section: Section name (optional)
        """
        elem = self.geometry.add_element(elem_id, node_ids, elem_type)
        if material:
            elem.material = material
        if section:
            elem.section = section
        self._geometry_ready = False
        
    def validate_geometry(self) -> Tuple[bool, List[str]]:
        """
        Validate the geometry
        
        Returns:
            (is_valid, error_messages)
        """
        is_valid, errors = self.geometry.validate_geometry()
        if is_valid:
            self._geometry_ready = True
        return is_valid, errors
    
    # ========================================================================
    # MATERIAL & SECTION METHODS
    # ========================================================================
    
    def add_material(self, name: str, E: float, G: float = None, 
                    density: float = 0, nu: float = 0.3) -> None:
        """
        Add a material definition
        
        Args:
            name: Material name
            E: Young's modulus (MPa)
            G: Shear modulus (MPa), calculated if not provided
            density: Mass density (kg/mm³)
            nu: Poisson's ratio
        """
        if G is None:
            G = E / (2 * (1 + nu))
        self.geometry.add_material(name, E, G, density, nu)
        self._materials_ready = True
        
    def add_section(self, name: str, A: float, Iy: float, Iz: float, 
                   J: float) -> None:
        """
        Add a section definition
        
        Args:
            name: Section name
            A: Cross-sectional area (mm²)
            Iy, Iz: Moments of inertia (mm⁴)
            J: Torsional constant (mm⁴)
        """
        self.geometry.add_section(name, A, Iy, Iz, J)
        
    # ========================================================================
    # LOAD METHODS
    # ========================================================================
    
    def apply_nodal_load(self, node_id: int, fx: float = 0, fy: float = 0, 
                        fz: float = 0, mx: float = 0, my: float = 0, 
                        mz: float = 0) -> None:
        """
        Apply loads to a node
        
        Args:
            node_id: Node identifier
            fx, fy, fz: Forces in N
            mx, my, mz: Moments in Nmm
        """
        node = self.geometry.nodes[node_id]
        node.apply_load(fx, fy, fz, mx, my, mz)
        self._loads_ready = True
        
    def create_load_case(self, name: str, load_type: str, 
                        description: str = "") -> LoadCase:
        """
        Create a new load case
        
        Args:
            name: Load case name
            load_type: 'dead', 'live', 'seismic', 'wind', etc.
            description: Optional description
            
        Returns:
            LoadCase object
        """
        load_case = LoadCase(name=name, type=load_type, description=description)
        self.load_cases[name] = load_case
        return load_case
        
    def add_load_combination(self, name: str, description: str, 
                           factors: Dict[str, float]) -> None:
        """
        Add a load combination
        
        Args:
            name: Combination name
            description: Description
            factors: Dict of {load_case_name: factor}
        """
        combo = LoadCombination(name=name, description=description, 
                               load_cases=factors)
        self.combinations.append(combo)
        
    # ========================================================================
    # SEISMIC ANALYSIS METHODS
    # ========================================================================
    
    def setup_seismic_analysis(self, code: SeismicCode, zone: SeismicZone,
                              soil: SoilType, importance: float = 1.0,
                              response_reduction: float = 5.0) -> None:
        """
        Setup seismic analysis parameters
        
        Args:
            code: Seismic code (IS1893, ASCE7, etc.)
            zone: Seismic zone
            soil: Soil type
            importance: Importance factor
            response_reduction: Response reduction factor
        """
        self.seismic_engine = SeismicAnalysis(code)
        self.seismic_engine.set_parameters(
            zone=zone,
            importance=importance,
            response_reduction=response_reduction,
            soil=soil
        )
        
    def calculate_seismic_loads(self, height: float, weight: float) -> Dict:
        """
        Calculate seismic loads
        
        Args:
            height: Building height (m)
            weight: Seismic weight (kN)
            
        Returns:
            Dict with base shear and load distribution
        """
        if not self.seismic_engine:
            raise ValueError("Seismic analysis not setup. Call setup_seismic_analysis first.")
            
        time_period = self.seismic_engine.calculate_time_period(height, "RC_MRF")
        base_shear = self.seismic_engine.calculate_base_shear(weight, time_period)
        
        return {
            'time_period': time_period,
            'base_shear': base_shear
        }
        
    # ========================================================================
    # WIND ANALYSIS METHODS
    # ========================================================================
    
    def setup_wind_analysis(self, code: WindCode, basic_wind_speed: float,
                           terrain: TerrainCategory, building_class: BuildingClass,
                           topography: float = 1.0) -> None:
        """
        Setup wind analysis parameters
        
        Args:
            code: Wind code (IS875, ASCE7, etc.)
            basic_wind_speed: Basic wind speed (m/s)
            terrain: Terrain category
            building_class: Building class
            topography: Topography factor
        """
        self.wind_engine = WindAnalysis(code)
        self.wind_engine.set_parameters(
            basic_wind_speed=basic_wind_speed,
            terrain=terrain,
            building_class=building_class,
            topography=topography
        )
        
    def calculate_wind_loads(self, height: float, width: float, 
                           depth: float) -> Dict:
        """
        Calculate wind loads
        
        Args:
            height: Building height (m)
            width: Building width (m)
            depth: Building depth (m)
            
        Returns:
            Dict with wind pressure and forces
        """
        if not self.wind_engine:
            raise ValueError("Wind analysis not setup. Call setup_wind_analysis first.")
            
        return self.wind_engine.calculate_design_wind_pressure(
            height=height,
            building_dimensions={'width': width, 'depth': depth}
        )
        
    # ========================================================================
    # ANALYSIS METHODS
    # ========================================================================
    
    def run_static_analysis(self, include_pdelta: bool = False,
                           pdelta_iterations: int = 10,
                           pdelta_tolerance: float = 0.001) -> AnalysisResults:
        """
        Run static linear analysis
        
        Args:
            include_pdelta: Include P-Delta effects
            pdelta_iterations: Max iterations for P-Delta
            pdelta_tolerance: Convergence tolerance for P-Delta
            
        Returns:
            AnalysisResults object
        """
        # Validate prerequisites
        if not self._geometry_ready:
            is_valid, errors = self.validate_geometry()
            if not is_valid:
                raise ValueError(f"Invalid geometry: {errors}")
                
        if not self._materials_ready:
            raise ValueError("Materials not defined. Call add_material first.")
            
        if not self._loads_ready:
            raise ValueError("No loads applied. Call apply_nodal_load first.")
        
        # Initialize analyzer if needed
        if self.analyzer is None:
            self.analyzer = StructuralAnalysis(self.geometry)
            
        # Step 1: Assemble stiffness matrix
        if not self._stiffness_assembled:
            print("  → Assembling stiffness matrix...")
            K = self.analyzer.assemble_stiffness_matrix(
                self.geometry.materials,
                self.geometry.sections
            )
            self._stiffness_assembled = True
            print(f"  ✓ Stiffness matrix: {K.shape[0]}×{K.shape[1]}")
        
        # Step 2: Build load vector
        print("  → Building load vector...")
        n_dof = len(self.geometry.nodes) * 6
        loads = np.zeros(n_dof)
        
        for node_id, node in self.geometry.nodes.items():
            if hasattr(node, 'loads') and node.loads:
                base_dof = node_id * 6
                for i, load_val in enumerate(node.loads):
                    loads[base_dof + i] = load_val
        
        print(f"  ✓ Load vector: {len(loads)} DOF")
        
        # Step 3: Prepare restraints
        print("  → Preparing restraints...")
        restraints = {}
        for node_id, node in self.geometry.nodes.items():
            if hasattr(node, 'restraints') and node.restraints:
                restraints[node_id] = node.restraints
        
        print(f"  ✓ Restraints: {len(restraints)} nodes")
        
        # Step 4: Solve
        print("  → Solving system...")
        results = self.analyzer.static_analysis(loads, restraints)
        print("  ✓ Solution converged")
        
        # Package results first
        max_disp = np.max(np.abs(results['displacements']))
        total_reaction = np.sum(np.abs(results['reactions']))
        
        # Step 5: P-Delta analysis if requested
        pdelta_factor = 1.0
        if include_pdelta:
            print("  → Running P-Delta analysis...")
            if self.pdelta_engine is None:
                self.pdelta_engine = PDeltaAnalysis(
                    tolerance=pdelta_tolerance,
                    max_iterations=pdelta_iterations
                )
            
            # For simplified P-Delta, calculate amplification factor
            # Using stability index approach
            # This is a simplified implementation - full P-Delta would need iteration
            story_height = 3500  # mm (typical)
            
            # Estimate story shear and weight from reactions
            story_shear = np.sum(np.abs(results['reactions'])) * 0.1  # Simplified
            story_weight = np.sum(np.abs(results['reactions']))
            
            if story_weight > 0 and story_height > 0:
                stability_result = self.pdelta_engine.stability_index(
                    story_shear=story_shear,
                    story_weight=story_weight,
                    story_drift=max_disp,
                    story_height=story_height
                )
                pdelta_factor = stability_result.get('amplification_factor', 1.0)
            else:
                pdelta_factor = 1.0
                
            print(f"  ✓ P-Delta factor: {pdelta_factor:.3f}")
        
        analysis_results = AnalysisResults(
            displacements=results['displacements'],
            reactions=results['reactions'],
            member_forces=results['element_forces'],
            max_displacement=max_disp,
            total_reaction=total_reaction,
            status="success"
        )
        
        # Add warnings
        if pdelta_factor > 1.1:
            analysis_results.warnings.append(
                f"Significant P-Delta effects detected (factor={pdelta_factor:.3f})"
            )
        
        # Store results
        self.results['static'] = analysis_results
        
        return analysis_results
        
    def run_modal_analysis(self, n_modes: int = 10) -> Dict:
        """
        Run modal analysis
        
        Args:
            n_modes: Number of modes to extract
            
        Returns:
            Dict with frequencies and mode shapes
        """
        if not self._geometry_ready:
            raise ValueError("Geometry not ready. Call validate_geometry first.")
            
        if self.analyzer is None:
            self.analyzer = StructuralAnalysis(self.geometry)
            
        # Prepare restraints
        restraints = {}
        for node_id, node in self.geometry.nodes.items():
            if hasattr(node, 'restraints') and node.restraints:
                restraints[node_id] = node.restraints
        
        print("  → Running modal analysis...")
        modal_results = self.analyzer.modal_analysis(
            self.geometry.materials,
            self.geometry.sections,
            restraints,
            n_modes=n_modes
        )
        
        print(f"  ✓ Extracted {len(modal_results['frequencies'])} modes")
        
        self.results['modal'] = modal_results
        return modal_results
        
    # ========================================================================
    # DESIGN CHECK METHODS
    # ========================================================================
    
    def check_concrete_design(self, fck: float = 30, fy: float = 500) -> Dict:
        """
        Perform concrete design checks (IS 456)
        
        Args:
            fck: Characteristic concrete strength (MPa)
            fy: Characteristic steel strength (MPa)
            
        Returns:
            Dict with design check results
        """
        if 'static' not in self.results:
            raise ValueError("No analysis results. Run run_static_analysis first.")
            
        is456 = IS456ConcreteDesign()
        member_forces = self.results['static'].member_forces
        
        design_results = {
            'columns': [],
            'beams': [],
            'status': 'pass'
        }
        
        # Check each member (simplified)
        for elem_id, forces in member_forces.items():
            elem = self.geometry.elements[elem_id]
            
            if elem.element_type == 'column':
                # Simplified column check
                axial = abs(forces.get('axial', 0))
                moment = abs(forces.get('moment', 0))
                
                # Assume 450x450 column
                area = 450 * 450
                capacity = 0.4 * fck * area / 1000  # kN
                utilization = axial / capacity if capacity > 0 else 0
                
                design_results['columns'].append({
                    'element_id': elem_id,
                    'axial': axial,
                    'capacity': capacity,
                    'utilization': utilization,
                    'status': 'pass' if utilization <= 1.0 else 'fail'
                })
                
                if utilization > 1.0:
                    design_results['status'] = 'fail'
                    
            elif elem.element_type == 'beam':
                # Simplified beam check
                moment = abs(forces.get('moment', 0))
                shear = abs(forces.get('shear', 0))
                
                section = {'width': 300, 'effective_depth': 550}
                material = {'fck': fck, 'fy': fy}
                
                flexure_check = is456.check_flexure(moment, section, material)
                shear_check = is456.check_shear(shear, section, material)
                
                design_results['beams'].append({
                    'element_id': elem_id,
                    'moment': moment,
                    'shear': shear,
                    'flexure': flexure_check['status'],
                    'shear_check': shear_check['status']
                })
                
                if flexure_check['status'] != 'OK' or shear_check['status'] != 'OK':
                    design_results['status'] = 'fail'
        
        return design_results
        
    # ========================================================================
    # UTILITY METHODS
    # ========================================================================
    
    def get_model_info(self) -> Dict:
        """Get model information summary"""
        return {
            'nodes': len(self.geometry.nodes),
            'elements': len(self.geometry.elements),
            'materials': len(self.geometry.materials),
            'sections': len(self.geometry.sections),
            'load_cases': len(self.load_cases),
            'combinations': len(self.combinations),
            'geometry_ready': self._geometry_ready,
            'materials_ready': self._materials_ready,
            'loads_ready': self._loads_ready,
            'stiffness_assembled': self._stiffness_assembled
        }
        
    def reset(self) -> None:
        """Reset the workflow to initial state"""
        self.__init__()
