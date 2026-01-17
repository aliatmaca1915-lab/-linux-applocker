"""
Linux AppLocker - Main Entry Point
"""

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio

from .gui import MainWindow
from .utils import Logger


class AppLockerApplication(Adw.Application):
    """Main application class"""
    
    def __init__(self):
        """Initialize application"""
        super().__init__(
            application_id='com.github.aliatmaca1915-lab.linux-applocker',
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )
        
        self.logger = Logger()
        self.main_window = None
        
        # Create actions
        self.create_action('quit', self.on_quit)
        self.create_action('about', self.on_about)
    
    def do_activate(self):
        """Activate application"""
        # Create and show main window if not exists
        if not self.main_window:
            self.main_window = MainWindow(self)
        
        self.main_window.present()
    
    def create_action(self, name, callback):
        """Create an application action"""
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)
    
    def on_quit(self, action, param):
        """Quit application"""
        self.quit()
    
    def on_about(self, action, param):
        """Show about dialog"""
        about = Adw.AboutWindow()
        about.set_transient_for(self.main_window)
        about.set_application_name("Linux AppLocker")
        about.set_version("1.0.0")
        about.set_developer_name("Linux AppLocker Team")
        about.set_license_type(Gtk.License.MIT_X11)
        about.set_comments("Profesyonel Uygulama ve Dosya Kilitleme Sistemi")
        about.set_website("https://github.com/aliatmaca1915-lab/-linux-applocker")
        about.set_issue_url("https://github.com/aliatmaca1915-lab/-linux-applocker/issues")
        about.set_developers([
            "Linux AppLocker Team"
        ])
        about.set_copyright("© 2026 Linux AppLocker Team")
        about.present()


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Linux AppLocker')
    parser.add_argument('--daemon', action='store_true', help='Run in daemon mode')
    parser.add_argument('--setup', action='store_true', help='Run setup wizard')
    args = parser.parse_args()
    
    if args.daemon:
        # Run daemon mode
        from .daemon import DaemonService
        daemon = DaemonService()
        daemon.run()
    else:
        # Run GUI mode
        app = AppLockerApplication()
        return app.run(sys.argv)


if __name__ == '__main__':
    sys.exit(main())
