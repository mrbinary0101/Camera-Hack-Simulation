# Kamera Tespit ve Simülasyon Sistemi

Bu proje, ağ üzerindeki kameraları tespit etmek ve güvenlik simülasyonu yapmak için geliştirilmiştir.

## 📁 Dosyalar

### 1. `kamera_simulasyon.py` - Simülasyon Versiyonu
- **Amaç**: Eğitim ve test amaçlı simülasyon
- **Özellikler**:
  - Sahte nmap tarama sonuçları
  - Kamera tespit simülasyonu
  - Sahte exploit simülasyonu
  - Detaylı raporlama
  - JSON çıktı

### 2. `gercek_nmap_kamera_tespit.py` - Gerçek Nmap Versiyonu
- **Amaç**: Gerçek ağ tarama ve kamera tespit
- **Özellikler**:
  - Gerçek nmap tarama
  - Sudo yetkisi desteği
  - SYN scan ve OS detection
  - XML çıktı parsing
  - Kamera tespit algoritması
  - Detaylı raporlama

## 🚀 Kullanım

### Simülasyon Versiyonu
```bash
python3 kamera_simulasyon.py
```

### Gerçek Nmap Versiyonu
```bash
# Önce nmap'i yükleyin
sudo apt install nmap  # Ubuntu/Debian
sudo yum install nmap  # CentOS/RHEL
sudo pacman -S nmap    # Arch

# Sonra çalıştırın
python3 gercek_nmap_kamera_tespit.py

# Sudo yetkisi ile daha detaylı tarama için:
sudo python3 gercek_nmap_kamera_tespit.py
```

## 🎯 Desteklenen Kamera Markaları

- **Hikvision** - DS-2CD2xxx, DS-7604NI, DS-7732NI
- **Hikingson** - HS-IP-2000, HS-IP-3000, HS-IP-4000
- **Dahua** - IPC-HFW4431R, NVR4104, DHI-NVR2104
- **Axis** - M3004, P1365, Q1615
- **Apple** - HomeKit Camera, iSight Pro, FaceTime HD
- **Samsung** - SNV-6013, SNV-6014, SNV-6015
- **Sony** - SNC-VB600, SNC-VB630, SNC-VB635
- **Bosch** - FLEXIDOME, AUTODOME, MIC
- **Panasonic** - WV-SP102, WV-SP103, WV-SP104
- **Canon** - VB-C50i, VB-C60i, VB-C70i
- **Foscam** - FI9821P, FI8910W, FI9900P
- **Vivotek** - FD8161, FD8162, FD8163
- **Mobotix** - M15, M16, M25
- **Pelco** - Sarix, Spectra, Endura
- **Geovision** - GV-ABL130, GV-ABL140, GV-ABL150

## 🔍 Tespit Yöntemleri

### Banner Analizi
- HTTP başlıkları
- Servis versiyonları
- Ürün bilgileri
- OS tespiti

### Port Tarama
- 80 (HTTP)
- 8080 (HTTP Alternatif)
- 8000-8001 (Kamera Portları)
- 8008 (Kamera Portları)
- 8081 (Kamera Portları)
- 8888 (Kamera Portları)
- 9000 (Kamera Portları)

## 📊 Çıktı Formatları

### Konsol Çıktısı
- Detaylı kamera bilgileri
- Exploit simülasyon sonuçları
- İstatistikler

### JSON Raporu
- Tüm tespit edilen kameralar
- Detaylı teknik bilgiler
- Tarih ve saat bilgileri
- Güvenlik seviyeleri

## ⚠️ Güvenlik Uyarıları

1. **Sadece kendi ağınızda kullanın**
2. **İzinsiz tarama yapmayın**
3. **Bu araçlar eğitim amaçlıdır**
4. **Gerçek sistemlere zarar vermez**

## 🔐 Sudo Yetkisi

### Neden Sudo Gerekli?
- **SYN Scan (-sS)**: Root yetkisi gerektirir
- **OS Detection (-O)**: Root yetkisi gerektirir
- **Daha hızlı tarama**: SYN scan TCP connect'ten daha hızlıdır
- **Daha az tespit edilir**: SYN scan daha gizli çalışır

### Sudo Olmadan Çalışma
- **TCP Connect Scan (-sT)**: Normal kullanıcı yetkisi yeterli
- **Servis Detection (-sV)**: Normal kullanıcı yetkisi yeterli
- **HTTP Scripts**: Normal kullanıcı yetkisi yeterli

### Sudo ile Çalışma
```bash
# Sudo yetkisi ile çalıştırma
sudo python3 gercek_nmap_kamera_tespit.py

# Veya sudo yetkisi olmadan çalıştırma
python3 gercek_nmap_kamera_tespit.py
```

## 🛠️ Gereksinimler

### Simülasyon Versiyonu
- Python 3.6+
- Standart kütüphaneler

### Gerçek Nmap Versiyonu
- Python 3.6+
- Nmap (yüklü olmalı)
- xml.etree.ElementTree
- subprocess

## 📈 Özellikler

### Simülasyon Versiyonu
- ✅ Sahte ağ tarama
- ✅ Kamera tespit simülasyonu
- ✅ Sahte exploit simülasyonu
- ✅ Detaylı raporlama
- ✅ JSON çıktı
- ✅ Güvenlik seviyesi analizi

### Gerçek Nmap Versiyonu
- ✅ Gerçek nmap tarama
- ✅ XML çıktı parsing
- ✅ Kamera tespit algoritması
- ✅ Detaylı raporlama
- ✅ JSON çıktı
- ✅ OS tespiti

## 🎬 Simülasyon Senaryosu

1. **Ağ Tarama**: Hedef ağ aralığı taranır
2. **Port Tespit**: Açık portlar bulunur
3. **Servis Analizi**: HTTP servisleri analiz edilir
4. **Kamera Tespit**: Banner ve OS bilgilerinden kamera tespiti
5. **Exploit Simülasyonu**: Sahte exploit denemeleri
6. **Raporlama**: Detaylı rapor oluşturma

## 📝 Örnek Çıktı

```
🎬 Kamera Tespit ve Exploit Simülasyonu
==================================================
⚠️  Bu bir simülasyondur! Gerçek sistemlere zarar vermez.
==================================================

🔍 Ağ Tarama Başlatılıyor: 192.168.1.0/24
==================================================
📡 Tarama sonuçları:
   192.168.1.10:80 - http - Linux - Hikvision Web Server
   192.168.1.15:80 - http - Linux - Hikingson Camera System
   ...

🎥 Kamera Tespit Analizi Başlatılıyor...
==================================================

📹 Tespit Edilen Kameralar (10 adet):
============================================================

🎯 Kamera #1
   IP Adresi: 192.168.1.10
   Port: 80
   Marka: HIKVISION
   Model: DS-7732NI
   İşletim Sistemi: Linux
   Banner: Hikvision Web Server
   Güvenlik Seviyesi: Orta
   Açık Portlar: 80, 8535
   Tespit Tarihi: 2025-10-24 22:09:44

💥 Exploit Simülasyonu Başlatılıyor...
==================================================

🎯 Hedef: 192.168.1.10 (HIKVISION DS-7732NI)
   ⚡ Port tarama yapılıyor...
   ⚡ Servis versiyonu tespit ediliyor...
   ⚡ Zafiyet analizi yapılıyor...
   ⚡ Exploit payload hazırlanıyor...
   ⚡ Bağlantı kuruluyor...
   ⚡ Komut çalıştırılıyor...
   ⚡ Shell erişimi sağlanıyor...
   ✅ BAŞARILI - Shell erişimi: root

📊 Exploit Sonuçları:
==================================================
✅ Başarılı: 7
❌ Başarısız: 3
📈 Başarı Oranı: 70.0%

📋 Simülasyon Raporu
==================================================
📄 Rapor kaydedildi: kamera_simulasyon_raporu_20251024_221021.json
🎯 Toplam Kamera: 10
💥 Başarılı Exploit: 7

🎉 Simülasyon tamamlandı!
```

## 🔧 Geliştirme

Bu proje eğitim amaçlı geliştirilmiştir. Gerçek güvenlik testleri için profesyonel araçlar kullanın.

## 📄 Lisans

Bu proje eğitim amaçlıdır. Ticari kullanım için izin alın.
