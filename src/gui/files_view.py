"""
Linux AppLocker - Files View
Shows encrypted files and allows encryption/decryption
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib
import os


class FilesView(Gtk.Box):
    """Files view"""
    
    def __init__(self, main_window):
        """Initialize files view"""
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        
        self.main_window = main_window
        
        # Toolbar
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        toolbar.set_margin_top(12)
        toolbar.set_margin_bottom(12)
        toolbar.set_margin_start(12)
        toolbar.set_margin_end(12)
        
        # Add file button
        add_file_button = Gtk.Button(label="Dosya Ekle")
        add_file_button.set_icon_name("document-new-symbolic")
        add_file_button.add_css_class("suggested-action")
        add_file_button.connect('clicked', self._on_add_file)
        toolbar.append(add_file_button)
        
        # Add folder button
        add_folder_button = Gtk.Button(label="Klasör Ekle")
        add_folder_button.set_icon_name("folder-new-symbolic")
        add_folder_button.connect('clicked', self._on_add_folder)
        toolbar.append(add_folder_button)
        
        # Spacer
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        toolbar.append(spacer)
        
        # Refresh button
        refresh_button = Gtk.Button()
        refresh_button.set_icon_name("view-refresh-symbolic")
        refresh_button.set_tooltip_text("Yenile")
        refresh_button.connect('clicked', lambda b: self.refresh())
        toolbar.append(refresh_button)
        
        self.append(toolbar)
        
        # Scrolled window for files list
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        
        # Files list
        self.files_list = Gtk.ListBox()
        self.files_list.add_css_class("boxed-list")
        self.files_list.set_margin_top(12)
        self.files_list.set_margin_bottom(12)
        self.files_list.set_margin_start(12)
        self.files_list.set_margin_end(12)
        
        scrolled.set_child(self.files_list)
        self.append(scrolled)
        
        # Load encrypted files
        self._load_files()
    
    def _load_files(self):
        """Load encrypted files"""
        # Clear existing rows
        while True:
            row = self.files_list.get_row_at_index(0)
            if row is None:
                break
            self.files_list.remove(row)
        
        # Get encrypted files
        files = self.main_window.file_locker.get_locked_files()
        
        if files:
            for file in files:
                row = self._create_file_row(file)
                self.files_list.append(row)
        else:
            empty_row = Adw.ActionRow()
            empty_row.set_title("Henüz şifrelenmiş dosya yok")
            empty_row.set_subtitle("'Dosya Ekle' veya 'Klasör Ekle' butonlarını kullanarak dosya ekleyin")
            self.files_list.append(empty_row)
    
    def _create_file_row(self, file):
        """Create a row for an encrypted file"""
        row = Adw.ActionRow()
        
        # File name from original path
        file_name = os.path.basename(file.original_path)
        row.set_title(file_name)
        
        # File info
        file_size_mb = file.file_size / (1024 * 1024) if file.file_size else 0
        encrypted_time = file.encrypted_at.strftime("%d.%m.%Y %H:%M")
        row.set_subtitle(f"{file_size_mb:.2f} MB - Şifrelendi: {encrypted_time}")
        
        # File icon
        icon = Gtk.Image.new_from_icon_name("document-properties-symbolic")
        icon.set_pixel_size(32)
        row.add_prefix(icon)
        
        # Unlock button
        unlock_button = Gtk.Button()
        unlock_button.set_icon_name("changes-allow-symbolic")
        unlock_button.set_tooltip_text("Şifre Çöz")
        unlock_button.add_css_class("success")
        unlock_button.connect('clicked', self._on_unlock_file, file)
        row.add_suffix(unlock_button)
        
        return row
    
    def _on_add_file(self, button):
        """Handle add file button click"""
        dialog = Gtk.FileDialog()
        dialog.set_title("Şifrelenecek Dosya Seçin")
        
        def on_response(dialog, result):
            try:
                file = dialog.open_finish(result)
                if file:
                    file_path = file.get_path()
                    self._encrypt_file(file_path)
            except Exception as e:
                print(f"File selection error: {e}")
        
        dialog.open(self.main_window, None, on_response)
    
    def _on_add_folder(self, button):
        """Handle add folder button click"""
        dialog = Gtk.FileDialog()
        dialog.set_title("Şifrelenecek Klasör Seçin")
        
        def on_response(dialog, result):
            try:
                folder = dialog.select_folder_finish(result)
                if folder:
                    folder_path = folder.get_path()
                    self._encrypt_folder(folder_path)
            except Exception as e:
                print(f"Folder selection error: {e}")
        
        dialog.select_folder(self.main_window, None, on_response)
    
    def _encrypt_file(self, file_path):
        """Encrypt a file"""
        # Show progress dialog
        progress_dialog = Adw.MessageDialog.new(self.main_window)
        progress_dialog.set_heading("Dosya Şifreleniyor")
        progress_dialog.set_body(f"Lütfen bekleyin...")
        
        def do_encrypt():
            success = self.main_window.file_locker.lock_file(file_path)
            
            def on_complete():
                progress_dialog.close()
                if success:
                    file_name = os.path.basename(file_path)
                    self.main_window.notifications.notify_file_encrypted(file_name)
                    self.refresh()
                else:
                    error_dialog = Adw.MessageDialog.new(self.main_window)
                    error_dialog.set_heading("Hata")
                    error_dialog.set_body("Dosya şifrelenemedi")
                    error_dialog.add_response("ok", "Tamam")
                    error_dialog.present()
            
            GLib.idle_add(on_complete)
        
        import threading
        thread = threading.Thread(target=do_encrypt, daemon=True)
        thread.start()
        
        progress_dialog.present()
    
    def _encrypt_folder(self, folder_path):
        """Encrypt all files in a folder"""
        # Show confirmation dialog
        dialog = Adw.MessageDialog.new(self.main_window)
        dialog.set_heading("Klasör Şifreleme")
        dialog.set_body(f"Bu klasördeki tüm dosyalar şifrelenecek. Devam etmek istiyor musunuz?")
        dialog.add_response("cancel", "İptal")
        dialog.add_response("ok", "Evet")
        dialog.set_response_appearance("ok", Adw.ResponseAppearance.SUGGESTED)
        
        def on_response(dialog, response):
            if response == "ok":
                # Show progress
                progress_dialog = Adw.MessageDialog.new(self.main_window)
                progress_dialog.set_heading("Klasör Şifreleniyor")
                progress_dialog.set_body("Lütfen bekleyin...")
                
                def do_encrypt():
                    count = self.main_window.file_locker.lock_directory(folder_path, recursive=True)
                    
                    def on_complete():
                        progress_dialog.close()
                        result_dialog = Adw.MessageDialog.new(self.main_window)
                        result_dialog.set_heading("Tamamlandı")
                        result_dialog.set_body(f"{count} dosya şifrelendi")
                        result_dialog.add_response("ok", "Tamam")
                        result_dialog.present()
                        self.refresh()
                    
                    GLib.idle_add(on_complete)
                
                import threading
                thread = threading.Thread(target=do_encrypt, daemon=True)
                thread.start()
                
                progress_dialog.present()
        
        dialog.connect('response', on_response)
        dialog.present()
    
    def _on_unlock_file(self, button, file):
        """Handle unlock file button click"""
        # Show progress dialog
        progress_dialog = Adw.MessageDialog.new(self.main_window)
        progress_dialog.set_heading("Dosya Şifresi Çözülüyor")
        progress_dialog.set_body("Lütfen bekleyin...")
        
        def do_decrypt():
            success = self.main_window.file_locker.unlock_file(file.encrypted_path)
            
            def on_complete():
                progress_dialog.close()
                if success:
                    file_name = os.path.basename(file.original_path)
                    self.main_window.notifications.notify_file_decrypted(file_name)
                    self.refresh()
                else:
                    error_dialog = Adw.MessageDialog.new(self.main_window)
                    error_dialog.set_heading("Hata")
                    error_dialog.set_body("Dosya şifresi çözülemedi")
                    error_dialog.add_response("ok", "Tamam")
                    error_dialog.present()
            
            GLib.idle_add(on_complete)
        
        import threading
        thread = threading.Thread(target=do_decrypt, daemon=True)
        thread.start()
        
        progress_dialog.present()
    
    def refresh(self):
        """Refresh files list"""
        self._load_files()
