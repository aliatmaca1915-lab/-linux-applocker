"""
Linux AppLocker - Process Monitor
Monitors running processes and enforces application locks
"""

import time
import psutil
import signal
from typing import List, Optional, Callable, Set
from threading import Thread, Event
from ..database import DatabaseManager
from ..utils import Logger


class ProcessMonitor:
    """Monitors processes and enforces application locks"""
    
    def __init__(self, db_manager: DatabaseManager, 
                 logger: Optional[Logger] = None,
                 check_interval: int = 1):
        """
        Initialize process monitor
        
        Args:
            db_manager: Database manager instance
            logger: Logger instance
            check_interval: Interval between checks in seconds
        """
        self.db = db_manager
        self.logger = logger or Logger()
        self.check_interval = check_interval
        
        self._monitoring = False
        self._monitor_thread: Optional[Thread] = None
        self._stop_event = Event()
        self._password_callback: Optional[Callable] = None
        self._suspended_processes: Set[int] = set()
    
    def set_password_callback(self, callback: Callable):
        """
        Set callback function to request password
        
        Args:
            callback: Function that takes (app_name, app_path) and returns password or None
        """
        self._password_callback = callback
    
    def start_monitoring(self):
        """Start process monitoring"""
        if self._monitoring:
            self.logger.warning("Process monitoring already running")
            return
        
        self._monitoring = True
        self._stop_event.clear()
        self._monitor_thread = Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()
        self.logger.info("Process monitoring started")
    
    def stop_monitoring(self):
        """Stop process monitoring"""
        if not self._monitoring:
            return
        
        self._monitoring = False
        self._stop_event.set()
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5)
        self.logger.info("Process monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self._monitoring and not self._stop_event.is_set():
            try:
                self._check_processes()
            except Exception as e:
                self.logger.error(f"Error in monitor loop: {e}")
            
            # Wait for next check
            self._stop_event.wait(self.check_interval)
    
    def _check_processes(self):
        """Check running processes against locked applications"""
        # Get locked application paths
        locked_apps = self.db.get_locked_applications(active_only=True)
        if not locked_apps:
            return
        
        # Get all running processes
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
            try:
                proc_info = proc.info
                exe_path = proc_info.get('exe')
                
                if not exe_path:
                    continue
                
                # Check if this process is a locked application
                for locked_app in locked_apps:
                    if self._is_process_locked(exe_path, locked_app.app_path):
                        # Found a locked application running
                        self._handle_locked_process(proc, locked_app)
                        
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    
    def _is_process_locked(self, proc_path: str, locked_path: str) -> bool:
        """
        Check if process matches locked application
        
        Args:
            proc_path: Process executable path
            locked_path: Locked application path
            
        Returns:
            True if they match
        """
        # Simple path comparison
        if proc_path == locked_path:
            return True
        
        # Check if basename matches (for apps in PATH)
        import os
        if os.path.basename(proc_path) == os.path.basename(locked_path):
            return True
        
        return False
    
    def _handle_locked_process(self, proc: psutil.Process, locked_app):
        """
        Handle a locked process that's running
        
        Args:
            proc: Process object
            locked_app: Locked application database object
        """
        pid = proc.pid
        
        # Skip if already suspended
        if pid in self._suspended_processes:
            return
        
        try:
            # Suspend the process
            proc.suspend()
            self._suspended_processes.add(pid)
            
            self.logger.info(f"Suspended locked process: {locked_app.app_name} (PID: {pid})")
            
            # Log access attempt
            self.db.log_access_attempt(
                resource_type='app',
                resource_name=locked_app.app_name,
                success=False
            )
            
            # Request password if callback is set
            if self._password_callback:
                # This should be called in the main thread
                # For now, we'll just terminate the process
                pass
            
            # Terminate the process
            time.sleep(1)  # Give a moment for user to see
            proc.terminate()
            self._suspended_processes.discard(pid)
            
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            self.logger.error(f"Error handling locked process: {e}")
            self._suspended_processes.discard(pid)
    
    def resume_process(self, pid: int) -> bool:
        """
        Resume a suspended process
        
        Args:
            pid: Process ID
            
        Returns:
            True if successful
        """
        try:
            proc = psutil.Process(pid)
            proc.resume()
            self._suspended_processes.discard(pid)
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False
    
    def terminate_process(self, pid: int) -> bool:
        """
        Terminate a process
        
        Args:
            pid: Process ID
            
        Returns:
            True if successful
        """
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            self._suspended_processes.discard(pid)
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False
    
    def is_monitoring(self) -> bool:
        """Check if monitoring is active"""
        return self._monitoring
