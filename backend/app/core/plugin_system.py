"""
Plugin system for extensibility
"""
from typing import Dict, List, Callable, Any, Optional
from abc import ABC, abstractmethod
import importlib
import inspect
from pathlib import Path
import json


class PluginInterface(ABC):
    """Base interface for all plugins"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name"""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Plugin version"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Plugin description"""
        pass
    
    @abstractmethod
    def initialize(self):
        """Initialize plugin"""
        pass
    
    @abstractmethod
    def shutdown(self):
        """Cleanup plugin resources"""
        pass


class AnalysisPlugin(PluginInterface):
    """Plugin for custom analysis methods"""
    
    @abstractmethod
    def analyze(self, model_data: dict, parameters: dict) -> dict:
        """
        Perform custom analysis
        
        Args:
            model_data: Structural model data
            parameters: Analysis parameters
        
        Returns:
            Analysis results
        """
        pass
    
    @abstractmethod
    def validate_input(self, model_data: dict, parameters: dict) -> bool:
        """Validate input data"""
        pass


class DesignPlugin(PluginInterface):
    """Plugin for custom design codes"""
    
    @abstractmethod
    def design(self, element_data: dict, forces: dict, parameters: dict) -> dict:
        """
        Perform custom design
        
        Args:
            element_data: Element properties
            forces: Applied forces
            parameters: Design parameters
        
        Returns:
            Design results
        """
        pass
    
    @abstractmethod
    def get_design_code(self) -> str:
        """Return design code name (e.g., 'ACI 318-19')"""
        pass


class ReportPlugin(PluginInterface):
    """Plugin for custom report formats"""
    
    @abstractmethod
    def generate_report(self, data: dict, template: str) -> bytes:
        """
        Generate custom report
        
        Args:
            data: Report data
            template: Template name
        
        Returns:
            Report file content
        """
        pass
    
    @abstractmethod
    def get_supported_formats(self) -> List[str]:
        """Return supported output formats"""
        pass


class PluginManager:
    """Manages plugin lifecycle and registration"""
    
    def __init__(self, plugin_dir: str = "plugins"):
        self.plugin_dir = Path(plugin_dir)
        self.plugins: Dict[str, PluginInterface] = {}
        self.plugin_types: Dict[str, List[str]] = {
            "analysis": [],
            "design": [],
            "report": [],
            "other": []
        }
        self.hooks: Dict[str, List[Callable]] = {}
    
    def register_plugin(self, plugin: PluginInterface):
        """Register a plugin"""
        plugin_name = plugin.name
        
        if plugin_name in self.plugins:
            raise ValueError(f"Plugin '{plugin_name}' already registered")
        
        # Initialize plugin
        plugin.initialize()
        
        # Store plugin
        self.plugins[plugin_name] = plugin
        
        # Categorize plugin
        if isinstance(plugin, AnalysisPlugin):
            self.plugin_types["analysis"].append(plugin_name)
        elif isinstance(plugin, DesignPlugin):
            self.plugin_types["design"].append(plugin_name)
        elif isinstance(plugin, ReportPlugin):
            self.plugin_types["report"].append(plugin_name)
        else:
            self.plugin_types["other"].append(plugin_name)
        
        print(f"Plugin registered: {plugin_name} v{plugin.version}")
    
    def unregister_plugin(self, plugin_name: str):
        """Unregister a plugin"""
        if plugin_name not in self.plugins:
            raise ValueError(f"Plugin '{plugin_name}' not found")
        
        plugin = self.plugins[plugin_name]
        
        # Cleanup
        plugin.shutdown()
        
        # Remove from registry
        del self.plugins[plugin_name]
        
        # Remove from type lists
        for plugin_list in self.plugin_types.values():
            if plugin_name in plugin_list:
                plugin_list.remove(plugin_name)
    
    def get_plugin(self, plugin_name: str) -> Optional[PluginInterface]:
        """Get a plugin by name"""
        return self.plugins.get(plugin_name)
    
    def get_plugins_by_type(self, plugin_type: str) -> List[PluginInterface]:
        """Get all plugins of a specific type"""
        plugin_names = self.plugin_types.get(plugin_type, [])
        return [self.plugins[name] for name in plugin_names]
    
    def list_plugins(self) -> List[dict]:
        """List all registered plugins"""
        return [
            {
                "name": plugin.name,
                "version": plugin.version,
                "description": plugin.description,
                "type": self._get_plugin_type(plugin)
            }
            for plugin in self.plugins.values()
        ]
    
    def load_plugins_from_directory(self):
        """Load plugins from plugin directory"""
        if not self.plugin_dir.exists():
            self.plugin_dir.mkdir(parents=True)
            return
        
        # Look for plugin files
        for plugin_file in self.plugin_dir.glob("*.py"):
            if plugin_file.name.startswith("_"):
                continue
            
            try:
                # Import plugin module
                module_name = plugin_file.stem
                spec = importlib.util.spec_from_file_location(module_name, plugin_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Find plugin classes
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        issubclass(obj, PluginInterface) and 
                        obj != PluginInterface):
                        
                        # Instantiate and register
                        plugin_instance = obj()
                        self.register_plugin(plugin_instance)
            
            except Exception as e:
                print(f"Failed to load plugin {plugin_file}: {e}")
    
    def register_hook(self, hook_name: str, callback: Callable):
        """Register a hook callback"""
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        
        self.hooks[hook_name].append(callback)
    
    def trigger_hook(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """Trigger all callbacks for a hook"""
        if hook_name not in self.hooks:
            return []
        
        results = []
        for callback in self.hooks[hook_name]:
            try:
                result = callback(*args, **kwargs)
                results.append(result)
            except Exception as e:
                print(f"Hook callback failed: {e}")
        
        return results
    
    def _get_plugin_type(self, plugin: PluginInterface) -> str:
        """Determine plugin type"""
        if isinstance(plugin, AnalysisPlugin):
            return "analysis"
        elif isinstance(plugin, DesignPlugin):
            return "design"
        elif isinstance(plugin, ReportPlugin):
            return "report"
        else:
            return "other"
    
    def get_plugin_info(self, plugin_name: str) -> Optional[dict]:
        """Get detailed plugin information"""
        plugin = self.get_plugin(plugin_name)
        if not plugin:
            return None
        
        return {
            "name": plugin.name,
            "version": plugin.version,
            "description": plugin.description,
            "type": self._get_plugin_type(plugin),
            "methods": [
                method for method in dir(plugin)
                if not method.startswith("_") and callable(getattr(plugin, method))
            ]
        }


# Global plugin manager
plugin_manager = PluginManager()


# Example plugin implementations

class CustomSeismicPlugin(AnalysisPlugin):
    """Example: Custom seismic analysis plugin"""
    
    @property
    def name(self) -> str:
        return "custom_seismic"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def description(self) -> str:
        return "Custom seismic analysis method"
    
    def initialize(self):
        print(f"Initializing {self.name}")
    
    def shutdown(self):
        print(f"Shutting down {self.name}")
    
    def analyze(self, model_data: dict, parameters: dict) -> dict:
        # Custom seismic analysis implementation
        return {
            "method": "custom_seismic",
            "results": {},
            "success": True
        }
    
    def validate_input(self, model_data: dict, parameters: dict) -> bool:
        return "nodes" in model_data and "elements" in model_data


class CustomDesignCodePlugin(DesignPlugin):
    """Example: Custom design code plugin"""
    
    @property
    def name(self) -> str:
        return "custom_design_code"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def description(self) -> str:
        return "Custom design code implementation"
    
    def initialize(self):
        print(f"Initializing {self.name}")
    
    def shutdown(self):
        print(f"Shutting down {self.name}")
    
    def design(self, element_data: dict, forces: dict, parameters: dict) -> dict:
        # Custom design implementation
        return {
            "design_code": self.get_design_code(),
            "utilization_ratio": 0.85,
            "status": "adequate",
            "success": True
        }
    
    def get_design_code(self) -> str:
        return "CUSTOM-2025"
