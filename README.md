# Kamera Tespit ve Simülasyon Sistemi

Bu depo, ağ üzerindeki IP kameralarını tespit etmek, güvenlik simülasyonları yapmak ve sonuçları JSON raporları şeklinde kaydetmek için hazırlanmış iki ana versiyon içerir: **simülasyon** (eğitim/test) ve **gerçek nmap tabanlı** (üretim/test ortamında dikkatli kullanım).

> ⚠️ **UYARI:** Bu araç sadece eğitim ve yetkili penetrasyon testleri içindir. Başkasının ağına izinsiz tarama veya saldırı denemesi yasa dışıdır.

---

## İçerik / Dosya Yapısı

```
Kamera-Tespit-Simulasyon/
├─ README.md
├─ kamera_simulasyon.py          # Simülasyon versiyonu (sahte nmap + exploit)
├─ gercek_nmap_kamera_tespit.py  # Gerçek nmap ile tarayan versiyon (XML parsing)
```

---

## Proje Özeti

* **Simülasyon Versiyonu** (`kamera_simulasyon.py`)

  * Eğitim ve test amaçlıdır.
  * Sahte nmap sonuçları üretir, açık port/servis/banners simüle eder.
  * Sahte exploit adımlarıyla zafiyet senaryoları çalıştırır (gerçek saldırı gerçekleştirmez).
  * JSON formatında detaylı rapor kaydeder.

* **Gerçek Nmap Versiyonu** (`gercek_nmap_kamera_tespit.py`)

  * Gerçek `nmap` çıktısını XML olarak alıp parse eder.
  * Banner, servis, versiyon ve OS bilgilerine göre kamera tespiti yapar.
  * `sudo` ile SYN scan (`-sS`) ve OS detection (`-O`) kullanılabilir.
  * Çıktıyı JSON raporuna dönüştürür.

---

## Desteklenen Marka / Modeller (Örnek)

* Hikvision: `DS-2CD2xxx`, `DS-7604NI`, `DS-7732NI`
* Dahua: `IPC-HFW4431R`, `NVR4104`
* Axis: `M3004`, `P1365`
* Foscam, Vivotek, Sony, Bosch, Panasonic, Canon, Samsung, Pelco, Geovision ...

> Not: Bu liste örnektir — gerçek ortamda banner tabanlı tespitte yanlış pozitif/negatifler olabilir.

---

## Kurulum

### Sistem Gereksinimleri

* Python 3.8+
* `nmap` (gerçek versiyon için)

### Hızlı Başlangıç (Simülasyon)

```bash
python3 kamera_simulasyon.py
# veya
python3 kamera_simulasyon.py --target 192.168.1.0/24 --output rapor.json
```

### Hızlı Başlangıç (Gerçek Nmap)

```bash
# nmap kurulu değilse (Debian/Ubuntu):
sudo apt update && sudo apt install -y nmap

# root ile daha detaylı tarama:
sudo python3 gercek_nmap_kamera_tespit.py --target 192.168.1.0/24 --out rapor.json

# sudo yoksa TCP connect tarama ile:
python3 gercek_nmap_kamera_tespit.py --target 192.168.1.0/24 --scan-type connect --out rapor.json
```

---

## Kullanım / Örnek Argümanlar

* `--target`    : Hedef IP ağı veya IP (örn: `192.168.1.0/24` veya `192.168.1.10`)
* `--out`       : JSON çıktı dosyası
* `--sudo`      : Sudo kullanılarak SYN scan ve OS detection aktifleştirme (gerçek nmap)
* `--scan-type` : `syn` | `connect` (varsayılan: `connect`)
* `--verbose`   : Konsola ayrıntılı çıktı yazma

---

## Tespit Yöntemleri

1. **Banner Analizi**: HTTP başlıkları, servis ürün/versiyon bilgileri.
2. **Port Tarama**: 80, 8080, 8000-8001, 8008, 8081, 8888, 9000 gibi tipik kamera portları.
3. **OS ve Servis Versiyonları**: `nmap -O -sV` çıktıları.
4. **Regex/Mappings**: Banner ve servis isimleri ile marka/model eşleştirmeleri.

---

## Örnek JSON Çıktı (Kısmi)

```json
{
  "report_time": "2025-10-24T22:10:21",
  "target": "192.168.1.0/24",
  "cameras": [
    {
      "ip": "192.168.1.10",
      "port": 80,
      "brand": "Hikvision",
      "model": "DS-7732NI",
      "os": "Linux",
      "banner": "Hikvision Web Server",
      "security_level": "medium",
      "detected_at": "2025-10-24T22:09:44"
    }
  ],
  "statistics": {
    "total_targets": 254,
    "found_cameras": 10
  }
}
```

---

## Güvenlik Uyarıları ve Etik Kurallar

* **Sadece** sahip olduğunuz veya izin verilen ağları tarayın.
* İzinsiz tarama, saldırı veya sömürü girişimleri yasa dışıdır.
* Bu proje eğitim amaçlıdır; gerçek penetrasyon testleri için yetkili uzmanlar ve sözleşmeler gereklidir.

---

## Geliştirme ve Katkı

1. Fork yapın
2. Yeni bir branch açın (`feature/yenilik`)
3. Değişiklik yapın
4. Pull request gönderin

**İyileştirilebilir özellikler**:

* Daha geniş model veri tabanı
* Banner fingerprinting için ML tabanlı sınıflandırıcı
* CVE/Exploit veritabanına bağlanma (sadece simülasyon dışındaysa dikkatli olun)

---

## İletişim

Projede değişiklik isterseniz veya yardıma ihtiyaç duyarsanız issue açın veya PR gönderin.

---

> Hazır şablonu GitHub deposuna eklemek isterseniz, README.md dosyasını repo köküne koyup `git init && git add . && git commit -m "Initial commit"` adımlarıyla başlayabilirsiniz.

---

## LICENSE

Aşağıda depoya ekleyebileceğiniz bir **MIT License** örneği bulunmaktadır. Eğer farklı bir lisans isterseniz (Apache-2.0, GPLv3, BSD vb.) söyleyin, değiştireyim.

```
MIT License

Copyright (c) 2025 Your Name or Organization

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---
