"""
Linux AppLocker - Database Models
Defines the SQLAlchemy models for the application
"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, 
    DateTime, create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class MasterPassword(Base):
    """Master password table - stores hashed master password"""
    __tablename__ = 'master_password'
    
    id = Column(Integer, primary_key=True)
    password_hash = Column(Text, nullable=False)
    salt = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<MasterPassword(id={self.id}, created_at={self.created_at})>"


class LockedApplication(Base):
    """Locked applications table"""
    __tablename__ = 'locked_applications'
    
    id = Column(Integer, primary_key=True)
    app_name = Column(String(255), nullable=False)
    app_path = Column(Text, nullable=False)
    desktop_file = Column(Text)
    icon_path = Column(Text)
    locked_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<LockedApplication(id={self.id}, app_name={self.app_name})>"


class EncryptedFile(Base):
    """Encrypted files table"""
    __tablename__ = 'encrypted_files'
    
    id = Column(Integer, primary_key=True)
    original_path = Column(Text, nullable=False)
    encrypted_path = Column(Text, nullable=False)
    encryption_key_id = Column(Text, nullable=False)
    file_size = Column(Integer)
    encrypted_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<EncryptedFile(id={self.id}, original_path={self.original_path})>"


class AccessLog(Base):
    """Access logs table - records access attempts"""
    __tablename__ = 'access_logs'
    
    id = Column(Integer, primary_key=True)
    resource_type = Column(String(50), nullable=False)  # 'app' or 'file'
    resource_name = Column(Text, nullable=False)
    access_attempt_time = Column(DateTime, default=datetime.utcnow)
    success = Column(Boolean, default=False)
    ip_address = Column(String(50))
    
    def __repr__(self):
        return f"<AccessLog(id={self.id}, resource_type={self.resource_type}, success={self.success})>"


class Setting(Base):
    """Settings table - stores application settings"""
    __tablename__ = 'settings'
    
    key = Column(String(255), primary_key=True)
    value = Column(Text, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Setting(key={self.key}, value={self.value})>"
