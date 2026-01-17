"""
Linux AppLocker - Key Storage
Manages secure storage of encryption keys using keyring
"""

import keyring
import os
import base64
from typing import Optional


class KeyStorage:
    """Manages secure storage of encryption keys"""
    
    SERVICE_NAME = "linux-applocker"
    
    def __init__(self):
        """Initialize key storage"""
        pass
    
    def store_key(self, key_id: str, key: bytes) -> bool:
        """
        Store an encryption key securely
        
        Args:
            key_id: Unique identifier for the key
            key: Encryption key to store
            
        Returns:
            True if successful
        """
        try:
            # Encode key as base64 for storage
            encoded_key = base64.b64encode(key).decode()
            keyring.set_password(self.SERVICE_NAME, key_id, encoded_key)
            return True
        except Exception as e:
            print(f"Error storing key: {e}")
            return False
    
    def retrieve_key(self, key_id: str) -> Optional[bytes]:
        """
        Retrieve an encryption key
        
        Args:
            key_id: Unique identifier for the key
            
        Returns:
            Encryption key or None if not found
        """
        try:
            encoded_key = keyring.get_password(self.SERVICE_NAME, key_id)
            if encoded_key:
                return base64.b64decode(encoded_key)
            return None
        except Exception as e:
            print(f"Error retrieving key: {e}")
            return None
    
    def delete_key(self, key_id: str) -> bool:
        """
        Delete an encryption key
        
        Args:
            key_id: Unique identifier for the key
            
        Returns:
            True if successful
        """
        try:
            keyring.delete_password(self.SERVICE_NAME, key_id)
            return True
        except Exception as e:
            print(f"Error deleting key: {e}")
            return False
    
    def generate_key_id(self, file_path: str) -> str:
        """
        Generate a unique key ID for a file
        
        Args:
            file_path: Path to the file
            
        Returns:
            Unique key ID
        """
        import hashlib
        # Use hash of file path as key ID
        return hashlib.sha256(file_path.encode()).hexdigest()
    
    def key_exists(self, key_id: str) -> bool:
        """
        Check if a key exists
        
        Args:
            key_id: Unique identifier for the key
            
        Returns:
            True if key exists
        """
        return self.retrieve_key(key_id) is not None
