"""
Linux AppLocker - Password Validator
Validates password strength and requirements
"""

from typing import Tuple


class PasswordValidator:
    """Validates password strength"""
    
    MIN_LENGTH = 8
    SPECIAL_CHARS = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    @staticmethod
    def validate(password: str) -> Tuple[bool, str]:
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
        if len(password) < PasswordValidator.MIN_LENGTH:
            return False, f"Şifre en az {PasswordValidator.MIN_LENGTH} karakter olmalıdır"
        
        if not any(c.isupper() for c in password):
            return False, "Şifre en az bir büyük harf içermelidir"
        
        if not any(c.islower() for c in password):
            return False, "Şifre en az bir küçük harf içermelidir"
        
        if not any(c.isdigit() for c in password):
            return False, "Şifre en az bir rakam içermelidir"
        
        if not any(c in PasswordValidator.SPECIAL_CHARS for c in password):
            return False, f"Şifre en az bir özel karakter içermelidir ({PasswordValidator.SPECIAL_CHARS[:10]}...)"
        
        return True, ""
    
    @staticmethod
    def calculate_strength(password: str) -> int:
        """
        Calculate password strength (0-100)
        
        Args:
            password: Password to evaluate
            
        Returns:
            Strength score (0-100)
        """
        score = 0
        
        # Length score
        if len(password) >= 8:
            score += 20
        if len(password) >= 12:
            score += 10
        if len(password) >= 16:
            score += 10
        
        # Character variety
        if any(c.isupper() for c in password):
            score += 15
        if any(c.islower() for c in password):
            score += 15
        if any(c.isdigit() for c in password):
            score += 15
        if any(c in PasswordValidator.SPECIAL_CHARS for c in password):
            score += 15
        
        return min(score, 100)
    
    @staticmethod
    def get_strength_label(score: int) -> str:
        """
        Get strength label for score
        
        Args:
            score: Strength score (0-100)
            
        Returns:
            Strength label
        """
        if score < 40:
            return "Zayıf"
        elif score < 60:
            return "Orta"
        elif score < 80:
            return "İyi"
        else:
            return "Güçlü"
