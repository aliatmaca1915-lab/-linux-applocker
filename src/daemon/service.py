"""
Linux AppLocker - Daemon Service
Background service for monitoring locked applications
"""

import time
import signal
import sys
from pathlib import Path

from ..database import DatabaseManager
from ..core import ProcessMonitor
from ..utils import Logger, Config


class DaemonService:
    """Background daemon service"""
    
    def __init__(self):
        """Initialize daemon service"""
        self.config = Config()
        self.logger = Logger(log_dir=self.config.log_dir)
        self.db = DatabaseManager()
        self.process_monitor = ProcessMonitor(
            self.db,
            self.logger,
            check_interval=self.config.get('process_monitor_interval', 1)
        )
        
        self.running = False
        
        # Setup signal handlers
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle termination signals"""
        self.logger.info(f"Received signal {signum}, shutting down...")
        self.stop()
    
    def start(self):
        """Start daemon service"""
        self.logger.info("Starting Linux AppLocker daemon...")
        
        # Start process monitor
        self.process_monitor.start_monitoring()
        
        self.running = True
        self.logger.info("Daemon started successfully")
    
    def stop(self):
        """Stop daemon service"""
        self.logger.info("Stopping daemon...")
        
        self.running = False
        
        # Stop process monitor
        if self.process_monitor:
            self.process_monitor.stop_monitoring()
        
        self.logger.info("Daemon stopped")
    
    def run(self):
        """Run daemon (blocking)"""
        self.start()
        
        try:
            # Keep daemon running
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Keyboard interrupt received")
        finally:
            self.stop()


def main():
    """Main entry point for daemon"""
    daemon = DaemonService()
    daemon.run()


if __name__ == '__main__':
    main()
