"""
Linux AppLocker - Main Window
Main application window with tabs for different views
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib

from ..database import DatabaseManager
from ..crypto import PasswordManager
from ..core import AppLocker, FileLocker, ProcessMonitor, AppScanner
from ..utils import Config, Logger, NotificationManager
from .password_dialog import PasswordDialog
from .setup_dialog import SetupDialog
from .applications_view import ApplicationsView
from .files_view import FilesView
from .dashboard_view import DashboardView
from .settings_view import SettingsView


class MainWindow(Adw.ApplicationWindow):
    """Main application window"""
    
    def __init__(self, app, **kwargs):
        """Initialize main window"""
        super().__init__(application=app, **kwargs)
        
        # Initialize components
        self.config = Config()
        self.logger = Logger(log_dir=self.config.log_dir)
        self.db = DatabaseManager()
        self.password_manager = PasswordManager()
        self.notifications = NotificationManager()
        
        # Master password (will be set during setup or login)
        self.master_password = None
        self.is_authenticated = False
        
        # Initialize core components
        self.app_locker = AppLocker(self.db, self.logger)
        self.file_locker = FileLocker(self.db, logger=self.logger)
        self.process_monitor = ProcessMonitor(self.db, self.logger)
        self.app_scanner = AppScanner()
        
        # Window properties
        self.set_title("Linux AppLocker")
        self.set_default_size(900, 650)
        
        # Check if first run
        if not self._check_master_password():
            self._show_setup_wizard()
        else:
            self._show_login()
    
    def _check_master_password(self):
        """Check if master password is set"""
        master_pwd = self.db.get_master_password()
        return master_pwd is not None
    
    def _show_setup_wizard(self):
        """Show setup wizard for first-time use"""
        setup = SetupDialog(self)
        setup.present()
        
        def on_close(dialog):
            if setup.is_complete():
                password = setup.get_password()
                self._setup_master_password(password)
                self._build_ui()
                self.is_authenticated = True
            else:
                # User cancelled setup, close app
                self.close()
        
        setup.connect('close-request', on_close)
    
    def _show_login(self):
        """Show login dialog"""
        dialog = PasswordDialog(
            self,
            title="Linux AppLocker - Giriş",
            message="Master şifrenizi girin:"
        )
        
        response = dialog.present()
        
        def on_response(dialog, response_id):
            if response_id == Gtk.ResponseType.OK:
                password = dialog.get_password()
                if self._verify_master_password(password):
                    self.master_password = password
                    self.is_authenticated = True
                    self.file_locker.set_master_password(password)
                    self._build_ui()
                    dialog.close()
                else:
                    dialog.show_error("Yanlış şifre!")
                    # Show dialog again
                    GLib.timeout_add(100, lambda: dialog.present())
            else:
                # User cancelled login
                self.close()
        
        dialog.connect('response', on_response)
        dialog.present()
    
    def _setup_master_password(self, password):
        """Set up master password for first time"""
        password_hash, salt = self.password_manager.hash_password(password)
        self.db.set_master_password(password_hash, salt)
        self.master_password = password
        self.file_locker.set_master_password(password)
        self.logger.info("Master password created")
    
    def _verify_master_password(self, password):
        """Verify master password"""
        master_pwd = self.db.get_master_password()
        if not master_pwd:
            return False
        return self.password_manager.verify_password(password, master_pwd.password_hash)
    
    def _build_ui(self):
        """Build main UI after authentication"""
        # Main box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        # Header bar
        header = Adw.HeaderBar()
        
        # Menu button
        menu_button = Gtk.MenuButton()
        menu_button.set_icon_name("open-menu-symbolic")
        header.pack_end(menu_button)
        
        # Create menu
        menu = Gio.Menu()
        menu.append("Ayarlar", "app.settings")
        menu.append("Hakkında", "app.about")
        menu.append("Çıkış", "app.quit")
        menu_button.set_menu_model(menu)
        
        main_box.append(header)
        
        # View stack
        self.view_stack = Gtk.Stack()
        self.view_stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        
        # Stack switcher
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(self.view_stack)
        header.set_title_widget(stack_switcher)
        
        # Create views
        self.dashboard_view = DashboardView(self)
        self.view_stack.add_titled(self.dashboard_view, "dashboard", "Dashboard")
        
        self.applications_view = ApplicationsView(self)
        self.view_stack.add_titled(self.applications_view, "apps", "Uygulamalar")
        
        self.files_view = FilesView(self)
        self.view_stack.add_titled(self.files_view, "files", "Dosyalar")
        
        self.settings_view = SettingsView(self)
        self.view_stack.add_titled(self.settings_view, "settings", "Ayarlar")
        
        main_box.append(self.view_stack)
        
        self.set_content(main_box)
        
        # Start process monitor
        self.process_monitor.start_monitoring()
        
        self.logger.info("Main window initialized")
    
    def show_password_dialog(self, title="Şifre Girin", message="Lütfen şifrenizi girin:"):
        """Show password dialog and return password if correct"""
        dialog = PasswordDialog(self, title, message)
        
        password = None
        
        def on_response(dialog, response_id):
            nonlocal password
            if response_id == Gtk.ResponseType.OK:
                entered_password = dialog.get_password()
                if self._verify_master_password(entered_password):
                    password = entered_password
                    dialog.close()
                else:
                    dialog.show_error("Yanlış şifre!")
        
        dialog.connect('response', on_response)
        dialog.present()
        
        return password
    
    def refresh_views(self):
        """Refresh all views"""
        if hasattr(self, 'dashboard_view'):
            self.dashboard_view.refresh()
        if hasattr(self, 'applications_view'):
            self.applications_view.refresh()
        if hasattr(self, 'files_view'):
            self.files_view.refresh()
    
    def do_close_request(self):
        """Handle window close request"""
        # Stop process monitor
        if hasattr(self, 'process_monitor'):
            self.process_monitor.stop_monitoring()
        
        self.logger.info("Application closing")
        return False  # Allow window to close
