"""
Linux AppLocker - Application Scanner
Scans system for installed applications by reading .desktop files
"""

import os
from pathlib import Path
from typing import List, Dict, Optional
import configparser


class AppScanner:
    """Scans system for installed applications"""
    
    DESKTOP_PATHS = [
        '/usr/share/applications',
        '/usr/local/share/applications',
        '~/.local/share/applications',
        '/var/lib/flatpak/exports/share/applications',
        '/var/lib/snapd/desktop/applications'
    ]
    
    def __init__(self):
        """Initialize app scanner"""
        pass
    
    def scan_applications(self) -> List[Dict[str, str]]:
        """
        Scan system for installed applications
        
        Returns:
            List of application dictionaries with name, exec, icon, desktop_file
        """
        applications = []
        seen_apps = set()
        
        for path in self.DESKTOP_PATHS:
            expanded_path = Path(path).expanduser()
            if not expanded_path.exists():
                continue
            
            for desktop_file in expanded_path.glob('*.desktop'):
                try:
                    app_info = self._parse_desktop_file(desktop_file)
                    if app_info and app_info['name'] not in seen_apps:
                        seen_apps.add(app_info['name'])
                        applications.append(app_info)
                except Exception as e:
                    # Skip files that can't be parsed
                    continue
        
        # Sort by name
        applications.sort(key=lambda x: x['name'].lower())
        
        return applications
    
    def _parse_desktop_file(self, desktop_file: Path) -> Optional[Dict[str, str]]:
        """
        Parse a .desktop file
        
        Args:
            desktop_file: Path to .desktop file
            
        Returns:
            Dictionary with app info or None if invalid
        """
        config = configparser.ConfigParser(interpolation=None)
        config.read(desktop_file, encoding='utf-8')
        
        if 'Desktop Entry' not in config:
            return None
        
        entry = config['Desktop Entry']
        
        # Skip if NoDisplay or Hidden
        if entry.get('NoDisplay', 'false').lower() == 'true':
            return None
        if entry.get('Hidden', 'false').lower() == 'true':
            return None
        
        # Get application info
        name = entry.get('Name', '')
        exec_cmd = entry.get('Exec', '')
        icon = entry.get('Icon', '')
        comment = entry.get('Comment', '')
        categories = entry.get('Categories', '')
        
        if not name or not exec_cmd:
            return None
        
        # Clean exec command (remove field codes)
        exec_cmd = self._clean_exec_command(exec_cmd)
        
        return {
            'name': name,
            'exec': exec_cmd,
            'icon': icon,
            'comment': comment,
            'categories': categories,
            'desktop_file': str(desktop_file)
        }
    
    def _clean_exec_command(self, exec_cmd: str) -> str:
        """
        Clean exec command by removing field codes (%f, %F, %u, %U, etc.)
        
        Args:
            exec_cmd: Raw exec command
            
        Returns:
            Cleaned exec command
        """
        # Remove field codes
        field_codes = ['%f', '%F', '%u', '%U', '%d', '%D', '%n', '%N', 
                      '%i', '%c', '%k', '%v', '%m']
        
        for code in field_codes:
            exec_cmd = exec_cmd.replace(code, '')
        
        # Remove extra spaces
        exec_cmd = ' '.join(exec_cmd.split())
        
        return exec_cmd.strip()
    
    def search_applications(self, query: str) -> List[Dict[str, str]]:
        """
        Search applications by name
        
        Args:
            query: Search query
            
        Returns:
            List of matching applications
        """
        all_apps = self.scan_applications()
        query_lower = query.lower()
        
        return [
            app for app in all_apps
            if query_lower in app['name'].lower() or 
               query_lower in app.get('comment', '').lower()
        ]
    
    def get_application_by_name(self, name: str) -> Optional[Dict[str, str]]:
        """
        Get application by exact name
        
        Args:
            name: Application name
            
        Returns:
            Application info or None
        """
        all_apps = self.scan_applications()
        for app in all_apps:
            if app['name'] == name:
                return app
        return None
    
    def get_executable_path(self, exec_cmd: str) -> str:
        """
        Extract executable path from exec command
        
        Args:
            exec_cmd: Exec command from .desktop file
            
        Returns:
            Executable path
        """
        # Split command and get first part
        parts = exec_cmd.split()
        if not parts:
            return exec_cmd
        
        executable = parts[0]
        
        # If it's an absolute path, return it
        if os.path.isabs(executable):
            return executable
        
        # Try to find in PATH
        import shutil
        path = shutil.which(executable)
        return path if path else executable
