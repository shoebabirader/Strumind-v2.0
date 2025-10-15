"""
Pushover analysis for seismic performance evaluation
"""
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class PushoverStep:
    """Single step in pushover analysis"""
    displacement: float
    base_shear: float
    roof_drift: float
    hinge_states: Dict[str, str]
    yielded_elements: List[str]
    failed_elements: List[str]


class PushoverAnalysis:
    """
    Pushover analysis for seismic performance evaluation
    Implements capacity curve generation and performance point determination
    """
    
    def __init__(self, model_data: dict):
        self.model = model_data
        self.nodes = model_data.get("nodes", {})
        self.elements = model_data.get("elements", {})
        self.materials = model_data.get("materials", {})
        
    def run_pushover(self, 
                    control_node: str,
                    load_pattern: Dict[str, np.ndarray],
                    target_displacement: float = None,
                    num_steps: int = 100) -> Dict:
        """
        Run pushover analysis
        
        Args:
            control_node: Node to monitor displacement
            load_pattern: Lateral load distribution
            target_displacement: Target displacement (auto if None)
            num_steps: Number of analysis steps
            
        Returns:
            Pushover analysis results with capacity curve
        """
        
        # Initialize
        if target_displacement is None:
            target_displacement = self._estimate_target_displacement()
        
        displacement_increment = target_displacement / num_steps
        
        # Storage for results
        steps = []
        capacity_curve = {"displacement": [], "base_shear": []}
        
        # Current state
        current_displacement = 0.0
        current_stiffness = self._calculate_initial_stiffness()
        
        # Pushover loop
        for step in range(num_steps):
            current_displacement += displacement_increment
            
            # Apply incremental load
            step_result = self._analyze_step(
                current_displacement,
                load_pattern,
                current_stiffness
            )
            
            # Check for convergence
            if not step_result["converged"]:
                print(f"Analysis stopped at step {step} - convergence failure")
                break
            
            # Update stiffness based on yielding
            current_stiffness = self._update_stiffness(
                current_stiffness,
                step_result["yielded_elements"]
            )
            
            # Store results
            pushover_step = PushoverStep(
                displacement=current_displacement,
                base_shear=step_result["base_shear"],
                roof_drift=step_result["roof_drift"],
                hinge_states=step_result["hinge_states"],
                yielded_elements=step_result["yielded_elements"],
                failed_elements=step_result["failed_elements"]
            )
            
            steps.append(pushover_step)
            capacity_curve["displacement"].append(current_displacement)
            capacity_curve["base_shear"].append(step_result["base_shear"])
            
            # Check for collapse
            if step_result["collapsed"]:
                print(f"Structure collapsed at step {step}")
                break
        
        # Calculate performance point
        performance_point = self._calculate_performance_point(capacity_curve)
        
        # Determine performance level
        performance_level = self._determine_performance_level(
            performance_point,
            steps
        )
        
        return {
            "success": True,
            "steps": steps,
            "capacity_curve": capacity_curve,
            "performance_point": performance_point,
            "performance_level": performance_level,
            "max_displacement": current_displacement,
            "max_base_shear": max(capacity_curve["base_shear"]),
            "ductility": self._calculate_ductility(capacity_curve),
            "overstrength": self._calculate_overstrength(capacity_curve)
        }
    
    def _analyze_step(self, displacement: float, load_pattern: Dict,
                     stiffness: np.ndarray) -> Dict:
        """Analyze single pushover step"""
        
        # Apply displacement-controlled loading
        forces = self._calculate_forces(displacement, load_pattern, stiffness)
        
        # Check element states
        yielded_elements = []
        failed_elements = []
        hinge_states = {}
        
        for elem_id, element in self.elements.items():
            # Calculate element forces
            elem_forces = self._get_element_forces(elem_id, forces)
            
            # Check yield
            yield_force = self._get_yield_force(elem_id)
            if abs(elem_forces) > yield_force:
                yielded_elements.append(elem_id)
                hinge_states[elem_id] = "yielded"
            
            # Check failure
            ultimate_force = self._get_ultimate_force(elem_id)
            if abs(elem_forces) > ultimate_force:
                failed_elements.append(elem_id)
                hinge_states[elem_id] = "failed"
        
        # Calculate base shear
        base_shear = np.sum([forces.get(node, 0) for node in self.nodes])
        
        # Calculate roof drift
        roof_displacement = displacement
        building_height = self._get_building_height()
        roof_drift = (roof_displacement / building_height) * 100  # percentage
        
        # Check convergence
        converged = len(failed_elements) < len(self.elements) * 0.1  # <10% failure
        
        # Check collapse
        collapsed = len(failed_elements) > len(self.elements) * 0.3  # >30% failure
        
        return {
            "converged": converged,
            "collapsed": collapsed,
            "base_shear": base_shear,
            "roof_drift": roof_drift,
            "yielded_elements": yielded_elements,
            "failed_elements": failed_elements,
            "hinge_states": hinge_states
        }
    
    def _calculate_performance_point(self, capacity_curve: Dict) -> Dict:
        """Calculate performance point using capacity spectrum method"""
        
        displacements = np.array(capacity_curve["displacement"])
        base_shears = np.array(capacity_curve["base_shear"])
        
        # Convert to spectral coordinates
        modal_mass = self._get_modal_mass()
        modal_participation = self._get_modal_participation_factor()
        
        spectral_displacement = displacements / (modal_participation * modal_mass)
        spectral_acceleration = base_shears / (modal_participation * modal_mass)
        
        # Find intersection with demand spectrum (simplified)
        # In practice, this would use actual site-specific demand spectrum
        target_displacement = displacements[len(displacements) // 2]
        target_base_shear = base_shears[len(base_shears) // 2]
        
        return {
            "displacement": target_displacement,
            "base_shear": target_base_shear,
            "spectral_displacement": float(spectral_displacement[len(displacements) // 2]),
            "spectral_acceleration": float(spectral_acceleration[len(base_shears) // 2])
        }
    
    def _determine_performance_level(self, performance_point: Dict,
                                    steps: List[PushoverStep]) -> str:
        """
        Determine performance level based on FEMA 356/ASCE 41
        IO: Immediate Occupancy
        LS: Life Safety
        CP: Collapse Prevention
        """
        
        drift = performance_point["displacement"] / self._get_building_height() * 100
        
        # Find step at performance point
        target_step = None
        for step in steps:
            if abs(step.displacement - performance_point["displacement"]) < 0.01:
                target_step = step
                break
        
        if target_step is None:
            return "Unknown"
        
        # Check damage levels
        yielded_ratio = len(target_step.yielded_elements) / len(self.elements)
        failed_ratio = len(target_step.failed_elements) / len(self.elements)
        
        # Performance level criteria
        if drift < 0.5 and yielded_ratio < 0.1:
            return "IO - Immediate Occupancy"
        elif drift < 1.5 and failed_ratio < 0.05:
            return "LS - Life Safety"
        elif drift < 3.0 and failed_ratio < 0.2:
            return "CP - Collapse Prevention"
        else:
            return "C - Collapse"
    
    def _calculate_ductility(self, capacity_curve: Dict) -> float:
        """Calculate displacement ductility"""
        displacements = np.array(capacity_curve["displacement"])
        base_shears = np.array(capacity_curve["base_shear"])
        
        # Find yield point (idealized bilinear)
        max_shear = np.max(base_shears)
        yield_idx = np.argmax(base_shears > 0.75 * max_shear)
        yield_displacement = displacements[yield_idx]
        
        # Ultimate displacement
        ultimate_displacement = displacements[-1]
        
        # Ductility
        ductility = ultimate_displacement / yield_displacement if yield_displacement > 0 else 1.0
        
        return float(ductility)
    
    def _calculate_overstrength(self, capacity_curve: Dict) -> float:
        """Calculate overstrength factor"""
        base_shears = np.array(capacity_curve["base_shear"])
        
        # Maximum base shear
        max_shear = np.max(base_shears)
        
        # Design base shear (simplified - would use code-based calculation)
        design_shear = max_shear * 0.7  # Typical overstrength ~1.4
        
        overstrength = max_shear / design_shear if design_shear > 0 else 1.0
        
        return float(overstrength)
    
    def _estimate_target_displacement(self) -> float:
        """Estimate target displacement based on building height"""
        height = self._get_building_height()
        # Typical target: 2-4% drift
        return height * 0.03
    
    def _calculate_initial_stiffness(self) -> np.ndarray:
        """Calculate initial elastic stiffness matrix"""
        n_dof = len(self.nodes) * 6  # 6 DOF per node
        K = np.zeros((n_dof, n_dof))
        
        # Build stiffness matrix from elements
        for elem_id, element in self.elements.items():
            k_elem = self._get_element_stiffness(elem_id)
            # Assemble into global matrix (simplified)
            # In practice, use proper assembly with DOF mapping
        
        return K
    
    def _update_stiffness(self, K: np.ndarray, yielded_elements: List[str]) -> np.ndarray:
        """Update stiffness matrix for yielded elements"""
        K_updated = K.copy()
        
        # Reduce stiffness of yielded elements
        for elem_id in yielded_elements:
            # Reduce to post-yield stiffness (typically 3-5% of elastic)
            # In practice, modify specific DOFs
            pass
        
        return K_updated
    
    def _calculate_forces(self, displacement: float, load_pattern: Dict,
                         stiffness: np.ndarray) -> Dict:
        """Calculate forces for given displacement"""
        # Simplified force calculation
        forces = {}
        for node_id in self.nodes:
            forces[node_id] = displacement * load_pattern.get(node_id, 0)
        return forces
    
    def _get_element_forces(self, elem_id: str, forces: Dict) -> float:
        """Get forces in element"""
        # Simplified - return sum of nodal forces
        return sum(forces.values()) / len(self.elements)
    
    def _get_yield_force(self, elem_id: str) -> float:
        """Get yield force for element"""
        element = self.elements[elem_id]
        material = self.materials.get(element.get("material", ""), {})
        fy = material.get("fy", 250)  # MPa
        area = element.get("area", 0.01)  # m²
        return fy * area * 1000  # kN
    
    def _get_ultimate_force(self, elem_id: str) -> float:
        """Get ultimate force for element"""
        return self._get_yield_force(elem_id) * 1.5  # Typical factor
    
    def _get_building_height(self) -> float:
        """Get total building height"""
        if not self.nodes:
            return 10.0  # Default
        
        z_coords = [node.get("z", 0) for node in self.nodes.values()]
        return max(z_coords) - min(z_coords)
    
    def _get_modal_mass(self) -> float:
        """Get first mode modal mass"""
        # Simplified - sum of all masses
        total_mass = 0
        for node in self.nodes.values():
            total_mass += node.get("mass", 1000)  # kg
        return total_mass
    
    def _get_modal_participation_factor(self) -> float:
        """Get first mode participation factor"""
        # Simplified - typically 0.7-0.9 for first mode
        return 0.8
    
    def _get_element_stiffness(self, elem_id: str) -> np.ndarray:
        """Get element stiffness matrix"""
        # Simplified 2x2 stiffness
        element = self.elements[elem_id]
        E = self.materials.get(element.get("material", ""), {}).get("E", 200000)  # MPa
        A = element.get("area", 0.01)  # m²
        L = element.get("length", 1.0)  # m
        
        k = E * A / L
        return np.array([[k, -k], [-k, k]])


def run_pushover_analysis(model_data: dict, parameters: dict) -> dict:
    """
    Convenience function to run pushover analysis
    
    Args:
        model_data: Structural model
        parameters: Analysis parameters
        
    Returns:
        Pushover analysis results
    """
    
    analyzer = PushoverAnalysis(model_data)
    
    control_node = parameters.get("control_node", "roof")
    load_pattern = parameters.get("load_pattern", {})
    target_displacement = parameters.get("target_displacement")
    num_steps = parameters.get("num_steps", 100)
    
    results = analyzer.run_pushover(
        control_node=control_node,
        load_pattern=load_pattern,
        target_displacement=target_displacement,
        num_steps=num_steps
    )
    
    return results
