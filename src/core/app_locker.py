"""
Linux AppLocker - Application Locker
Manages application locking functionality
"""

from typing import Optional, List
from ..database import DatabaseManager
from ..utils import Logger


class AppLocker:
    """Manages application locking"""
    
    def __init__(self, db_manager: DatabaseManager, logger: Optional[Logger] = None):
        """
        Initialize app locker
        
        Args:
            db_manager: Database manager instance
            logger: Logger instance
        """
        self.db = db_manager
        self.logger = logger or Logger()
    
    def lock_application(self, app_name: str, app_path: str,
                        desktop_file: Optional[str] = None,
                        icon_path: Optional[str] = None) -> bool:
        """
        Lock an application
        
        Args:
            app_name: Application name
            app_path: Application executable path
            desktop_file: Path to .desktop file
            icon_path: Path to application icon
            
        Returns:
            True if successful
        """
        try:
            # Check if already locked
            if self.is_locked(app_path):
                self.logger.warning(f"Application {app_name} is already locked")
                return False
            
            # Add to database
            self.db.add_locked_application(
                app_name=app_name,
                app_path=app_path,
                desktop_file=desktop_file,
                icon_path=icon_path
            )
            
            self.logger.info(f"Locked application: {app_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error locking application {app_name}: {e}")
            return False
    
    def unlock_application(self, app_id: int) -> bool:
        """
        Unlock an application
        
        Args:
            app_id: Application ID in database
            
        Returns:
            True if successful
        """
        try:
            success = self.db.remove_locked_application(app_id)
            if success:
                self.logger.info(f"Unlocked application ID: {app_id}")
            return success
        except Exception as e:
            self.logger.error(f"Error unlocking application {app_id}: {e}")
            return False
    
    def unlock_application_by_path(self, app_path: str) -> bool:
        """
        Unlock an application by its path
        
        Args:
            app_path: Application executable path
            
        Returns:
            True if successful
        """
        try:
            apps = self.get_locked_applications()
            for app in apps:
                if app.app_path == app_path:
                    return self.unlock_application(app.id)
            return False
        except Exception as e:
            self.logger.error(f"Error unlocking application by path {app_path}: {e}")
            return False
    
    def is_locked(self, app_path: str) -> bool:
        """
        Check if an application is locked
        
        Args:
            app_path: Application executable path
            
        Returns:
            True if locked
        """
        return self.db.is_application_locked(app_path)
    
    def get_locked_applications(self) -> List:
        """
        Get all locked applications
        
        Returns:
            List of locked application objects
        """
        return self.db.get_locked_applications(active_only=True)
    
    def get_locked_app_paths(self) -> List[str]:
        """
        Get list of locked application paths
        
        Returns:
            List of executable paths
        """
        apps = self.get_locked_applications()
        return [app.app_path for app in apps]
    
    def verify_access(self, app_path: str, password: str) -> bool:
        """
        Verify if access should be granted to a locked application
        This method should be overridden or connected to password verification
        
        Args:
            app_path: Application path
            password: Password to verify
            
        Returns:
            True if access granted
        """
        # This is a placeholder - actual password verification
        # should be done through the password manager
        return False
