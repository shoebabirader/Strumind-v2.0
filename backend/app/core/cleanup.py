"""
Cleanup Utilities
Manages temporary files, caches, and resource cleanup
"""
import os
import shutil
import logging
from pathlib import Path
from typing import List
from datetime import timedelta
from app.core.datetime_utils import utc_now

logger = logging.getLogger(__name__)


class CleanupManager:
    """
    Manages cleanup of temporary files and resources
    """
    
    def __init__(self, temp_dir: str = "temp", cache_dir: str = "cache"):
        self.temp_dir = Path(temp_dir)
        self.cache_dir = Path(cache_dir)
        self.temp_dir.mkdir(exist_ok=True)
        self.cache_dir.mkdir(exist_ok=True)
    
    def cleanup_old_files(self, directory: Path, max_age_hours: int = 24) -> int:
        """
        Remove files older than specified age
        
        Args:
            directory: Directory to clean
            max_age_hours: Maximum file age in hours
        
        Returns:
            Number of files removed
        """
        if not directory.exists():
            return 0
        
        removed_count = 0
        cutoff_time = utc_now() - timedelta(hours=max_age_hours)
        
        try:
            for file_path in directory.rglob('*'):
                if file_path.is_file():
                    # Get file modification time
                    mtime = file_path.stat().st_mtime
                    file_time = utc_now().fromtimestamp(mtime)
                    
                    if file_time < cutoff_time:
                        try:
                            file_path.unlink()
                            removed_count += 1
                            logger.debug(f"Removed old file: {file_path}")
                        except Exception as e:
                            logger.error(f"Error removing file {file_path}: {e}")
        
        except Exception as e:
            logger.error(f"Error cleaning directory {directory}: {e}")
        
        if removed_count > 0:
            logger.info(f"Cleaned {removed_count} old files from {directory}")
        
        return removed_count
    
    def cleanup_temp_files(self, max_age_hours: int = 24) -> int:
        """
        Clean up temporary files older than specified age
        
        Args:
            max_age_hours: Maximum file age in hours
        
        Returns:
            Number of files removed
        """
        return self.cleanup_old_files(self.temp_dir, max_age_hours)
    
    def cleanup_cache_files(self, max_age_hours: int = 168) -> int:
        """
        Clean up cache files older than specified age (default 7 days)
        
        Args:
            max_age_hours: Maximum file age in hours
        
        Returns:
            Number of files removed
        """
        return self.cleanup_old_files(self.cache_dir, max_age_hours)
    
    def cleanup_large_files(self, directory: Path, max_size_mb: int = 100) -> int:
        """
        Remove files larger than specified size
        
        Args:
            directory: Directory to clean
            max_size_mb: Maximum file size in MB
        
        Returns:
            Number of files removed
        """
        if not directory.exists():
            return 0
        
        removed_count = 0
        max_size_bytes = max_size_mb * 1024 * 1024
        
        try:
            for file_path in directory.rglob('*'):
                if file_path.is_file():
                    try:
                        if file_path.stat().st_size > max_size_bytes:
                            file_path.unlink()
                            removed_count += 1
                            logger.debug(f"Removed large file: {file_path}")
                    except Exception as e:
                        logger.error(f"Error removing file {file_path}: {e}")
        
        except Exception as e:
            logger.error(f"Error cleaning directory {directory}: {e}")
        
        if removed_count > 0:
            logger.info(f"Cleaned {removed_count} large files from {directory}")
        
        return removed_count
    
    def get_directory_size(self, directory: Path) -> float:
        """
        Get total size of directory in MB
        
        Args:
            directory: Directory to measure
        
        Returns:
            Size in MB
        """
        if not directory.exists():
            return 0.0
        
        total_size = 0
        try:
            for file_path in directory.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
        except Exception as e:
            logger.error(f"Error calculating directory size: {e}")
        
        return total_size / (1024 * 1024)  # Convert to MB
    
    def cleanup_empty_directories(self, directory: Path) -> int:
        """
        Remove empty directories
        
        Args:
            directory: Root directory to clean
        
        Returns:
            Number of directories removed
        """
        if not directory.exists():
            return 0
        
        removed_count = 0
        
        try:
            # Walk bottom-up to remove nested empty directories
            for dir_path in sorted(directory.rglob('*'), reverse=True):
                if dir_path.is_dir() and not any(dir_path.iterdir()):
                    try:
                        dir_path.rmdir()
                        removed_count += 1
                        logger.debug(f"Removed empty directory: {dir_path}")
                    except Exception as e:
                        logger.error(f"Error removing directory {dir_path}: {e}")
        
        except Exception as e:
            logger.error(f"Error cleaning empty directories: {e}")
        
        if removed_count > 0:
            logger.info(f"Cleaned {removed_count} empty directories")
        
        return removed_count
    
    def full_cleanup(self) -> dict:
        """
        Perform full cleanup of all managed directories
        
        Returns:
            Dictionary with cleanup statistics
        """
        stats = {
            'temp_files_removed': self.cleanup_temp_files(),
            'cache_files_removed': self.cleanup_cache_files(),
            'empty_dirs_removed': self.cleanup_empty_directories(self.temp_dir),
            'temp_size_mb': self.get_directory_size(self.temp_dir),
            'cache_size_mb': self.get_directory_size(self.cache_dir),
        }
        
        logger.info(f"Full cleanup completed: {stats}")
        return stats


# Global cleanup manager instance
cleanup_manager = CleanupManager()


def get_cleanup_manager() -> CleanupManager:
    """Get the global cleanup manager instance"""
    return cleanup_manager
