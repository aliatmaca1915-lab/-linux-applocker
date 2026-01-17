"""
Linux AppLocker - Applications View
Shows list of applications and allows locking/unlocking
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib


class ApplicationsView(Gtk.Box):
    """Applications view"""
    
    def __init__(self, main_window):
        """Initialize applications view"""
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        
        self.main_window = main_window
        
        # Toolbar
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        toolbar.set_margin_top(12)
        toolbar.set_margin_bottom(12)
        toolbar.set_margin_start(12)
        toolbar.set_margin_end(12)
        
        # Search entry
        self.search_entry = Gtk.SearchEntry()
        # Note: GTK4 SearchEntry uses placeholder-text property, not set_placeholder_text()
        self.search_entry.set_hexpand(True)
        self.search_entry.connect('search-changed', self._on_search_changed)
        toolbar.append(self.search_entry)
        
        # Refresh button
        refresh_button = Gtk.Button()
        refresh_button.set_icon_name("view-refresh-symbolic")
        refresh_button.set_tooltip_text("Yenile")
        refresh_button.connect('clicked', lambda b: self.refresh())
        toolbar.append(refresh_button)
        
        self.append(toolbar)
        
        # Scrolled window for app list
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        
        # Apps list
        self.apps_list = Gtk.ListBox()
        self.apps_list.add_css_class("boxed-list")
        self.apps_list.set_margin_top(12)
        self.apps_list.set_margin_bottom(12)
        self.apps_list.set_margin_start(12)
        self.apps_list.set_margin_end(12)
        
        scrolled.set_child(self.apps_list)
        self.append(scrolled)
        
        # Load applications
        self._load_applications()
    
    def _load_applications(self):
        """Load system applications"""
        # Clear existing rows
        while True:
            row = self.apps_list.get_row_at_index(0)
            if row is None:
                break
            self.apps_list.remove(row)
        
        # Show loading indicator
        spinner = Gtk.Spinner()
        spinner.set_spinning(True)
        loading_row = Gtk.ListBoxRow()
        loading_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        loading_box.set_halign(Gtk.Align.CENTER)
        loading_box.set_margin_top(24)
        loading_box.set_margin_bottom(24)
        loading_box.append(spinner)
        loading_label = Gtk.Label(label="Uygulamalar yükleniyor...")
        loading_label.set_margin_start(12)
        loading_box.append(loading_label)
        loading_row.set_child(loading_box)
        self.apps_list.append(loading_row)
        
        # Load apps in background
        def load():
            apps = self.main_window.app_scanner.scan_applications()
            locked_apps = self.main_window.app_locker.get_locked_applications()
            locked_paths = {app.app_path for app in locked_apps}
            
            GLib.idle_add(self._populate_apps, apps, locked_paths)
        
        import threading
        thread = threading.Thread(target=load, daemon=True)
        thread.start()
    
    def _populate_apps(self, apps, locked_paths):
        """Populate apps list (called from main thread)"""
        # Clear loading row
        while True:
            row = self.apps_list.get_row_at_index(0)
            if row is None:
                break
            self.apps_list.remove(row)
        
        # Add app rows
        for app in apps:
            row = self._create_app_row(app, locked_paths)
            self.apps_list.append(row)
        
        if not apps:
            empty_row = Adw.ActionRow()
            empty_row.set_title("Uygulama bulunamadı")
            self.apps_list.append(empty_row)
    
    def _create_app_row(self, app, locked_paths):
        """Create a row for an application"""
        row = Adw.ActionRow()
        row.set_title(app['name'])
        
        if app.get('comment'):
            row.set_subtitle(app['comment'][:50])
        
        # App icon
        icon = Gtk.Image()
        if app.get('icon'):
            icon.set_from_icon_name(app['icon'])
        else:
            icon.set_from_icon_name("application-x-executable")
        icon.set_pixel_size(32)
        row.add_prefix(icon)
        
        # Lock/Unlock button
        exec_path = self.main_window.app_scanner.get_executable_path(app['exec'])
        is_locked = exec_path in locked_paths
        
        button = Gtk.Button()
        if is_locked:
            button.set_icon_name("changes-allow-symbolic")
            button.set_tooltip_text("Kilidi Aç")
            button.add_css_class("success")
        else:
            button.set_icon_name("changes-prevent-symbolic")
            button.set_tooltip_text("Kilitle")
        
        button.connect('clicked', self._on_lock_toggle, app, exec_path, is_locked)
        row.add_suffix(button)
        
        return row
    
    def _on_lock_toggle(self, button, app, exec_path, is_locked):
        """Handle lock/unlock button click"""
        if is_locked:
            # Unlock application
            success = self.main_window.app_locker.unlock_application_by_path(exec_path)
            if success:
                self.main_window.notifications.notify_app_unlocked(app['name'])
                self.refresh()
        else:
            # Lock application
            success = self.main_window.app_locker.lock_application(
                app_name=app['name'],
                app_path=exec_path,
                desktop_file=app.get('desktop_file'),
                icon_path=app.get('icon')
            )
            if success:
                self.main_window.notifications.notify_app_locked(app['name'])
                self.refresh()
    
    def _on_search_changed(self, entry):
        """Handle search text change"""
        search_text = entry.get_text().lower()
        
        # Filter list rows
        def filter_func(row):
            if isinstance(row, Adw.ActionRow):
                title = row.get_title().lower()
                subtitle = row.get_subtitle()
                if subtitle:
                    subtitle = subtitle.lower()
                    return search_text in title or search_text in subtitle
                return search_text in title
            return True
        
        self.apps_list.set_filter_func(filter_func)
    
    def refresh(self):
        """Refresh applications list"""
        self._load_applications()
