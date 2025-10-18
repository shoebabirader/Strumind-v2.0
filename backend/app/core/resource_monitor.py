"""
Resource Monitoring and Management
Tracks and manages system resources to prevent leaks
"""
import psutil
import logging
from typing import Dict, Optional
from datetime import datetime
from app.core.datetime_utils import utc_now

logger = logging.getLogger(__name__)


class ResourceMonitor:
    """
    Monitor system resources and detect potential leaks
    """
    
    def __init__(self):
        self.process = psutil.Process()
        self.baseline_memory = None
        self.baseline_connections = None
        self.baseline_threads = None
        self.start_time = utc_now()
    
    def capture_baseline(self):
        """Capture baseline resource usage"""
        self.baseline_memory = self.get_memory_usage()
        self.baseline_connections = self.get_connection_count()
        self.baseline_threads = self.get_thread_count()
        logger.info(
            f"Resource baseline captured: "
            f"Memory={self.baseline_memory}MB, "
            f"Connections={self.baseline_connections}, "
            f"Threads={self.baseline_threads}"
        )
    
    def get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        try:
            memory_info = self.process.memory_info()
            return memory_info.rss / (1024 * 1024)  # Convert to MB
        except Exception as e:
            logger.error(f"Error getting memory usage: {e}")
            return 0.0
    
    def get_connection_count(self) -> int:
        """Get number of open connections"""
        try:
            connections = self.process.connections()
            return len(connections)
        except Exception as e:
            logger.error(f"Error getting connection count: {e}")
            return 0
    
    def get_thread_count(self) -> int:
        """Get number of threads"""
        try:
            return self.process.num_threads()
        except Exception as e:
            logger.error(f"Error getting thread count: {e}")
            return 0
    
    def get_cpu_percent(self) -> float:
        """Get CPU usage percentage"""
        try:
            return self.process.cpu_percent(interval=0.1)
        except Exception as e:
            logger.error(f"Error getting CPU usage: {e}")
            return 0.0
    
    def get_resource_stats(self) -> Dict:
        """Get comprehensive resource statistics"""
        stats = {
            'timestamp': utc_now().isoformat(),
            'uptime_seconds': (utc_now() - self.start_time).total_seconds(),
            'memory_mb': self.get_memory_usage(),
            'connections': self.get_connection_count(),
            'threads': self.get_thread_count(),
            'cpu_percent': self.get_cpu_percent(),
        }
        
        # Calculate deltas from baseline if available
        if self.baseline_memory is not None:
            stats['memory_delta_mb'] = stats['memory_mb'] - self.baseline_memory
            stats['connections_delta'] = stats['connections'] - self.baseline_connections
            stats['threads_delta'] = stats['threads'] - self.baseline_threads
        
        return stats
    
    def check_for_leaks(self, memory_threshold_mb: float = 500,
                       connection_threshold: int = 100,
                       thread_threshold: int = 50) -> Dict[str, bool]:
        """
        Check for potential resource leaks
        
        Args:
            memory_threshold_mb: Memory increase threshold in MB
            connection_threshold: Connection increase threshold
            thread_threshold: Thread increase threshold
        
        Returns:
            Dictionary of leak detection results
        """
        if self.baseline_memory is None:
            logger.warning("No baseline captured, cannot check for leaks")
            return {}
        
        stats = self.get_resource_stats()
        leaks = {}
        
        # Check memory leak
        if stats.get('memory_delta_mb', 0) > memory_threshold_mb:
            leaks['memory_leak'] = True
            logger.warning(
                f"Potential memory leak detected: "
                f"{stats['memory_delta_mb']:.2f}MB increase"
            )
        else:
            leaks['memory_leak'] = False
        
        # Check connection leak
        if stats.get('connections_delta', 0) > connection_threshold:
            leaks['connection_leak'] = True
            logger.warning(
                f"Potential connection leak detected: "
                f"{stats['connections_delta']} connections increase"
            )
        else:
            leaks['connection_leak'] = False
        
        # Check thread leak
        if stats.get('threads_delta', 0) > thread_threshold:
            leaks['thread_leak'] = True
            logger.warning(
                f"Potential thread leak detected: "
                f"{stats['threads_delta']} threads increase"
            )
        else:
            leaks['thread_leak'] = False
        
        return leaks
    
    def log_resource_usage(self):
        """Log current resource usage"""
        stats = self.get_resource_stats()
        logger.info(
            f"Resource usage: "
            f"Memory={stats['memory_mb']:.2f}MB, "
            f"Connections={stats['connections']}, "
            f"Threads={stats['threads']}, "
            f"CPU={stats['cpu_percent']:.1f}%"
        )


# Global resource monitor instance
resource_monitor = ResourceMonitor()


def get_resource_monitor() -> ResourceMonitor:
    """Get the global resource monitor instance"""
    return resource_monitor
