"""
Tests for File Encryption
"""

import os
import tempfile
import pytest
from src.crypto.encryption import FileEncryption


class TestFileEncryption:
    """Test file encryption functionality"""
    
    def setup_method(self):
        """Setup test method"""
        self.encryption = FileEncryption()
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Cleanup after test"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_key_generation(self):
        """Test encryption key generation"""
        key = self.encryption.generate_key()
        assert key is not None
        assert len(key) == 32  # 256 bits = 32 bytes
    
    def test_data_encryption_decryption(self):
        """Test data encryption and decryption"""
        original_data = b"This is test data for encryption"
        key = self.encryption.generate_key()
        
        # Encrypt
        encrypted_data, nonce = self.encryption.encrypt_data(original_data, key)
        
        # Verify encrypted data is different
        assert encrypted_data != original_data
        assert nonce is not None
        assert len(nonce) == 12  # GCM nonce size
        
        # Decrypt
        decrypted_data = self.encryption.decrypt_data(encrypted_data, key, nonce)
        
        # Verify decryption is correct
        assert decrypted_data == original_data
    
    def test_file_encryption_decryption(self):
        """Test file encryption and decryption"""
        # Create test file
        test_file = os.path.join(self.temp_dir, 'test.txt')
        test_data = b"Test file content for encryption"
        
        with open(test_file, 'wb') as f:
            f.write(test_data)
        
        # Generate key
        key = self.encryption.generate_key()
        
        # Encrypt file
        encrypted_file = os.path.join(self.temp_dir, 'test.txt.encrypted')
        self.encryption.encrypt_file(test_file, encrypted_file, key)
        
        # Verify encrypted file exists
        assert os.path.exists(encrypted_file)
        assert os.path.getsize(encrypted_file) > 0
        
        # Decrypt file
        decrypted_file = os.path.join(self.temp_dir, 'test_decrypted.txt')
        self.encryption.decrypt_file(encrypted_file, decrypted_file, key)
        
        # Verify decryption is correct
        with open(decrypted_file, 'rb') as f:
            decrypted_data = f.read()
        
        assert decrypted_data == test_data
    
    def test_key_derivation_from_password(self):
        """Test PBKDF2 key derivation"""
        password = "TestPassword123!"
        salt = os.urandom(16)
        
        # Derive key
        key = self.encryption.derive_key_from_password(password, salt)
        
        # Verify key properties
        assert key is not None
        assert len(key) == 32
        
        # Same password and salt should give same key
        key2 = self.encryption.derive_key_from_password(password, salt)
        assert key == key2
        
        # Different salt should give different key
        different_salt = os.urandom(16)
        key3 = self.encryption.derive_key_from_password(password, different_salt)
        assert key != key3
