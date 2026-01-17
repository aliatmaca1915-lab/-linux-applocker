# Development Guide / Geliştirici Kılavuzu

## 🇹🇷 Türkçe

### Proje Yapısı

```
linux-applocker/
├── src/                        # Kaynak kod
│   ├── core/                   # Ana işlevsellik
│   │   ├── app_scanner.py     # .desktop dosyalarını tarama
│   │   ├── app_locker.py      # Uygulama kilitleme
│   │   ├── process_monitor.py # Process izleme
│   │   └── file_locker.py     # Dosya şifreleme
│   ├── crypto/                 # Şifreleme modülleri
│   │   ├── encryption.py      # AES-256-GCM
│   │   ├── password_manager.py # bcrypt şifre yönetimi
│   │   └── key_storage.py     # Anahtar saklama
│   ├── database/              # Veritabanı
│   │   ├── models.py          # SQLAlchemy modelleri
│   │   └── db_manager.py      # Veritabanı yöneticisi
│   ├── gui/                   # GTK4 arayüzü
│   │   ├── main_window.py     # Ana pencere
│   │   ├── applications_view.py
│   │   ├── files_view.py
│   │   ├── dashboard_view.py
│   │   └── settings_view.py
│   ├── utils/                 # Yardımcı modüller
│   │   ├── config.py          # Yapılandırma
│   │   ├── logger.py          # Loglama
│   │   └── notifications.py   # Bildirimler
│   ├── daemon/                # Arka plan servisi
│   │   └── service.py
│   └── main.py               # Giriş noktası
├── assets/                    # Varlıklar
│   ├── icons/                # İkonlar
│   └── styles/               # CSS stilleri
├── systemd/                   # Systemd servisi
├── docs/                      # Dokümantasyon
└── tests/                     # Testler
```

### Geliştirme Ortamı Kurulumu

#### 1. Depoyu Klonlayın

```bash
git clone https://github.com/aliatmaca1915-lab/-linux-applocker.git
cd -linux-applocker
```

#### 2. Virtual Environment Oluşturun

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Geliştirme Bağımlılıklarını Yükleyin

```bash
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy
```

#### 4. Uygulamayı Çalıştırın

```bash
python3 -m src.main
```

### Kod Standartları

#### Python Stil Kılavuzu

- **PEP 8** standartlarına uyun
- **Type hints** kullanın
- **Docstrings** yazın (Google stil)

#### Örnek:

```python
def encrypt_file(self, file_path: str, key: bytes) -> Tuple[str, bytes]:
    """
    Encrypt a file using AES-256-GCM
    
    Args:
        file_path: Path to file to encrypt
        key: Encryption key
        
    Returns:
        Tuple of (encrypted_path, nonce)
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    # Implementation
    pass
```

### Test Yazma

#### Unit Test Örneği

```python
import pytest
from src.crypto.encryption import FileEncryption

class TestFileEncryption:
    def setup_method(self):
        self.encryption = FileEncryption()
        
    def test_key_generation(self):
        key = self.encryption.generate_key()
        assert len(key) == 32  # 256 bits
        
    def test_encryption_decryption(self):
        data = b"Test data"
        key = self.encryption.generate_key()
        
        encrypted, nonce = self.encryption.encrypt_data(data, key)
        decrypted = self.encryption.decrypt_data(encrypted, key, nonce)
        
        assert decrypted == data
```

#### Test Çalıştırma

```bash
# Tüm testleri çalıştır
pytest

# Coverage ile
pytest --cov=src tests/

# Belirli bir test dosyası
pytest tests/test_encryption.py
```

### Kod Formatlama

```bash
# Black ile formatla
black src/

# Flake8 ile kontrol et
flake8 src/

# MyPy ile tip kontrolü
mypy src/
```

### Yeni Özellik Ekleme

#### 1. Branch Oluşturun

```bash
git checkout -b feature/yeni-ozellik
```

#### 2. Kodu Yazın

- Mümkünse TDD (Test-Driven Development) kullanın
- Küçük, anlamlı commit'ler yapın

#### 3. Test Edin

```bash
pytest
black src/
flake8 src/
```

#### 4. Pull Request Açın

- Değişiklikleri açıklayan detaylı bir açıklama yazın
- Test sonuçlarını ekleyin
- Ekran görüntüleri ekleyin (UI değişiklikleri için)

### Mimariye Genel Bakış

#### 1. Database Layer (models.py, db_manager.py)

SQLAlchemy ORM kullanarak veritabanı işlemlerini yönetir:
- Master şifre saklama
- Kilitli uygulamalar
- Şifreli dosyalar
- Erişim logları
- Ayarlar

#### 2. Crypto Layer (encryption.py, password_manager.py)

Şifreleme işlemlerini yönetir:
- AES-256-GCM ile dosya şifreleme
- bcrypt ile şifre hash'leme
- PBKDF2 ile anahtar türetme
- Keyring ile güvenli anahtar saklama

#### 3. Core Layer (app_locker.py, file_locker.py, process_monitor.py)

Ana işlevselliği sağlar:
- Uygulama kilitleme mantığı
- Dosya şifreleme işlemleri
- Process monitoring

#### 4. GUI Layer (GTK4 + LibAdwaita)

Modern kullanıcı arayüzü:
- MainWindow: Ana pencere ve koordinasyon
- Views: Dashboard, Applications, Files, Settings
- Dialogs: Password, Setup

#### 5. Utils Layer

Yardımcı işlevler:
- Config: Yapılandırma yönetimi
- Logger: Loglama
- Notifications: Bildirimler

### Güvenlik Notları

#### Şifre Yönetimi

- Şifreleri asla plain text olarak saklamayın
- bcrypt ile hash'leyin (minimum 12 rounds)
- Salt kullanın

#### Dosya Şifreleme

- AES-256-GCM kullanın (authenticated encryption)
- Her dosya için benzersiz nonce kullanın
- Orijinal dosyaları güvenli şekilde silin

#### Anahtar Yönetimi

- Anahtarları sistem keyring'inde saklayın
- Memory'de şifreleri temizleyin
- PBKDF2 ile key derivation yapın

### Performans İpuçları

#### Database

- Connection pooling kullanın
- Index'leri doğru kullanın
- Batch operations yapın

#### Process Monitoring

- İzleme intervalini optimize edin (varsayılan: 1 saniye)
- Sadece gerekli process bilgilerini alın
- Thread-safe olduğundan emin olun

#### File Encryption

- Büyük dosyalar için chunk-based encryption düşünün
- Progress callback'leri kullanın
- Async işlemler yapın

### Debug

#### Logları Görüntüleme

```bash
# Uygulama logları
tail -f ~/.local/share/linux-applocker/logs/applocker_*.log

# Systemd servis logları
journalctl --user -u linux-applocker.service -f
```

#### Debug Mode

```python
# Logger seviyesini DEBUG'a ayarlayın
logger.set_level('DEBUG')
```

### Katkıda Bulunma

1. Issue açın veya mevcut bir issue'yu seçin
2. Fork yapın
3. Feature branch oluşturun
4. Değişikliklerinizi yapın
5. Test edin
6. Pull request açın

### Lisans

MIT License - Detaylar için [LICENSE](../LICENSE) dosyasına bakın.

---

## 🇬🇧 English

### Project Structure

(Same as Turkish section)

### Development Environment Setup

(Same as Turkish section with English comments)

### Code Standards

Follow PEP 8 guidelines, use type hints, and write docstrings.

### Testing

Write unit tests for all functionality. Use pytest for testing.

### Contributing

1. Open an issue or choose an existing one
2. Fork the repository
3. Create a feature branch
4. Make your changes
5. Test thoroughly
6. Open a pull request
