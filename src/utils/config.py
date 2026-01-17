"""
Linux AppLocker - Configuration Manager
Manages application configuration and settings
"""

import os
import json
from pathlib import Path
from typing import Any, Optional, Dict


class Config:
    """Application configuration manager"""
    
    DEFAULT_CONFIG = {
        'auto_lock_timeout': 300,  # 5 minutes
        'theme': 'auto',  # auto, light, dark
        'notifications_enabled': True,
        'start_on_boot': False,
        'language': 'tr',
        'brute_force_timeout': 30,  # seconds
        'max_failed_attempts': 3,
        'process_monitor_interval': 1,  # seconds
        'log_level': 'INFO'
    }
    
    def __init__(self):
        """Initialize configuration"""
        self.config_dir = Path.home() / '.config' / 'linux-applocker'
        self.config_file = self.config_dir / 'config.json'
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults
                    config = self.DEFAULT_CONFIG.copy()
                    config.update(loaded_config)
                    return config
            except Exception as e:
                print(f"Error loading config: {e}")
                return self.DEFAULT_CONFIG.copy()
        else:
            # Create default config file
            self._save_config(self.DEFAULT_CONFIG)
            return self.DEFAULT_CONFIG.copy()
    
    def _save_config(self, config: Dict[str, Any]):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set a configuration value"""
        self._config[key] = value
        self._save_config(self._config)
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values"""
        return self._config.copy()
    
    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        self._config = self.DEFAULT_CONFIG.copy()
        self._save_config(self._config)
    
    @property
    def data_dir(self) -> Path:
        """Get data directory path"""
        data_dir = Path.home() / '.local' / 'share' / 'linux-applocker'
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir
    
    @property
    def log_dir(self) -> Path:
        """Get log directory path"""
        log_dir = self.data_dir / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir
