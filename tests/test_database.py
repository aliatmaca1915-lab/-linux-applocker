"""
Tests for Database Manager
"""

import os
import tempfile
import pytest
from src.database.db_manager import DatabaseManager


class TestDatabaseManager:
    """Test database manager functionality"""
    
    def setup_method(self):
        """Setup test method"""
        # Create temporary database
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db = DatabaseManager(db_path=self.temp_db.name)
    
    def teardown_method(self):
        """Cleanup after test"""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_master_password_operations(self):
        """Test master password database operations"""
        # Set master password
        password_hash = "test_hash_123"
        salt = "test_salt_456"
        
        result = self.db.set_master_password(password_hash, salt)
        
        assert result is not None
        assert result.password_hash == password_hash
        assert result.salt == salt
        
        # Get master password
        master_pwd = self.db.get_master_password()
        
        assert master_pwd is not None
        assert master_pwd.password_hash == password_hash
        assert master_pwd.salt == salt
    
    def test_locked_applications_operations(self):
        """Test locked applications database operations"""
        # Add locked application
        app = self.db.add_locked_application(
            app_name="Firefox",
            app_path="/usr/bin/firefox",
            desktop_file="/usr/share/applications/firefox.desktop",
            icon_path="firefox"
        )
        
        assert app is not None
        assert app.app_name == "Firefox"
        assert app.app_path == "/usr/bin/firefox"
        
        # Get locked applications
        apps = self.db.get_locked_applications()
        assert len(apps) == 1
        assert apps[0].app_name == "Firefox"
        
        # Check if application is locked
        assert self.db.is_application_locked("/usr/bin/firefox") is True
        assert self.db.is_application_locked("/usr/bin/chrome") is False
        
        # Remove locked application
        success = self.db.remove_locked_application(app.id)
        assert success is True
        
        # Verify removal
        apps = self.db.get_locked_applications()
        assert len(apps) == 0
    
    def test_encrypted_files_operations(self):
        """Test encrypted files database operations"""
        # Add encrypted file
        file = self.db.add_encrypted_file(
            original_path="/home/user/test.txt",
            encrypted_path="/home/user/test.txt.locked",
            encryption_key_id="key_123",
            file_size=1024
        )
        
        assert file is not None
        assert file.original_path == "/home/user/test.txt"
        assert file.encrypted_path == "/home/user/test.txt.locked"
        
        # Get encrypted files
        files = self.db.get_encrypted_files()
        assert len(files) == 1
        
        # Get by path
        file_by_path = self.db.get_encrypted_file_by_path("/home/user/test.txt.locked")
        assert file_by_path is not None
        assert file_by_path.original_path == "/home/user/test.txt"
        
        # Remove encrypted file
        success = self.db.remove_encrypted_file(file.id)
        assert success is True
        
        # Verify removal
        files = self.db.get_encrypted_files()
        assert len(files) == 0
    
    def test_access_logs_operations(self):
        """Test access logs database operations"""
        # Log access attempt
        log = self.db.log_access_attempt(
            resource_type="app",
            resource_name="Firefox",
            success=False
        )
        
        assert log is not None
        assert log.resource_type == "app"
        assert log.resource_name == "Firefox"
        assert log.success is False
        
        # Get access logs
        logs = self.db.get_access_logs(limit=10)
        assert len(logs) == 1
        
        # Get failed access count
        count = self.db.get_failed_access_count(minutes=5)
        assert count == 1
    
    def test_settings_operations(self):
        """Test settings database operations"""
        # Set setting
        setting = self.db.set_setting("theme", "dark")
        assert setting is not None
        assert setting.key == "theme"
        assert setting.value == "dark"
        
        # Get setting
        value = self.db.get_setting("theme")
        assert value == "dark"
        
        # Get setting with default
        value = self.db.get_setting("non_existent", "default_value")
        assert value == "default_value"
        
        # Update setting
        setting = self.db.set_setting("theme", "light")
        assert setting.value == "light"
        
        # Get all settings
        all_settings = self.db.get_all_settings()
        assert "theme" in all_settings
        assert all_settings["theme"] == "light"
    
    def test_statistics(self):
        """Test statistics"""
        # Add some data
        self.db.add_locked_application("App1", "/usr/bin/app1")
        self.db.add_locked_application("App2", "/usr/bin/app2")
        self.db.add_encrypted_file("/home/user/file1.txt", "/home/user/file1.txt.locked", "key1", 1024)
        self.db.log_access_attempt("app", "App1", False)
        
        # Get statistics
        stats = self.db.get_statistics()
        
        assert stats['locked_apps_count'] == 2
        assert stats['encrypted_files_count'] == 1
        assert stats['failed_attempts_today'] == 1
