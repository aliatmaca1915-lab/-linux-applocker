"""
Linux AppLocker - File Encryption
Implements AES-256-GCM encryption for files
"""

import os
from pathlib import Path
from typing import Tuple, Optional
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.backends import default_backend


class FileEncryption:
    """Handles file encryption and decryption using AES-256-GCM"""
    
    KEY_SIZE = 32  # 256 bits
    NONCE_SIZE = 12  # 96 bits for GCM
    SALT_SIZE = 16
    ITERATIONS = 100000
    
    def __init__(self):
        """Initialize file encryption"""
        pass
    
    def derive_key_from_password(self, password: str, salt: bytes) -> bytes:
        """
        Derive encryption key from password using PBKDF2
        
        Args:
            password: Master password
            salt: Salt for key derivation
            
        Returns:
            Derived encryption key
        """
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=self.KEY_SIZE,
            salt=salt,
            iterations=self.ITERATIONS,
            backend=default_backend()
        )
        return kdf.derive(password.encode())
    
    def generate_key(self) -> bytes:
        """Generate a random encryption key"""
        return AESGCM.generate_key(bit_length=256)
    
    def encrypt_data(self, data: bytes, key: bytes) -> Tuple[bytes, bytes]:
        """
        Encrypt data using AES-256-GCM
        
        Args:
            data: Data to encrypt
            key: Encryption key
            
        Returns:
            Tuple of (encrypted_data, nonce)
        """
        aesgcm = AESGCM(key)
        nonce = os.urandom(self.NONCE_SIZE)
        encrypted_data = aesgcm.encrypt(nonce, data, None)
        return encrypted_data, nonce
    
    def decrypt_data(self, encrypted_data: bytes, key: bytes, nonce: bytes) -> bytes:
        """
        Decrypt data using AES-256-GCM
        
        Args:
            encrypted_data: Encrypted data
            key: Encryption key
            nonce: Nonce used for encryption
            
        Returns:
            Decrypted data
        """
        aesgcm = AESGCM(key)
        return aesgcm.decrypt(nonce, encrypted_data, None)
    
    def encrypt_file(self, input_path: str, output_path: str, key: bytes) -> Tuple[str, bytes]:
        """
        Encrypt a file
        
        Args:
            input_path: Path to file to encrypt
            output_path: Path for encrypted file
            key: Encryption key
            
        Returns:
            Tuple of (output_path, nonce)
        """
        # Read file
        with open(input_path, 'rb') as f:
            data = f.read()
        
        # Encrypt
        encrypted_data, nonce = self.encrypt_data(data, key)
        
        # Write encrypted file with nonce prepended
        with open(output_path, 'wb') as f:
            f.write(nonce)
            f.write(encrypted_data)
        
        return output_path, nonce
    
    def decrypt_file(self, input_path: str, output_path: str, key: bytes) -> str:
        """
        Decrypt a file
        
        Args:
            input_path: Path to encrypted file
            output_path: Path for decrypted file
            key: Encryption key
            
        Returns:
            Output path
        """
        # Read encrypted file
        with open(input_path, 'rb') as f:
            nonce = f.read(self.NONCE_SIZE)
            encrypted_data = f.read()
        
        # Decrypt
        decrypted_data = self.decrypt_data(encrypted_data, key, nonce)
        
        # Write decrypted file
        with open(output_path, 'wb') as f:
            f.write(decrypted_data)
        
        return output_path
    
    def secure_delete_file(self, file_path: str, passes: int = 3):
        """
        Securely delete a file by overwriting it
        
        Args:
            file_path: Path to file to delete
            passes: Number of overwrite passes
        """
        if not os.path.exists(file_path):
            return
        
        file_size = os.path.getsize(file_path)
        
        # Overwrite file multiple times
        with open(file_path, 'wb') as f:
            for _ in range(passes):
                f.seek(0)
                f.write(os.urandom(file_size))
                f.flush()
                os.fsync(f.fileno())
        
        # Finally delete the file
        os.remove(file_path)
    
    def encrypt_file_in_place(self, file_path: str, key: bytes, 
                              master_password: str) -> str:
        """
        Encrypt a file in place (replaces original with encrypted version)
        
        Args:
            file_path: Path to file to encrypt
            key: Encryption key
            master_password: Master password for key derivation
            
        Returns:
            Path to encrypted file (.locked extension)
        """
        encrypted_path = file_path + '.locked'
        
        # Encrypt file
        self.encrypt_file(file_path, encrypted_path, key)
        
        # Securely delete original
        self.secure_delete_file(file_path)
        
        return encrypted_path
    
    def decrypt_file_in_place(self, encrypted_path: str, key: bytes) -> str:
        """
        Decrypt a file in place (removes .locked extension)
        
        Args:
            encrypted_path: Path to encrypted file
            key: Encryption key
            
        Returns:
            Path to decrypted file
        """
        if not encrypted_path.endswith('.locked'):
            raise ValueError("File does not have .locked extension")
        
        original_path = encrypted_path[:-7]  # Remove '.locked'
        
        # Decrypt file
        self.decrypt_file(encrypted_path, original_path, key)
        
        # Delete encrypted file
        os.remove(encrypted_path)
        
        return original_path
