"""
Linux AppLocker - File Locker
Manages file encryption and decryption
"""

import os
from pathlib import Path
from typing import Optional, List
from ..database import DatabaseManager
from ..crypto import FileEncryption, KeyStorage
from ..utils import Logger


class FileLocker:
    """Manages file locking through encryption"""
    
    def __init__(self, db_manager: DatabaseManager, 
                 master_password: Optional[str] = None,
                 logger: Optional[Logger] = None):
        """
        Initialize file locker
        
        Args:
            db_manager: Database manager instance
            master_password: Master password for key derivation
            logger: Logger instance
        """
        self.db = db_manager
        self.master_password = master_password
        self.logger = logger or Logger()
        self.encryption = FileEncryption()
        self.key_storage = KeyStorage()
    
    def set_master_password(self, password: str):
        """Set master password for encryption"""
        self.master_password = password
    
    def lock_file(self, file_path: str) -> bool:
        """
        Lock (encrypt) a file
        
        Args:
            file_path: Path to file to lock
            
        Returns:
            True if successful
        """
        try:
            if not os.path.exists(file_path):
                self.logger.error(f"File not found: {file_path}")
                return False
            
            if not os.path.isfile(file_path):
                self.logger.error(f"Not a file: {file_path}")
                return False
            
            # Generate encryption key
            encryption_key = self.encryption.generate_key()
            
            # Generate key ID
            key_id = self.key_storage.generate_key_id(file_path)
            
            # Store key securely
            if not self.key_storage.store_key(key_id, encryption_key):
                self.logger.error("Failed to store encryption key")
                return False
            
            # Get file size
            file_size = os.path.getsize(file_path)
            
            # Encrypt file
            encrypted_path = file_path + '.locked'
            self.encryption.encrypt_file(file_path, encrypted_path, encryption_key)
            
            # Add to database
            self.db.add_encrypted_file(
                original_path=file_path,
                encrypted_path=encrypted_path,
                encryption_key_id=key_id,
                file_size=file_size
            )
            
            # Securely delete original
            self.encryption.secure_delete_file(file_path)
            
            self.logger.info(f"Locked file: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error locking file {file_path}: {e}")
            return False
    
    def unlock_file(self, encrypted_path: str) -> bool:
        """
        Unlock (decrypt) a file
        
        Args:
            encrypted_path: Path to encrypted file
            
        Returns:
            True if successful
        """
        try:
            if not os.path.exists(encrypted_path):
                self.logger.error(f"Encrypted file not found: {encrypted_path}")
                return False
            
            # Get file info from database
            file_info = self.db.get_encrypted_file_by_path(encrypted_path)
            if not file_info:
                self.logger.error(f"File not found in database: {encrypted_path}")
                return False
            
            # Retrieve encryption key
            encryption_key = self.key_storage.retrieve_key(file_info.encryption_key_id)
            if not encryption_key:
                self.logger.error("Failed to retrieve encryption key")
                return False
            
            # Decrypt file
            original_path = file_info.original_path
            self.encryption.decrypt_file(encrypted_path, original_path, encryption_key)
            
            # Remove encrypted file
            os.remove(encrypted_path)
            
            # Remove from database
            self.db.remove_encrypted_file(file_info.id)
            
            # Delete key from storage
            self.key_storage.delete_key(file_info.encryption_key_id)
            
            self.logger.info(f"Unlocked file: {original_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error unlocking file {encrypted_path}: {e}")
            return False
    
    def lock_directory(self, directory_path: str, recursive: bool = True) -> int:
        """
        Lock all files in a directory
        
        Args:
            directory_path: Path to directory
            recursive: Whether to lock files in subdirectories
            
        Returns:
            Number of files locked
        """
        try:
            if not os.path.exists(directory_path):
                self.logger.error(f"Directory not found: {directory_path}")
                return 0
            
            if not os.path.isdir(directory_path):
                self.logger.error(f"Not a directory: {directory_path}")
                return 0
            
            locked_count = 0
            
            if recursive:
                for root, dirs, files in os.walk(directory_path):
                    for file in files:
                        if not file.endswith('.locked'):
                            file_path = os.path.join(root, file)
                            if self.lock_file(file_path):
                                locked_count += 1
            else:
                for item in os.listdir(directory_path):
                    item_path = os.path.join(directory_path, item)
                    if os.path.isfile(item_path) and not item.endswith('.locked'):
                        if self.lock_file(item_path):
                            locked_count += 1
            
            self.logger.info(f"Locked {locked_count} files in directory: {directory_path}")
            return locked_count
            
        except Exception as e:
            self.logger.error(f"Error locking directory {directory_path}: {e}")
            return 0
    
    def get_locked_files(self) -> List:
        """
        Get all locked files
        
        Returns:
            List of encrypted file objects
        """
        return self.db.get_encrypted_files(active_only=True)
    
    def is_file_locked(self, file_path: str) -> bool:
        """
        Check if a file is locked
        
        Args:
            file_path: Path to check (original or encrypted)
            
        Returns:
            True if locked
        """
        # Check if encrypted version exists
        encrypted_path = file_path + '.locked'
        return self.db.get_encrypted_file_by_path(encrypted_path) is not None
