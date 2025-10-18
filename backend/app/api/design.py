from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Optional
import logging
from app.engine.design_codes.is456_concrete import IS456ConcreteDesign
from app.engine.design_codes.is800_steel import IS800SteelDesign

router = APIRouter()
logger = logging.getLogger(__name__)

class DesignRequest(BaseModel):
    model_config = {"protected_namespaces": ()}
    
    model_id: int
    design_code: str = Field(..., description="Design code: IS456, IS800, ACI318, AISC")
    element_type: str = Field(..., description="Element type: beam, column, foundation")
    forces: Dict = Field(..., description="Forces dict with M, V, N, T")
    geometry: Dict = Field(..., description="Geometry dict with b, d, L, etc.")
    material: Dict = Field(..., description="Material properties: fck/fy, fu")

class DesignResponse(BaseModel):
    model_config = {"protected_namespaces": ()}
    
    model_id: int
    design_code: str
    element_type: str
    reinforcement: Dict
    checks: Dict
    status: str

@router.post("/run", response_model=DesignResponse)
def run_design(request: DesignRequest):
    """
    Run design calculations using appropriate design code
    
    Supports:
    - IS456 concrete design
    - IS800 steel design
    - Automatic design based on forces and geometry
    """
    try:
        logger.info(f"Running {request.design_code} design for {request.element_type}")
        
        if request.design_code == "IS456":
            # Concrete design
            fck = request.material.get('fck', 25)
            fy = request.material.get('fy', 415)
            designer = IS456ConcreteDesign(fck, fy)
            
            # Extract forces
            M = request.forces.get('M', 0)
            V = request.forces.get('V', 0)
            T = request.forces.get('T', 0)
            
            # Extract geometry
            b = request.geometry.get('b', 300)
            d = request.geometry.get('d', 500)
            D = request.geometry.get('D', d + 50)
            
            # Flexural design
            flex_result = designer.flexural_design_singly_reinforced(M, b, d)
            
            # Shear design
            Ast = flex_result.get('Ast_required', 1000)
            shear_result = designer.shear_design(V, b, d, Ast)
            
            # Torsion design (if applicable)
            if T > 0:
                torsion_result = designer.torsion_design(T, b, D, Ast)
            else:
                torsion_result = {'status': 'not_applicable'}
            
            # Compile reinforcement
            reinforcement = {
                "main_bars": flex_result.get('bar_arrangement', {}),
                "Ast_required": flex_result.get('Ast_required', 0),
                "stirrups": shear_result.get('stirrup_arrangement', {}),
                "torsion_steel": torsion_result.get('Asl_torsion', 0) if T > 0 else 0
            }
            
            # Compile checks
            checks = {
                "flexure": "OK" if flex_result.get('design_ok') else "FAIL",
                "shear": "OK" if shear_result.get('design_ok') else "FAIL",
                "torsion": "OK" if torsion_result.get('design_ok', True) else "FAIL",
                "utilization_ratio": flex_result.get('utilization_ratio', 0)
            }
            
            status = "design_ok" if all(v == "OK" for v in checks.values() if v in ["OK", "FAIL"]) else "inadequate"
            
        elif request.design_code == "IS800":
            # Steel design
            fy = request.material.get('fy', 250)
            fu = request.material.get('fu', 410)
            designer = IS800SteelDesign(fy, fu)
            
            # Extract forces
            N = request.forces.get('N', 0)
            M = request.forces.get('M', 0)
            V = request.forces.get('V', 0)
            
            # Extract geometry/section
            section = request.geometry.get('section', {})
            L = request.geometry.get('L', 4000)
            
            # Design based on element type
            if request.element_type == 'column' or N > 0:
                result = designer.compression_member_design(abs(N), L, section)
            elif request.element_type == 'beam':
                result = designer.beam_design(M, V, section)
            else:
                result = designer.tension_member_design(abs(N), section.get('A', 2400), section.get('A', 2400) * 0.9)
            
            reinforcement = {
                "section_adequate": result.get('design_ok', False),
                "capacity": result.get('Pd_capacity', result.get('Md_capacity', result.get('Td_capacity', 0))),
                "utilization_ratio": result.get('utilization_ratio', 0)
            }
            
            checks = {
                "strength": "OK" if result.get('design_ok') else "FAIL",
                "slenderness": "OK" if result.get('lambda_max', 0) <= 180 else "FAIL"
            }
            
            status = result.get('status', 'unknown')
            
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported design code: {request.design_code}")
        
        logger.info(f"Design completed: {status}")
        
        return DesignResponse(
            model_id=request.model_id,
            design_code=request.design_code,
            element_type=request.element_type,
            reinforcement=reinforcement,
            checks=checks,
            status=status
        )
        
    except Exception as e:
        logger.error(f"Design failed: {e}")
        raise HTTPException(status_code=500, detail=f"Design failed: {str(e)}")
