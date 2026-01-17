"""
Linux AppLocker - Dashboard View
Shows statistics and recent activity
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw


class DashboardView(Gtk.Box):
    """Dashboard view with statistics"""
    
    def __init__(self, main_window):
        """Initialize dashboard view"""
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        
        self.main_window = main_window
        
        self.set_margin_top(24)
        self.set_margin_bottom(24)
        self.set_margin_start(24)
        self.set_margin_end(24)
        
        # Welcome section
        welcome_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        
        welcome_label = Gtk.Label(label="Linux AppLocker")
        welcome_label.add_css_class("title-1")
        welcome_box.append(welcome_label)
        
        subtitle = Gtk.Label(label="Uygulamalarınız ve dosyalarınız güvende")
        subtitle.add_css_class("dim-label")
        welcome_box.append(subtitle)
        
        self.append(welcome_box)
        
        # Statistics cards
        stats_flow = Gtk.FlowBox()
        stats_flow.set_selection_mode(Gtk.SelectionMode.NONE)
        stats_flow.set_max_children_per_line(3)
        stats_flow.set_column_spacing(12)
        stats_flow.set_row_spacing(12)
        
        # Get statistics from database
        stats = self.main_window.db.get_statistics()
        
        # Locked apps card
        self.locked_apps_card = self._create_stat_card(
            "🔒 Kilitli Uygulamalar",
            str(stats.get('locked_apps_count', 0)),
            "Şu anda kilitli"
        )
        stats_flow.append(self.locked_apps_card)
        
        # Encrypted files card
        self.encrypted_files_card = self._create_stat_card(
            "📁 Şifreli Dosyalar",
            str(stats.get('encrypted_files_count', 0)),
            "Şu anda şifreli"
        )
        stats_flow.append(self.encrypted_files_card)
        
        # Failed attempts card
        self.failed_attempts_card = self._create_stat_card(
            "⚠️ Başarısız Denemeler",
            str(stats.get('failed_attempts_today', 0)),
            "Bugün"
        )
        stats_flow.append(self.failed_attempts_card)
        
        self.append(stats_flow)
        
        # Recent activity section
        activity_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        
        activity_label = Gtk.Label(label="Son Aktiviteler")
        activity_label.add_css_class("title-3")
        activity_label.set_xalign(0)
        activity_box.append(activity_label)
        
        # Activity list
        self.activity_list = Gtk.ListBox()
        self.activity_list.add_css_class("boxed-list")
        
        # Get recent logs
        logs = self.main_window.db.get_access_logs(limit=10)
        
        if logs:
            for log in logs:
                row = self._create_activity_row(log)
                self.activity_list.append(row)
        else:
            empty_row = Adw.ActionRow()
            empty_row.set_title("Henüz aktivite yok")
            empty_row.set_subtitle("Uygulama veya dosya kilitlediğinizde burada görünecektir")
            self.activity_list.append(empty_row)
        
        activity_box.append(self.activity_list)
        
        self.append(activity_box)
    
    def _create_stat_card(self, title, value, subtitle):
        """Create a statistics card"""
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        card.set_size_request(250, 120)
        card.add_css_class("card")
        card.set_margin_top(12)
        card.set_margin_bottom(12)
        card.set_margin_start(12)
        card.set_margin_end(12)
        
        title_label = Gtk.Label(label=title)
        title_label.add_css_class("title-4")
        card.append(title_label)
        
        value_label = Gtk.Label(label=value)
        value_label.add_css_class("title-1")
        card.append(value_label)
        
        subtitle_label = Gtk.Label(label=subtitle)
        subtitle_label.add_css_class("dim-label")
        card.append(subtitle_label)
        
        return card
    
    def _create_activity_row(self, log):
        """Create an activity row"""
        row = Adw.ActionRow()
        
        # Set icon based on success
        icon = "emblem-ok-symbolic" if log.success else "dialog-error-symbolic"
        icon_image = Gtk.Image.new_from_icon_name(icon)
        row.add_prefix(icon_image)
        
        # Set title and subtitle
        resource_type = "Uygulama" if log.resource_type == 'app' else "Dosya"
        row.set_title(f"{resource_type}: {log.resource_name}")
        
        status = "Erişim başarılı" if log.success else "Erişim engellendi"
        timestamp = log.access_attempt_time.strftime("%d.%m.%Y %H:%M")
        row.set_subtitle(f"{status} - {timestamp}")
        
        return row
    
    def refresh(self):
        """Refresh dashboard data"""
        # Update statistics
        stats = self.main_window.db.get_statistics()
        
        # Update card values (simplified - would need to update labels inside cards)
        # In a real implementation, we'd store references to the value labels
        pass
