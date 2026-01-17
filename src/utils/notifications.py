"""
Linux AppLocker - Notifications
Handles desktop notifications
"""

import subprocess
from typing import Optional


class NotificationManager:
    """Manages desktop notifications"""
    
    def __init__(self):
        """Initialize notification manager"""
        self.app_name = "Linux AppLocker"
        self.icon = "security-high"
    
    def send_notification(self, title: str, message: str, 
                         urgency: str = "normal",
                         icon: Optional[str] = None):
        """
        Send a desktop notification
        
        Args:
            title: Notification title
            message: Notification message
            urgency: Urgency level (low, normal, critical)
            icon: Icon name or path
        """
        try:
            cmd = [
                'notify-send',
                '-a', self.app_name,
                '-u', urgency,
                '-i', icon or self.icon,
                title,
                message
            ]
            subprocess.run(cmd, check=False, capture_output=True)
        except Exception as e:
            print(f"Error sending notification: {e}")
    
    def notify_app_locked(self, app_name: str):
        """Notify that an application has been locked"""
        self.send_notification(
            "Uygulama Kilitlendi",
            f"{app_name} başarıyla kilitlendi",
            urgency="normal",
            icon="lock"
        )
    
    def notify_app_unlocked(self, app_name: str):
        """Notify that an application has been unlocked"""
        self.send_notification(
            "Uygulama Kilidi Açıldı",
            f"{app_name} kilidi başarıyla açıldı",
            urgency="normal",
            icon="unlock"
        )
    
    def notify_file_encrypted(self, file_name: str):
        """Notify that a file has been encrypted"""
        self.send_notification(
            "Dosya Şifrelendi",
            f"{file_name} başarıyla şifrelendi",
            urgency="normal",
            icon="lock"
        )
    
    def notify_file_decrypted(self, file_name: str):
        """Notify that a file has been decrypted"""
        self.send_notification(
            "Dosya Şifresi Çözüldü",
            f"{file_name} şifresi başarıyla çözüldü",
            urgency="normal",
            icon="unlock"
        )
    
    def notify_access_denied(self, resource_name: str):
        """Notify that access was denied"""
        self.send_notification(
            "Erişim Engellendi",
            f"{resource_name} erişimi engellendi - Yanlış şifre",
            urgency="critical",
            icon="dialog-error"
        )
    
    def notify_brute_force_protection(self, timeout_seconds: int):
        """Notify about brute force protection"""
        self.send_notification(
            "Güvenlik Uyarısı",
            f"Çok fazla yanlış deneme. {timeout_seconds} saniye bekleyin.",
            urgency="critical",
            icon="dialog-warning"
        )
    
    def notify_master_password_changed(self):
        """Notify that master password was changed"""
        self.send_notification(
            "Master Şifre Değiştirildi",
            "Master şifreniz başarıyla değiştirildi",
            urgency="normal",
            icon="security-high"
        )
