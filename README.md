# Linux AppLocker 🔒

**Profesyonel Uygulama ve Dosya Kilitleme Sistemi - Linux Mint için**

[English](#english) | [Türkçe](#türkçe)

---

<a name="türkçe"></a>
## 🇹🇷 Türkçe

### 📋 Özellikler

- 🔐 **Uygulama Kilitleme** - Sistemdeki uygulamaları şifre ile koruma
- 📁 **Dosya Şifreleme** - AES-256-GCM ile güvenli dosya kilitleme
- 🎨 **Modern GTK4 Arayüzü** - LibAdwaita ile şık ve modern tasarım
- 🔑 **Master Şifre Sistemi** - Güçlü bcrypt şifreleme
- 📊 **Güvenlik Dashboard'u** - İstatistikler ve aktivite takibi
- 🔔 **Bildirimler** - Erişim denemelerinde sistem bildirimleri
- 🌙 **Tema Desteği** - Otomatik, açık ve koyu mod
- ⚡ **Arka Plan Servisi** - Systemd ile sürekli koruma
- 🛡️ **Process Monitoring** - Kilitli uygulamaları gerçek zamanlı izleme
- 🔒 **Güvenli Silme** - Dosyaları güvenli şekilde üzerine yazarak silme

### 📦 Kurulum

#### Gereksinimler

- Python 3.10 veya üzeri
- GTK 4.0
- LibAdwaita 1.0
- Linux Mint 20+ (veya uyumlu bir dağıtım)

#### Otomatik Kurulum

```bash
git clone https://github.com/aliatmaca1915-lab/-linux-applocker.git
cd -linux-applocker
chmod +x install.sh
./install.sh
```

Detaylı kurulum talimatları için [INSTALLATION.md](docs/INSTALLATION.md) dosyasına bakın.

### 🚀 Kullanım

#### İlk Başlatma

```bash
linux-applocker
```

İlk açılışta master şifre oluşturma sihirbazı açılacaktır. Güvenli bir şifre oluşturun:
- En az 8 karakter
- Büyük ve küçük harf
- Rakam
- Özel karakter (!@#$%^&*)

Detaylı kullanım kılavuzu için [USER_GUIDE.md](docs/USER_GUIDE.md) dosyasına bakın.

### 🔒 Güvenlik

- **AES-256-GCM** şifreleme ile dosya koruması
- **bcrypt** ile master şifre hash'leme (12 rounds)
- **PBKDF2** ile anahtar türetme (100,000 iterasyon)
- Şifreli anahtarlar sistem keyring'inde saklanır
- Brute force koruması (3 yanlış denemeden sonra timeout)
- Güvenli dosya silme (3 geçişli üzerine yazma)

### 🗑️ Kaldırma

```bash
./uninstall.sh
```

---

<a name="english"></a>
## 🇬🇧 English

### 📋 Features

- 🔐 **Application Locking** - Protect system applications with password
- 📁 **File Encryption** - Secure file locking with AES-256-GCM
- 🎨 **Modern GTK4 Interface** - Beautiful design with LibAdwaita
- 🔑 **Master Password System** - Strong bcrypt encryption
- 📊 **Security Dashboard** - Statistics and activity tracking
- 🔔 **Notifications** - System notifications on access attempts
- 🌙 **Theme Support** - Auto, light and dark mode
- ⚡ **Background Service** - Continuous protection with systemd
- 🛡️ **Process Monitoring** - Real-time monitoring of locked applications
- 🔒 **Secure Delete** - Securely overwrite and delete files

### 📦 Installation

#### Requirements

- Python 3.10 or higher
- GTK 4.0
- LibAdwaita 1.0
- Linux Mint 20+ (or compatible distribution)

#### Automatic Installation

```bash
git clone https://github.com/aliatmaca1915-lab/-linux-applocker.git
cd -linux-applocker
chmod +x install.sh
./install.sh
```

For detailed installation instructions, see [INSTALLATION.md](docs/INSTALLATION.md).

### 🚀 Usage

#### First Launch

```bash
linux-applocker
```

On first launch, the master password setup wizard will open. Create a secure password:
- At least 8 characters
- Upper and lowercase letters
- Numbers
- Special characters (!@#$%^&*)

For detailed usage guide, see [USER_GUIDE.md](docs/USER_GUIDE.md).

### 🔒 Security

- **AES-256-GCM** encryption for file protection
- **bcrypt** for master password hashing (12 rounds)
- **PBKDF2** for key derivation (100,000 iterations)
- Encrypted keys stored in system keyring
- Brute force protection (timeout after 3 failed attempts)
- Secure file deletion (3-pass overwrite)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

For development guidelines, see [DEVELOPMENT.md](docs/DEVELOPMENT.md).

## 📧 Support

For issues and questions, please use the [GitHub Issues](https://github.com/aliatmaca1915-lab/-linux-applocker/issues) page.

---

**Made with ❤️ for Linux Mint users**
