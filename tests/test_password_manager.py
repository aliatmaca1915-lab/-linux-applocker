"""
Tests for Password Manager
"""

import pytest
from src.crypto.password_manager import PasswordManager


class TestPasswordManager:
    """Test password manager functionality"""
    
    def setup_method(self):
        """Setup test method"""
        self.password_manager = PasswordManager()
    
    def test_password_hashing(self):
        """Test password hashing"""
        password = "TestPassword123!"
        
        # Hash password
        password_hash, salt = self.password_manager.hash_password(password)
        
        # Verify hash and salt
        assert password_hash is not None
        assert salt is not None
        assert len(password_hash) > 0
        assert len(salt) > 0
    
    def test_password_verification(self):
        """Test password verification"""
        password = "TestPassword123!"
        
        # Hash password
        password_hash, salt = self.password_manager.hash_password(password)
        
        # Verify correct password
        assert self.password_manager.verify_password(password, password_hash) is True
        
        # Verify incorrect password
        assert self.password_manager.verify_password("WrongPassword", password_hash) is False
    
    def test_password_strength_validation(self):
        """Test password strength validation"""
        # Valid password
        valid_password = "TestPassword123!"
        is_valid, error = self.password_manager.validate_password_strength(valid_password)
        assert is_valid is True
        assert error == ""
        
        # Too short
        short_password = "Test1!"
        is_valid, error = self.password_manager.validate_password_strength(short_password)
        assert is_valid is False
        assert "8 karakter" in error
        
        # No uppercase
        no_upper = "testpassword123!"
        is_valid, error = self.password_manager.validate_password_strength(no_upper)
        assert is_valid is False
        assert "büyük harf" in error
        
        # No lowercase
        no_lower = "TESTPASSWORD123!"
        is_valid, error = self.password_manager.validate_password_strength(no_lower)
        assert is_valid is False
        assert "küçük harf" in error
        
        # No digit
        no_digit = "TestPassword!"
        is_valid, error = self.password_manager.validate_password_strength(no_digit)
        assert is_valid is False
        assert "rakam" in error
        
        # No special character
        no_special = "TestPassword123"
        is_valid, error = self.password_manager.validate_password_strength(no_special)
        assert is_valid is False
        assert "özel karakter" in error
    
    def test_password_change(self):
        """Test password change"""
        old_password = "OldPassword123!"
        new_password = "NewPassword456!"
        
        # Hash old password
        old_hash, old_salt = self.password_manager.hash_password(old_password)
        
        # Change password
        success, result = self.password_manager.change_password(
            old_password, new_password, old_hash
        )
        
        # Verify change was successful
        assert success is True
        assert result is not None
        
        new_hash, new_salt = result
        assert new_hash != old_hash
        
        # Verify new password works
        assert self.password_manager.verify_password(new_password, new_hash) is True
        
        # Verify old password doesn't work
        assert self.password_manager.verify_password(old_password, new_hash) is False
    
    def test_password_change_with_wrong_old_password(self):
        """Test password change with wrong old password"""
        old_password = "OldPassword123!"
        wrong_old_password = "WrongPassword123!"
        new_password = "NewPassword456!"
        
        # Hash old password
        old_hash, old_salt = self.password_manager.hash_password(old_password)
        
        # Try to change password with wrong old password
        success, result = self.password_manager.change_password(
            wrong_old_password, new_password, old_hash
        )
        
        # Verify change failed
        assert success is False
        assert result is None
