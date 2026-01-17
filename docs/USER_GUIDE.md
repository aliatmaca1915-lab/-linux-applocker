# User Guide / Kullanıcı Kılavuzu

## 🇹🇷 Türkçe

### İçindekiler
1. [İlk Kurulum](#ilk-kurulum)
2. [Uygulama Kilitleme](#uygulama-kilitleme)
3. [Dosya Şifreleme](#dosya-şifreleme)
4. [Dashboard](#dashboard)
5. [Ayarlar](#ayarlar)
6. [SSS](#sss)

---

### İlk Kurulum

#### Master Şifre Oluşturma

Linux AppLocker'ı ilk kez başlattığınızda, master şifre oluşturma sihirbazı açılacaktır.

1. **Hoş Geldin Ekranı**: "İleri" butonuna tıklayın
2. **Şifre Oluşturma**: Güvenli bir şifre oluşturun
   - Minimum 8 karakter
   - En az bir büyük harf
   - En az bir küçük harf
   - En az bir rakam
   - En az bir özel karakter (!@#$%^&*)
3. **Şifre Onayı**: Şifrenizi tekrar girin
4. **Tamamlandı**: "Bitir" butonuna tıklayın

⚠️ **Önemli**: Master şifrenizi unutmayın! Bu şifre olmadan kilitli kaynaklara erişemezsiniz.

---

### Uygulama Kilitleme

#### Uygulama Nasıl Kilitlenir?

1. **Uygulamalar Sekmesine Gidin**
   - Ana pencerede "Uygulamalar" sekmesine tıklayın

2. **Uygulama Arama**
   - Üstteki arama kutusuna uygulama adını yazın
   - Liste otomatik olarak filtrelenecektir

3. **Uygulamayı Kilitleme**
   - Kilitlemek istediğiniz uygulamanın yanındaki kilit simgesine tıklayın
   - Uygulama kilitli olarak işaretlenecek
   - Bildirim alacaksınız

4. **Kilitli Uygulamaya Erişim**
   - Kilitli bir uygulamayı açmaya çalıştığınızda:
   - Process monitor uygulamayı algılar
   - Uygulama durdurulur
   - Şifre istenecek (planlanmış özellik - şu anda process sonlandırılır)

#### Uygulama Kilidini Açma

1. Uygulamanın yanındaki yeşil kilidi aç simgesine tıklayın
2. Uygulama artık normal şekilde açılabilir

---

### Dosya Şifreleme

#### Tek Dosya Şifreleme

1. **Dosyalar Sekmesine Gidin**

2. **Dosya Ekle Butonuna Tıklayın**
   - "Dosya Ekle" butonuna tıklayın
   - Şifrelemek istediğiniz dosyayı seçin

3. **Şifreleme İşlemi**
   - Dosya AES-256-GCM ile şifrelenir
   - Orijinal dosya güvenli şekilde silinir
   - .locked uzantılı şifreli dosya oluşturulur
   - Dosya listesinde görünür

#### Klasör Şifreleme

1. **Klasör Ekle Butonuna Tıklayın**
   - "Klasör Ekle" butonuna tıklayın
   - Şifrelemek istediğiniz klasörü seçin

2. **Onay**
   - Tüm dosyaların şifreleneceği uyarısı görünür
   - "Evet" butonuna tıklayın

3. **Şifreleme İşlemi**
   - Klasördeki tüm dosyalar şifrelenir
   - İşlem bittiğinde kaç dosya şifrelendiği gösterilir

#### Dosya Şifresini Çözme

1. Şifrelenmiş dosyanın yanındaki kilidi aç simgesine tıklayın
2. Dosya şifresi çözülür ve orijinal haline döner
3. .locked dosyası silinir

---

### Dashboard

Dashboard, güvenlik durumunuzun genel görünümünü sunar.

#### İstatistikler

- **Kilitli Uygulamalar**: Şu anda kilitli olan uygulama sayısı
- **Şifreli Dosyalar**: Şu anda şifreli olan dosya sayısı
- **Başarısız Denemeler**: Bugünkü başarısız erişim denemeleri

#### Son Aktiviteler

Dashboard'da son erişim denemelerini görebilirsiniz:
- Kaynak türü (Uygulama/Dosya)
- Kaynak adı
- Başarı durumu
- Tarih ve saat

---

### Ayarlar

#### Güvenlik Ayarları

**Master Şifre Değiştir**
- Mevcut master şifrenizi değiştirin
- Yeni şifre aynı gereksinimleri karşılamalıdır

**Otomatik Kilitleme Süresi**
- Belirlenen süre sonra otomatik kilitleme (dakika)
- Varsayılan: 5 dakika

#### Görünüm Ayarları

**Tema**
- Otomatik: Sistem temasını takip eder
- Açık: Daima açık tema
- Koyu: Daima koyu tema

#### Bildirim Ayarları

**Bildirimleri Etkinleştir**
- Erişim denemelerinde bildirim gösterir
- Dosya şifreleme/çözme işlemlerinde bildirim

#### Sistem Ayarları

**Başlangıçta Çalıştır**
- Sistem açılışında otomatik başlatma
- Arka plan servisini etkinleştirir

**Process Monitor Durumu**
- Process monitor'ün çalışma durumunu gösterir

---

### SSS

#### Soru: Master şifremi unuttum, ne yapmalıyım?

Cevap: Maalesef master şifreyi sıfırlama yöntemi yoktur. Güvenlik nedeniyle şifre kurtarma özelliği bulunmamaktadır. Veritabanını sıfırlamak için:
```bash
rm -rf ~/.local/share/linux-applocker
rm -rf ~/.config/linux-applocker
```
⚠️ Bu işlem tüm kilitli uygulama ve şifreli dosya bilgilerini siler!

#### Soru: Şifreli bir dosyayı yedekleyebilir miyim?

Cevap: Evet, .locked dosyalarını kopyalayabilir veya yedekleyebilirsiniz. Ancak şifre çözmek için aynı sistem ve aynı master şifre gereklidir.

#### Soru: Uygulama çok fazla RAM kullanıyor?

Cevap: Normal çalışmada Linux AppLocker 50-100 MB RAM kullanır. Process monitoring aktifse bu 100-150 MB'a çıkabilir.

#### Soru: Hangi dosya formatları şifrelenebilir?

Cevap: Tüm dosya formatları şifrelenebilir (metin, resim, video, arşiv vb.). AES-256-GCM binary düzeyde şifreleme yapar.

#### Soru: Birden fazla kullanıcı aynı bilgisayarda Linux AppLocker kullanabilir mi?

Cevap: Evet, her kullanıcının kendi master şifresi ve kendi kilitli kaynakları olur. Veriler kullanıcı home dizininde saklanır.

#### Soru: Kilitli bir uygulamayı terminal'den açabilir miyim?

Cevap: Process monitor aktifse, terminal'den açılan kilitli uygulamalar da tespit edilir ve durdurulur.

---

## 🇬🇧 English

### Contents
1. [Initial Setup](#initial-setup-en)
2. [Application Locking](#application-locking-en)
3. [File Encryption](#file-encryption-en)
4. [Dashboard](#dashboard-en)
5. [Settings](#settings-en)
6. [FAQ](#faq-en)

---

<a name="initial-setup-en"></a>
### Initial Setup

#### Creating Master Password

When you launch Linux AppLocker for the first time, the master password creation wizard will open.

1. **Welcome Screen**: Click "Next" button
2. **Password Creation**: Create a secure password
   - Minimum 8 characters
   - At least one uppercase letter
   - At least one lowercase letter
   - At least one number
   - At least one special character (!@#$%^&*)
3. **Password Confirmation**: Re-enter your password
4. **Complete**: Click "Finish" button

⚠️ **Important**: Don't forget your master password! You cannot access locked resources without it.

---

<a name="application-locking-en"></a>
### Application Locking

#### How to Lock an Application?

1. **Go to Applications Tab**
   - Click "Applications" tab in main window

2. **Search Application**
   - Type application name in search box
   - List will be filtered automatically

3. **Lock Application**
   - Click lock icon next to the application
   - Application will be marked as locked
   - You'll receive a notification

4. **Access Locked Application**
   - When trying to open a locked application:
   - Process monitor detects the application
   - Application is stopped
   - Password will be requested (planned feature - currently process is terminated)

---

<a name="faq-en"></a>
### FAQ

#### Question: I forgot my master password, what should I do?

Answer: Unfortunately, there is no way to reset the master password. For security reasons, there is no password recovery feature. To reset the database:
```bash
rm -rf ~/.local/share/linux-applocker
rm -rf ~/.config/linux-applocker
```
⚠️ This will delete all locked application and encrypted file information!

#### Question: Can I backup an encrypted file?

Answer: Yes, you can copy or backup .locked files. However, you need the same system and same master password to decrypt them.

#### Question: Which file formats can be encrypted?

Answer: All file formats can be encrypted (text, images, videos, archives, etc.). AES-256-GCM performs binary-level encryption.
