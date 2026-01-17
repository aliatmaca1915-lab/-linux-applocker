"""
Linux AppLocker - Setup Dialog
Initial setup wizard for first-time use
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw


class SetupDialog(Adw.Window):
    """Setup wizard for first-time use"""
    
    def __init__(self, parent=None):
        """Initialize setup dialog"""
        super().__init__()
        self.set_title("Linux AppLocker - İlk Kurulum")
        self.set_default_size(600, 500)
        self.set_modal(True)
        if parent:
            self.set_transient_for(parent)
        
        self.password = None
        self.setup_complete = False
        
        # Create main box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        # Header bar
        header = Adw.HeaderBar()
        header.set_show_end_title_buttons(False)
        main_box.append(header)
        
        # Content area with carousel
        self.carousel = Adw.Carousel()
        self.carousel.set_vexpand(True)
        main_box.append(self.carousel)
        
        # Carousel indicator
        carousel_dots = Adw.CarouselIndicatorDots()
        carousel_dots.set_carousel(self.carousel)
        main_box.append(carousel_dots)
        
        # Navigation buttons
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        button_box.set_margin_top(12)
        button_box.set_margin_bottom(12)
        button_box.set_margin_start(12)
        button_box.set_margin_end(12)
        button_box.set_halign(Gtk.Align.END)
        
        self.back_button = Gtk.Button(label="Geri")
        self.back_button.connect('clicked', self._on_back_clicked)
        button_box.append(self.back_button)
        
        self.next_button = Gtk.Button(label="İleri")
        self.next_button.add_css_class("suggested-action")
        self.next_button.connect('clicked', self._on_next_clicked)
        button_box.append(self.next_button)
        
        main_box.append(button_box)
        
        # Create pages
        self._create_welcome_page()
        self._create_password_page()
        self._create_finish_page()
        
        # Update button states
        self._update_buttons()
        
        self.set_content(main_box)
    
    def _create_welcome_page(self):
        """Create welcome page"""
        page = Adw.StatusPage()
        page.set_icon_name("security-high-symbolic")
        page.set_title("Linux AppLocker'a Hoş Geldiniz")
        page.set_description(
            "Uygulamalarınızı ve dosyalarınızı güvenli bir şekilde koruyun.\n\n"
            "Linux AppLocker ile:\n"
            "• Uygulamaları şifre ile kilitleyin\n"
            "• Dosyaları güvenli şekilde şifreleyin\n"
            "• Erişim denemelerini takip edin"
        )
        
        clamp = Adw.Clamp()
        clamp.set_child(page)
        self.carousel.append(clamp)
    
    def _create_password_page(self):
        """Create password setup page"""
        page_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        page_box.set_margin_top(48)
        page_box.set_margin_bottom(48)
        page_box.set_margin_start(48)
        page_box.set_margin_end(48)
        page_box.set_valign(Gtk.Align.CENTER)
        
        # Title
        title = Gtk.Label(label="Master Şifre Oluşturun")
        title.add_css_class("title-1")
        page_box.append(title)
        
        # Description
        desc = Gtk.Label(
            label="Bu şifre tüm kilitli kaynaklara erişim için kullanılacaktır.\n"
                  "Güvenli ve unutamayacağınız bir şifre seçin."
        )
        desc.set_wrap(True)
        desc.add_css_class("dim-label")
        page_box.append(desc)
        
        # Requirements
        req_frame = Gtk.Frame()
        req_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        req_box.set_margin_top(12)
        req_box.set_margin_bottom(12)
        req_box.set_margin_start(12)
        req_box.set_margin_end(12)
        
        req_title = Gtk.Label(label="Şifre Gereksinimleri:")
        req_title.add_css_class("heading")
        req_title.set_xalign(0)
        req_box.append(req_title)
        
        requirements = [
            "✓ En az 8 karakter",
            "✓ En az bir büyük harf",
            "✓ En az bir küçük harf",
            "✓ En az bir rakam",
            "✓ En az bir özel karakter (!@#$%^&*)"
        ]
        
        for req in requirements:
            label = Gtk.Label(label=req)
            label.set_xalign(0)
            req_box.append(label)
        
        req_frame.set_child(req_box)
        page_box.append(req_frame)
        
        # Password entry
        password_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        password_label = Gtk.Label(label="Şifre:")
        password_label.set_xalign(0)
        password_box.append(password_label)
        
        self.password_entry = Gtk.PasswordEntry()
        self.password_entry.set_show_peek_icon(True)
        self.password_entry.connect('changed', self._on_password_changed)
        password_box.append(self.password_entry)
        page_box.append(password_box)
        
        # Confirm password
        confirm_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        confirm_label = Gtk.Label(label="Şifre (Tekrar):")
        confirm_label.set_xalign(0)
        confirm_box.append(confirm_label)
        
        self.confirm_entry = Gtk.PasswordEntry()
        self.confirm_entry.set_show_peek_icon(True)
        self.confirm_entry.connect('changed', self._on_password_changed)
        confirm_box.append(self.confirm_entry)
        page_box.append(confirm_box)
        
        # Error label
        self.error_label = Gtk.Label(label="")
        self.error_label.add_css_class("error")
        self.error_label.set_visible(False)
        page_box.append(self.error_label)
        
        clamp = Adw.Clamp()
        clamp.set_maximum_size(500)
        clamp.set_child(page_box)
        self.carousel.append(clamp)
    
    def _create_finish_page(self):
        """Create finish page"""
        page = Adw.StatusPage()
        page.set_icon_name("emblem-ok-symbolic")
        page.set_title("Kurulum Tamamlandı!")
        page.set_description(
            "Linux AppLocker başarıyla kuruldu.\n\n"
            "Artık uygulamalarınızı ve dosyalarınızı koruyabilirsiniz."
        )
        
        clamp = Adw.Clamp()
        clamp.set_child(page)
        self.carousel.append(clamp)
    
    def _update_buttons(self):
        """Update button states based on current page"""
        current_page = self.carousel.get_position()
        n_pages = self.carousel.get_n_pages()
        
        # Update back button
        self.back_button.set_sensitive(current_page > 0)
        
        # Update next button
        if current_page >= n_pages - 1:
            self.next_button.set_label("Bitir")
        else:
            self.next_button.set_label("İleri")
        
        # Disable next on password page if password invalid
        if int(current_page) == 1:
            self._validate_password()
    
    def _on_back_clicked(self, button):
        """Handle back button click"""
        current = int(self.carousel.get_position())
        if current > 0:
            page = self.carousel.get_nth_page(current - 1)
            self.carousel.scroll_to(page, True)
            self._update_buttons()
    
    def _on_next_clicked(self, button):
        """Handle next button click"""
        current = int(self.carousel.get_position())
        n_pages = self.carousel.get_n_pages()
        
        # If on password page, validate
        if current == 1:
            if not self._validate_password():
                return
            self.password = self.password_entry.get_text()
        
        # Move to next page or finish
        if current < n_pages - 1:
            page = self.carousel.get_nth_page(current + 1)
            self.carousel.scroll_to(page, True)
            self._update_buttons()
        else:
            # Finish setup
            self.setup_complete = True
            self.close()
    
    def _on_password_changed(self, entry):
        """Handle password entry changes"""
        self._validate_password()
    
    def _validate_password(self) -> bool:
        """Validate password and show error if invalid"""
        from ..utils.validators import PasswordValidator
        
        password = self.password_entry.get_text()
        confirm = self.confirm_entry.get_text()
        
        # Check if passwords match
        if password != confirm:
            self.error_label.set_text("Şifreler eşleşmiyor")
            self.error_label.set_visible(True)
            self.next_button.set_sensitive(False)
            return False
        
        # Validate password strength
        is_valid, error_msg = PasswordValidator.validate(password)
        if not is_valid:
            self.error_label.set_text(error_msg)
            self.error_label.set_visible(True)
            self.next_button.set_sensitive(False)
            return False
        
        # Password is valid
        self.error_label.set_visible(False)
        self.next_button.set_sensitive(True)
        return True
    
    def get_password(self):
        """Get the created password"""
        return self.password
    
    def is_complete(self):
        """Check if setup was completed"""
        return self.setup_complete
