"""
Linux AppLocker - Password Dialog
Dialog for password entry
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw


class PasswordDialog(Gtk.Dialog):
    """Dialog for entering password"""
    
    def __init__(self, parent, title="Şifre Girin", message="Lütfen şifrenizi girin:"):
        """
        Initialize password dialog
        
        Args:
            parent: Parent window
            title: Dialog title
            message: Message to display
        """
        super().__init__(transient_for=parent, modal=True)
        self.set_title(title)
        self.set_default_size(400, 200)
        
        self.password = None
        
        # Create content
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content_box.set_margin_top(24)
        content_box.set_margin_bottom(24)
        content_box.set_margin_start(24)
        content_box.set_margin_end(24)
        
        # Message label
        message_label = Gtk.Label(label=message)
        message_label.set_wrap(True)
        content_box.append(message_label)
        
        # Password entry
        self.password_entry = Gtk.PasswordEntry()
        self.password_entry.set_show_peek_icon(True)
        self.password_entry.connect('activate', self._on_password_activate)
        content_box.append(self.password_entry)
        
        # Error label (initially hidden)
        self.error_label = Gtk.Label(label="")
        self.error_label.add_css_class("error")
        self.error_label.set_visible(False)
        content_box.append(self.error_label)
        
        # Add content to dialog
        self.set_child(content_box)
        
        # Add buttons
        self.add_button("İptal", Gtk.ResponseType.CANCEL)
        ok_button = self.add_button("Tamam", Gtk.ResponseType.OK)
        ok_button.add_css_class("suggested-action")
        
        # Set default response
        self.set_default_response(Gtk.ResponseType.OK)
        
        # Focus password entry
        self.password_entry.grab_focus()
    
    def _on_password_activate(self, entry):
        """Handle password entry activation (Enter key)"""
        self.response(Gtk.ResponseType.OK)
    
    def get_password(self):
        """Get entered password"""
        return self.password_entry.get_text()
    
    def show_error(self, error_message):
        """Show error message"""
        self.error_label.set_text(error_message)
        self.error_label.set_visible(True)
    
    def clear_error(self):
        """Clear error message"""
        self.error_label.set_text("")
        self.error_label.set_visible(False)


class SetupPasswordDialog(Gtk.Dialog):
    """Dialog for setting up new password"""
    
    def __init__(self, parent):
        """Initialize setup password dialog"""
        super().__init__(transient_for=parent, modal=True)
        self.set_title("Master Şifre Oluştur")
        self.set_default_size(450, 350)
        
        # Create content
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content_box.set_margin_top(24)
        content_box.set_margin_bottom(24)
        content_box.set_margin_start(24)
        content_box.set_margin_end(24)
        
        # Title
        title_label = Gtk.Label(label="Master Şifre Oluşturun")
        title_label.add_css_class("title-2")
        content_box.append(title_label)
        
        # Description
        desc_label = Gtk.Label(
            label="Bu şifre tüm kilitli uygulamalara ve dosyalara erişim için kullanılacaktır."
        )
        desc_label.set_wrap(True)
        desc_label.add_css_class("dim-label")
        content_box.append(desc_label)
        
        # Password requirements
        req_label = Gtk.Label(
            label="Şifre gereksinimleri:\n• En az 8 karakter\n• Büyük ve küçük harf\n• Rakam\n• Özel karakter"
        )
        req_label.set_wrap(True)
        req_label.set_xalign(0)
        content_box.append(req_label)
        
        # Password entry
        password_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        password_label = Gtk.Label(label="Şifre:")
        password_label.set_xalign(0)
        password_box.append(password_label)
        
        self.password_entry = Gtk.PasswordEntry()
        self.password_entry.set_show_peek_icon(True)
        password_box.append(self.password_entry)
        content_box.append(password_box)
        
        # Confirm password entry
        confirm_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        confirm_label = Gtk.Label(label="Şifre (Tekrar):")
        confirm_label.set_xalign(0)
        confirm_box.append(confirm_label)
        
        self.confirm_entry = Gtk.PasswordEntry()
        self.confirm_entry.set_show_peek_icon(True)
        self.confirm_entry.connect('activate', self._on_confirm_activate)
        confirm_box.append(self.confirm_entry)
        content_box.append(confirm_box)
        
        # Error label
        self.error_label = Gtk.Label(label="")
        self.error_label.add_css_class("error")
        self.error_label.set_visible(False)
        content_box.append(self.error_label)
        
        # Add content to dialog
        self.set_child(content_box)
        
        # Add buttons
        self.add_button("İptal", Gtk.ResponseType.CANCEL)
        create_button = self.add_button("Oluştur", Gtk.ResponseType.OK)
        create_button.add_css_class("suggested-action")
        
        # Set default response
        self.set_default_response(Gtk.ResponseType.OK)
        
        # Focus first entry
        self.password_entry.grab_focus()
    
    def _on_confirm_activate(self, entry):
        """Handle confirm entry activation"""
        self.response(Gtk.ResponseType.OK)
    
    def get_password(self):
        """Get entered password"""
        return self.password_entry.get_text()
    
    def get_confirm_password(self):
        """Get confirm password"""
        return self.confirm_entry.get_text()
    
    def show_error(self, error_message):
        """Show error message"""
        self.error_label.set_text(error_message)
        self.error_label.set_visible(True)
    
    def clear_error(self):
        """Clear error message"""
        self.error_label.set_text("")
        self.error_label.set_visible(False)
