"""
Linux AppLocker - Database Manager
Handles all database operations using SQLAlchemy
"""

import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import (
    Base, MasterPassword, LockedApplication, 
    EncryptedFile, AccessLog, Setting
)


class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize database manager
        
        Args:
            db_path: Path to SQLite database file. If None, uses default location.
        """
        if db_path is None:
            db_path = self._get_default_db_path()
        
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        # Create tables if they don't exist
        self._create_tables()
    
    def _get_default_db_path(self) -> str:
        """Get default database path in user's config directory"""
        config_dir = Path.home() / '.local' / 'share' / 'linux-applocker'
        config_dir.mkdir(parents=True, exist_ok=True)
        return str(config_dir / 'applocker.db')
    
    def _create_tables(self):
        """Create all database tables"""
        Base.metadata.create_all(self.engine)
    
    def get_session(self) -> Session:
        """Get a new database session"""
        return self.SessionLocal()
    
    # Master Password operations
    def set_master_password(self, password_hash: str, salt: str) -> MasterPassword:
        """Set or update master password"""
        session = self.get_session()
        try:
            # Delete existing master password
            session.query(MasterPassword).delete()
            
            # Create new master password
            master_pwd = MasterPassword(password_hash=password_hash, salt=salt)
            session.add(master_pwd)
            session.commit()
            session.refresh(master_pwd)
            return master_pwd
        finally:
            session.close()
    
    def get_master_password(self) -> Optional[MasterPassword]:
        """Get master password record"""
        session = self.get_session()
        try:
            return session.query(MasterPassword).first()
        finally:
            session.close()
    
    # Locked Applications operations
    def add_locked_application(self, app_name: str, app_path: str, 
                               desktop_file: Optional[str] = None,
                               icon_path: Optional[str] = None) -> LockedApplication:
        """Add a locked application"""
        session = self.get_session()
        try:
            app = LockedApplication(
                app_name=app_name,
                app_path=app_path,
                desktop_file=desktop_file,
                icon_path=icon_path
            )
            session.add(app)
            session.commit()
            session.refresh(app)
            return app
        finally:
            session.close()
    
    def remove_locked_application(self, app_id: int) -> bool:
        """Remove a locked application"""
        session = self.get_session()
        try:
            app = session.query(LockedApplication).filter_by(id=app_id).first()
            if app:
                session.delete(app)
                session.commit()
                return True
            return False
        finally:
            session.close()
    
    def get_locked_applications(self, active_only: bool = True) -> List[LockedApplication]:
        """Get all locked applications"""
        session = self.get_session()
        try:
            query = session.query(LockedApplication)
            if active_only:
                query = query.filter_by(is_active=True)
            return query.all()
        finally:
            session.close()
    
    def is_application_locked(self, app_path: str) -> bool:
        """Check if an application is locked"""
        session = self.get_session()
        try:
            app = session.query(LockedApplication).filter_by(
                app_path=app_path, is_active=True
            ).first()
            return app is not None
        finally:
            session.close()
    
    # Encrypted Files operations
    def add_encrypted_file(self, original_path: str, encrypted_path: str,
                          encryption_key_id: str, file_size: int) -> EncryptedFile:
        """Add an encrypted file record"""
        session = self.get_session()
        try:
            encrypted_file = EncryptedFile(
                original_path=original_path,
                encrypted_path=encrypted_path,
                encryption_key_id=encryption_key_id,
                file_size=file_size
            )
            session.add(encrypted_file)
            session.commit()
            session.refresh(encrypted_file)
            return encrypted_file
        finally:
            session.close()
    
    def remove_encrypted_file(self, file_id: int) -> bool:
        """Remove an encrypted file record"""
        session = self.get_session()
        try:
            file = session.query(EncryptedFile).filter_by(id=file_id).first()
            if file:
                session.delete(file)
                session.commit()
                return True
            return False
        finally:
            session.close()
    
    def get_encrypted_files(self, active_only: bool = True) -> List[EncryptedFile]:
        """Get all encrypted files"""
        session = self.get_session()
        try:
            query = session.query(EncryptedFile)
            if active_only:
                query = query.filter_by(is_active=True)
            return query.all()
        finally:
            session.close()
    
    def get_encrypted_file_by_path(self, encrypted_path: str) -> Optional[EncryptedFile]:
        """Get encrypted file by its encrypted path"""
        session = self.get_session()
        try:
            return session.query(EncryptedFile).filter_by(
                encrypted_path=encrypted_path, is_active=True
            ).first()
        finally:
            session.close()
    
    # Access Logs operations
    def log_access_attempt(self, resource_type: str, resource_name: str,
                          success: bool, ip_address: Optional[str] = None) -> AccessLog:
        """Log an access attempt"""
        session = self.get_session()
        try:
            log = AccessLog(
                resource_type=resource_type,
                resource_name=resource_name,
                success=success,
                ip_address=ip_address
            )
            session.add(log)
            session.commit()
            session.refresh(log)
            return log
        finally:
            session.close()
    
    def get_access_logs(self, limit: int = 100) -> List[AccessLog]:
        """Get recent access logs"""
        session = self.get_session()
        try:
            return session.query(AccessLog)\
                .order_by(AccessLog.access_attempt_time.desc())\
                .limit(limit)\
                .all()
        finally:
            session.close()
    
    def get_failed_access_count(self, minutes: int = 5) -> int:
        """Get count of failed access attempts in last N minutes"""
        from datetime import datetime, timedelta
        session = self.get_session()
        try:
            cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
            return session.query(AccessLog).filter(
                AccessLog.success == False,
                AccessLog.access_attempt_time >= cutoff_time
            ).count()
        finally:
            session.close()
    
    # Settings operations
    def set_setting(self, key: str, value: str) -> Setting:
        """Set a setting value"""
        session = self.get_session()
        try:
            setting = session.query(Setting).filter_by(key=key).first()
            if setting:
                setting.value = value
            else:
                setting = Setting(key=key, value=value)
                session.add(setting)
            session.commit()
            session.refresh(setting)
            return setting
        finally:
            session.close()
    
    def get_setting(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get a setting value"""
        session = self.get_session()
        try:
            setting = session.query(Setting).filter_by(key=key).first()
            return setting.value if setting else default
        finally:
            session.close()
    
    def get_all_settings(self) -> Dict[str, str]:
        """Get all settings as a dictionary"""
        session = self.get_session()
        try:
            settings = session.query(Setting).all()
            return {s.key: s.value for s in settings}
        finally:
            session.close()
    
    # Statistics
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        session = self.get_session()
        try:
            return {
                'locked_apps_count': session.query(LockedApplication).filter_by(is_active=True).count(),
                'encrypted_files_count': session.query(EncryptedFile).filter_by(is_active=True).count(),
                'total_access_logs': session.query(AccessLog).count(),
                'failed_attempts_today': self._get_failed_attempts_today(session)
            }
        finally:
            session.close()
    
    def _get_failed_attempts_today(self, session: Session) -> int:
        """Get failed access attempts today"""
        from datetime import datetime, timedelta
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        return session.query(AccessLog).filter(
            AccessLog.success == False,
            AccessLog.access_attempt_time >= today_start
        ).count()
