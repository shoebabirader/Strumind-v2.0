"""
Plugin management endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Dict, Any
from app.core.plugin_system import plugin_manager, AnalysisPlugin, DesignPlugin
from app.core.security import get_current_active_user, TokenData

router = APIRouter()


class PluginExecuteRequest(BaseModel):
    plugin_name: str
    method: str
    parameters: Dict[Any, Any]


@router.get("/plugins")
async def list_plugins(current_user: TokenData = Depends(get_current_active_user)):
    """List all registered plugins"""
    return {
        "plugins": plugin_manager.list_plugins(),
        "total": len(plugin_manager.plugins),
        "by_type": {
            plugin_type: len(plugins)
            for plugin_type, plugins in plugin_manager.plugin_types.items()
        }
    }


@router.get("/plugins/{plugin_name}")
async def get_plugin_info(
    plugin_name: str,
    current_user: TokenData = Depends(get_current_active_user)
):
    """Get detailed information about a specific plugin"""
    info = plugin_manager.get_plugin_info(plugin_name)
    
    if not info:
        raise HTTPException(status_code=404, detail=f"Plugin '{plugin_name}' not found")
    
    return info


@router.get("/plugins/type/{plugin_type}")
async def get_plugins_by_type(
    plugin_type: str,
    current_user: TokenData = Depends(get_current_active_user)
):
    """Get all plugins of a specific type"""
    plugins = plugin_manager.get_plugins_by_type(plugin_type)
    
    return {
        "type": plugin_type,
        "count": len(plugins),
        "plugins": [
            {
                "name": p.name,
                "version": p.version,
                "description": p.description
            }
            for p in plugins
        ]
    }


@router.post("/plugins/{plugin_name}/execute")
async def execute_plugin(
    plugin_name: str,
    request: PluginExecuteRequest,
    current_user: TokenData = Depends(get_current_active_user)
):
    """Execute a plugin method"""
    plugin = plugin_manager.get_plugin(plugin_name)
    
    if not plugin:
        raise HTTPException(status_code=404, detail=f"Plugin '{plugin_name}' not found")
    
    # Get the method
    if not hasattr(plugin, request.method):
        raise HTTPException(
            status_code=400,
            detail=f"Plugin '{plugin_name}' does not have method '{request.method}'"
        )
    
    method = getattr(plugin, request.method)
    
    try:
        # Execute method
        result = method(**request.parameters)
        
        return {
            "plugin": plugin_name,
            "method": request.method,
            "result": result,
            "success": True
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Plugin execution failed: {str(e)}"
        )


@router.post("/plugins/{plugin_name}/analysis")
async def run_plugin_analysis(
    plugin_name: str,
    model_data: Dict[Any, Any],
    parameters: Dict[Any, Any],
    current_user: TokenData = Depends(get_current_active_user)
):
    """Run analysis using a plugin"""
    plugin = plugin_manager.get_plugin(plugin_name)
    
    if not plugin:
        raise HTTPException(status_code=404, detail=f"Plugin '{plugin_name}' not found")
    
    if not isinstance(plugin, AnalysisPlugin):
        raise HTTPException(
            status_code=400,
            detail=f"Plugin '{plugin_name}' is not an analysis plugin"
        )
    
    # Validate input
    if not plugin.validate_input(model_data, parameters):
        raise HTTPException(status_code=400, detail="Invalid input data")
    
    # Run analysis
    try:
        result = plugin.analyze(model_data, parameters)
        return {
            "plugin": plugin_name,
            "analysis_type": "custom",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@router.post("/plugins/{plugin_name}/design")
async def run_plugin_design(
    plugin_name: str,
    element_data: Dict[Any, Any],
    forces: Dict[Any, Any],
    parameters: Dict[Any, Any],
    current_user: TokenData = Depends(get_current_active_user)
):
    """Run design using a plugin"""
    plugin = plugin_manager.get_plugin(plugin_name)
    
    if not plugin:
        raise HTTPException(status_code=404, detail=f"Plugin '{plugin_name}' not found")
    
    if not isinstance(plugin, DesignPlugin):
        raise HTTPException(
            status_code=400,
            detail=f"Plugin '{plugin_name}' is not a design plugin"
        )
    
    # Run design
    try:
        result = plugin.design(element_data, forces, parameters)
        return {
            "plugin": plugin_name,
            "design_code": plugin.get_design_code(),
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Design failed: {str(e)}"
        )


@router.post("/plugins/reload")
async def reload_plugins(current_user: TokenData = Depends(get_current_active_user)):
    """Reload plugins from plugin directory"""
    try:
        plugin_manager.load_plugins_from_directory()
        return {
            "message": "Plugins reloaded successfully",
            "plugins": plugin_manager.list_plugins()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to reload plugins: {str(e)}"
        )


@router.get("/plugins/hooks/list")
async def list_hooks(current_user: TokenData = Depends(get_current_active_user)):
    """List all registered hooks"""
    return {
        "hooks": list(plugin_manager.hooks.keys()),
        "total": len(plugin_manager.hooks)
    }


@router.post("/plugins/hooks/{hook_name}/trigger")
async def trigger_hook(
    hook_name: str,
    parameters: Dict[Any, Any],
    current_user: TokenData = Depends(get_current_active_user)
):
    """Trigger a hook"""
    results = plugin_manager.trigger_hook(hook_name, **parameters)
    
    return {
        "hook": hook_name,
        "callbacks_executed": len(results),
        "results": results
    }
