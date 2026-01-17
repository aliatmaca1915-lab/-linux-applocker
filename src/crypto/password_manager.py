"""
Linux AppLocker - Password Manager
Manages master password hashing and verification using bcrypt
"""

import os
import bcrypt
from typing import Tuple, Optional


class PasswordManager:
    """Manages master password operations"""
    
    def __init__(self):
        """Initialize password manager"""
        self.rounds = 12  # bcrypt rounds (2^12 iterations)
    
    def hash_password(self, password: str) -> Tuple[str, str]:
        """
        Hash a password using bcrypt
        
        Args:
            password: Plain text password
            
        Returns:
            Tuple of (password_hash, salt)
        """
        # Generate salt
        salt = bcrypt.gensalt(rounds=self.rounds)
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode(), salt)
        
        return password_hash.decode(), salt.decode()
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """
        Verify a password against its hash
        
        Args:
            password: Plain text password to verify
            password_hash: Stored password hash
            
        Returns:
            True if password matches, False otherwise
        """
        try:
            return bcrypt.checkpw(password.encode(), password_hash.encode())
        except Exception:
            return False
    
    def validate_password_strength(self, password: str) -> Tuple[bool, str]:
        """
        Validate password strength
        
        Requirements:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - At least one special character
        
        Args:
            password: Password to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if len(password) < 8:
            return False, "Şifre en az 8 karakter olmalıdır"
        
        if not any(c.isupper() for c in password):
            return False, "Şifre en az bir büyük harf içermelidir"
        
        if not any(c.islower() for c in password):
            return False, "Şifre en az bir küçük harf içermelidir"
        
        if not any(c.isdigit() for c in password):
            return False, "Şifre en az bir rakam içermelidir"
        
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not any(c in special_chars for c in password):
            return False, "Şifre en az bir özel karakter içermelidir (!@#$%^&* vb.)"
        
        return True, ""
    
    def generate_salt(self) -> bytes:
        """Generate a random salt"""
        return os.urandom(16)
    
    def change_password(self, old_password: str, new_password: str,
                       stored_hash: str) -> Tuple[bool, Optional[Tuple[str, str]]]:
        """
        Change master password
        
        Args:
            old_password: Current password
            new_password: New password
            stored_hash: Stored hash of current password
            
        Returns:
            Tuple of (success, (new_hash, new_salt) or None)
        """
        # Verify old password
        if not self.verify_password(old_password, stored_hash):
            return False, None
        
        # Validate new password
        is_valid, error = self.validate_password_strength(new_password)
        if not is_valid:
            return False, None
        
        # Hash new password
        new_hash, new_salt = self.hash_password(new_password)
        
        return True, (new_hash, new_salt)
