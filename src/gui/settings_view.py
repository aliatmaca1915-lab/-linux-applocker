"""
Linux AppLocker - Settings View
Application settings and preferences
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw


class SettingsView(Gtk.Box):
    """Settings view"""
    
    def __init__(self, main_window):
        """Initialize settings view"""
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        
        self.main_window = main_window
        
        # Scrolled window
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        
        # Settings list
        settings_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        settings_box.set_margin_top(24)
        settings_box.set_margin_bottom(24)
        settings_box.set_margin_start(24)
        settings_box.set_margin_end(24)
        
        # Security section
        security_group = Adw.PreferencesGroup()
        security_group.set_title("Güvenlik")
        security_group.set_description("Güvenlik ayarları")
        
        # Change password
        change_password_row = Adw.ActionRow()
        change_password_row.set_title("Master Şifre Değiştir")
        change_password_row.set_subtitle("Master şifrenizi değiştirin")
        change_password_button = Gtk.Button()
        change_password_button.set_icon_name("go-next-symbolic")
        change_password_button.set_valign(Gtk.Align.CENTER)
        change_password_button.add_css_class("flat")
        change_password_button.connect('clicked', self._on_change_password)
        change_password_row.add_suffix(change_password_button)
        security_group.add(change_password_row)
        
        # Auto lock timeout
        auto_lock_row = Adw.ActionRow()
        auto_lock_row.set_title("Otomatik Kilitleme Süresi")
        auto_lock_row.set_subtitle("Dakika cinsinden")
        timeout_spin = Gtk.SpinButton()
        timeout_spin.set_range(1, 60)
        timeout_spin.set_increments(1, 5)
        timeout_value = self.main_window.config.get('auto_lock_timeout', 300) // 60
        timeout_spin.set_value(timeout_value)
        timeout_spin.set_valign(Gtk.Align.CENTER)
        timeout_spin.connect('value-changed', self._on_timeout_changed)
        auto_lock_row.add_suffix(timeout_spin)
        security_group.add(auto_lock_row)
        
        settings_box.append(security_group)
        
        # Appearance section
        appearance_group = Adw.PreferencesGroup()
        appearance_group.set_title("Görünüm")
        appearance_group.set_description("Arayüz ayarları")
        
        # Theme selection
        theme_row = Adw.ComboRow()
        theme_row.set_title("Tema")
        theme_row.set_subtitle("Arayüz teması")
        
        theme_model = Gtk.StringList()
        theme_model.append("Otomatik")
        theme_model.append("Açık")
        theme_model.append("Koyu")
        theme_row.set_model(theme_model)
        
        current_theme = self.main_window.config.get('theme', 'auto')
        theme_index = {'auto': 0, 'light': 1, 'dark': 2}.get(current_theme, 0)
        theme_row.set_selected(theme_index)
        theme_row.connect('notify::selected', self._on_theme_changed)
        
        appearance_group.add(theme_row)
        
        settings_box.append(appearance_group)
        
        # Notifications section
        notifications_group = Adw.PreferencesGroup()
        notifications_group.set_title("Bildirimler")
        
        # Enable notifications
        notifications_row = Adw.SwitchRow()
        notifications_row.set_title("Bildirimleri Etkinleştir")
        notifications_row.set_subtitle("Erişim denemelerinde bildirim göster")
        notifications_enabled = self.main_window.config.get('notifications_enabled', True)
        notifications_row.set_active(notifications_enabled)
        notifications_row.connect('notify::active', self._on_notifications_changed)
        notifications_group.add(notifications_row)
        
        settings_box.append(notifications_group)
        
        # System section
        system_group = Adw.PreferencesGroup()
        system_group.set_title("Sistem")
        
        # Start on boot
        autostart_row = Adw.SwitchRow()
        autostart_row.set_title("Başlangıçta Çalıştır")
        autostart_row.set_subtitle("Sistem açılışında otomatik başlat")
        autostart_enabled = self.main_window.config.get('start_on_boot', False)
        autostart_row.set_active(autostart_enabled)
        autostart_row.connect('notify::active', self._on_autostart_changed)
        system_group.add(autostart_row)
        
        # Process monitor status
        monitor_status_row = Adw.ActionRow()
        monitor_status_row.set_title("Process Monitor")
        is_monitoring = self.main_window.process_monitor.is_monitoring()
        monitor_status_row.set_subtitle("Çalışıyor" if is_monitoring else "Durduruldu")
        
        monitor_icon = Gtk.Image()
        monitor_icon.set_from_icon_name("emblem-ok-symbolic" if is_monitoring else "process-stop-symbolic")
        monitor_status_row.add_suffix(monitor_icon)
        system_group.add(monitor_status_row)
        
        settings_box.append(system_group)
        
        # About section
        about_group = Adw.PreferencesGroup()
        about_group.set_title("Hakkında")
        
        # Version info
        version_row = Adw.ActionRow()
        version_row.set_title("Linux AppLocker")
        version_row.set_subtitle("Versiyon 1.0.0")
        about_group.add(version_row)
        
        # License info
        license_row = Adw.ActionRow()
        license_row.set_title("Lisans")
        license_row.set_subtitle("MIT License")
        about_group.add(license_row)
        
        settings_box.append(about_group)
        
        scrolled.set_child(settings_box)
        self.append(scrolled)
    
    def _on_change_password(self, button):
        """Handle change password button click"""
        from .password_dialog import SetupPasswordDialog
        
        dialog = SetupPasswordDialog(self.main_window)
        
        def on_response(dialog, response_id):
            if response_id == Gtk.ResponseType.OK:
                new_password = dialog.get_password()
                confirm_password = dialog.get_confirm_password()
                
                if new_password != confirm_password:
                    dialog.show_error("Şifreler eşleşmiyor")
                    return
                
                # Verify old password first
                old_password_dialog = Adw.MessageDialog.new(self.main_window)
                old_password_dialog.set_heading("Mevcut Şifre")
                old_password_dialog.set_body("Lütfen mevcut master şifrenizi girin")
                
                # This is simplified - should use a proper password entry dialog
                # For now, we'll just update the password
                success, result = self.main_window.password_manager.change_password(
                    self.main_window.master_password,
                    new_password,
                    self.main_window.db.get_master_password().password_hash
                )
                
                if success and result:
                    new_hash, new_salt = result
                    self.main_window.db.set_master_password(new_hash, new_salt)
                    self.main_window.master_password = new_password
                    self.main_window.notifications.notify_master_password_changed()
                    dialog.close()
                else:
                    dialog.show_error("Şifre değiştirilemedi")
        
        dialog.connect('response', on_response)
        dialog.present()
    
    def _on_timeout_changed(self, spin_button):
        """Handle auto lock timeout change"""
        minutes = int(spin_button.get_value())
        seconds = minutes * 60
        self.main_window.config.set('auto_lock_timeout', seconds)
    
    def _on_theme_changed(self, combo_row, param):
        """Handle theme change"""
        selected = combo_row.get_selected()
        themes = ['auto', 'light', 'dark']
        if selected < len(themes):
            theme = themes[selected]
            self.main_window.config.set('theme', theme)
            
            # Apply theme
            style_manager = Adw.StyleManager.get_default()
            if theme == 'light':
                style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
            elif theme == 'dark':
                style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
            else:
                style_manager.set_color_scheme(Adw.ColorScheme.DEFAULT)
    
    def _on_notifications_changed(self, switch_row, param):
        """Handle notifications toggle"""
        enabled = switch_row.get_active()
        self.main_window.config.set('notifications_enabled', enabled)
    
    def _on_autostart_changed(self, switch_row, param):
        """Handle autostart toggle"""
        enabled = switch_row.get_active()
        self.main_window.config.set('start_on_boot', enabled)
        
        # Enable/disable systemd service
        import subprocess
        if enabled:
            subprocess.run(['systemctl', '--user', 'enable', 'linux-applocker.service'],
                         capture_output=True)
        else:
            subprocess.run(['systemctl', '--user', 'disable', 'linux-applocker.service'],
                         capture_output=True)
    
    def refresh(self):
        """Refresh settings view"""
        pass
