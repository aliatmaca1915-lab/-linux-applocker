# Installation Guide / Kurulum Kılavuzu

## 🇹🇷 Türkçe

### Sistem Gereksinimleri

- **İşletim Sistemi**: Linux Mint 20+ (veya Ubuntu 20.04+ tabanlı dağıtımlar)
- **Python**: 3.10 veya üzeri
- **GTK**: 4.0 veya üzeri
- **LibAdwaita**: 1.0 veya üzeri
- **Disk Alanı**: Minimum 50 MB
- **RAM**: Minimum 512 MB

### Otomatik Kurulum (Önerilen)

1. **Depoyu Klonlayın**
```bash
git clone https://github.com/aliatmaca1915-lab/-linux-applocker.git
cd -linux-applocker
```

2. **Kurulum Scriptini Çalıştırın**
```bash
chmod +x install.sh
./install.sh
```

Kurulum scripti otomatik olarak:
- Sistem bağımlılıklarını kontrol eder ve yükler
- Python paketlerini kurar
- Uygulama dosyalarını /opt/linux-applocker/ dizinine kopyalar
- Desktop entry'yi yükler
- İkonları kopyalar
- Systemd servisini kurar

3. **Uygulamayı Başlatın**
```bash
linux-applocker
```

Veya uygulama menüsünden "Linux AppLocker" arayın.

### Manuel Kurulum

#### Adım 1: Sistem Bağımlılıklarını Yükleyin

```bash
sudo apt update
sudo apt install -y \
    python3 \
    python3-pip \
    libgtk-4-1 \
    libadwaita-1-0 \
    gir1.2-gtk-4.0 \
    gir1.2-adw-1 \
    git
```

#### Adım 2: Python Bağımlılıklarını Yükleyin

```bash
cd -linux-applocker
pip3 install --user -r requirements.txt
```

#### Adım 3: Uygulamayı Kurun

```bash
sudo mkdir -p /opt/linux-applocker
sudo cp -r src assets systemd /opt/linux-applocker/
sudo cp requirements.txt /opt/linux-applocker/
```

#### Adım 4: Launcher Script Oluşturun

```bash
sudo tee /usr/local/bin/linux-applocker > /dev/null << 'EOF'
#!/bin/bash
cd /opt/linux-applocker
python3 -m src.main "$@"
EOF

sudo chmod +x /usr/local/bin/linux-applocker
```

#### Adım 5: Desktop Entry Yükleyin

```bash
sudo cp linux-applocker.desktop /usr/share/applications/
```

#### Adım 6: İkonları Yükleyin

```bash
sudo mkdir -p /usr/share/icons/hicolor/scalable/apps
sudo cp assets/icons/app-icon.svg /usr/share/icons/hicolor/scalable/apps/linux-applocker.svg
sudo gtk-update-icon-cache /usr/share/icons/hicolor/ 2>/dev/null || true
```

#### Adım 7: Systemd Servisini Kurun (Opsiyonel)

```bash
mkdir -p ~/.config/systemd/user
cp systemd/linux-applocker.service ~/.config/systemd/user/
systemctl --user daemon-reload
```

### Kurulum Sonrası

#### Uygulamayı Başlatın

```bash
linux-applocker
```

#### Arka Plan Servisini Etkinleştirin (Opsiyonel)

```bash
systemctl --user enable linux-applocker.service
systemctl --user start linux-applocker.service
```

#### Kurulumu Doğrulayın

```bash
# Uygulama versiyonunu kontrol edin
linux-applocker --help

# Servis durumunu kontrol edin
systemctl --user status linux-applocker.service
```

### Sorun Giderme

#### GTK/LibAdwaita Bulunamadı

```bash
sudo apt install libgtk-4-1 libadwaita-1-0 gir1.2-gtk-4.0 gir1.2-adw-1
```

#### Python Modülleri Bulunamadı

```bash
pip3 install --user --force-reinstall -r requirements.txt
```

#### İzin Hataları

```bash
# Script'lere çalıştırma izni verin
chmod +x install.sh uninstall.sh

# Kullanıcı dizinlerinin izinlerini kontrol edin
ls -la ~/.config/linux-applocker
ls -la ~/.local/share/linux-applocker
```

#### Uygulama Başlamıyor

```bash
# Logları kontrol edin
cat ~/.local/share/linux-applocker/logs/applocker_*.log

# Python versiyonunu kontrol edin
python3 --version  # 3.10+ olmalı
```

---

## 🇬🇧 English

### System Requirements

- **Operating System**: Linux Mint 20+ (or Ubuntu 20.04+ based distributions)
- **Python**: 3.10 or higher
- **GTK**: 4.0 or higher
- **LibAdwaita**: 1.0 or higher
- **Disk Space**: Minimum 50 MB
- **RAM**: Minimum 512 MB

### Automatic Installation (Recommended)

1. **Clone the Repository**
```bash
git clone https://github.com/aliatmaca1915-lab/-linux-applocker.git
cd -linux-applocker
```

2. **Run the Installation Script**
```bash
chmod +x install.sh
./install.sh
```

The installation script automatically:
- Checks and installs system dependencies
- Installs Python packages
- Copies application files to /opt/linux-applocker/
- Installs desktop entry
- Copies icons
- Installs systemd service

3. **Launch the Application**
```bash
linux-applocker
```

Or search for "Linux AppLocker" in your application menu.

### Manual Installation

Follow the same steps as in Turkish section above.

### Post-Installation

#### Launch the Application

```bash
linux-applocker
```

#### Enable Background Service (Optional)

```bash
systemctl --user enable linux-applocker.service
systemctl --user start linux-applocker.service
```

### Troubleshooting

Same as Turkish section above.
