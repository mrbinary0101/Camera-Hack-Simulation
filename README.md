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
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.

Preamble

The GNU General Public License is a free, copyleft license for software and other kinds of works.

The licenses for most software and other practical works are designed to take away your freedom to share and change the works. By contrast, the GNU General Public License is intended to guarantee your freedom to share and change all versions of a program—to make sure it remains free software for all its users. We, the Free Software Foundation, use the GNU General Public License for most of our software; it also applies to any other work released this way by its authors. You can apply it to your programs, too.

When we speak of free software, we are referring to freedom, not price. Our General Public Licenses are designed to make sure that you have the freedom to distribute copies of free software (and charge for them if you wish), that you receive source code or can get it if you want it, that you can change the software or use pieces of it in new free programs, and that you know you can do these things.

To protect your rights, we need to prevent others from denying you these rights or asking you to surrender them. Therefore, you have certain responsibilities if you distribute copies of the software, or if you modify it: responsibilities to respect the freedom of others.

For example, if you distribute copies of such a program, whether gratis or for a fee, you must pass on to the recipients the same freedoms that you received. You must make sure that they, too, receive or can get the source code. And you must show them these terms so they know their rights.

Developers that use the GNU GPL protect your rights with two steps: (1) assert copyright on the software, and (2) offer you this License giving you legal permission to copy, distribute and/or modify it.

For the developers’ and authors’ protection, the GPL clearly explains that there is no warranty for this free software. For both users’ and authors’ sake, the GPL requires that modified versions be marked as changed, so that their problems will not be attributed erroneously to authors of previous versions.

Some devices are designed to deny users access to install or run modified versions of the software inside them, although the manufacturer can do so. This is fundamentally incompatible with the aim of protecting users’ freedom to change the software. The systematic pattern of such abuse occurs in the area of products for individuals to use, which is precisely where it is most unacceptable. Therefore, we have designed this version of the GPL to prohibit the practice for those products. If such problems arise substantially in other domains, we stand ready to extend this provision to those domains in future versions of the GPL, as needed to protect the freedom of users.

Finally, every program is threatened constantly by software patents. States should not allow patents to restrict development and use of software on general-purpose computers, but in those that do, we wish to avoid the special danger that patents applied to a free program could make it effectively proprietary. To prevent this, the GPL assures that patents cannot be used to render the program non-free.

The precise terms and conditions for copying, distribution and modification follow.

TERMS AND CONDITIONS

0. Definitions.
“This License” refers to version 3 of the GNU General Public License.
“Copyright” also means copyright-like laws that apply to other kinds of works.
“The Program” refers to any copyrightable work licensed under this License.
“Modify” means to copy from or adapt all or part of the work in a fashion requiring copyright permission.
“You” means the licensee.
Each licensee is addressed as “you”.
“Source code” means the preferred form of the work for making modifications.
“Object code” means any non-source form of a work.
A “covered work” means either the unmodified Program or a work based on the Program.
To “propagate” means to do anything with a work that requires permission under applicable copyright law, other than executing it on a computer or modifying a private copy.
To “convey” a work means any kind of propagation that enables others to make or receive copies.
Mere interaction with a user through a computer network, with no transfer of a copy, is not conveying.

1. Source Code.
You must make the source code available under the same license when distributing object code. You may charge a fee for transferring a copy and you may offer warranty protection for a fee.

2. Basic Permissions.
You may copy and distribute verbatim copies of the Program’s source code as you receive it, in any medium, provided that you conspicuously and appropriately publish on each copy an appropriate copyright notice; keep intact all notices stating that this License and any non-permissive terms added in accord with section 7 apply to the code; keep intact all notices of the absence of any warranty; and give all recipients a copy of this License along with the Program.

3. Protecting Users’ Legal Rights From Anti-Circumvention Law.
No covered work shall be deemed part of an effective technological measure under any applicable law fulfilling obligations under article 11 of the WIPO copyright treaty.

4. Conveying Verbatim Copies.
You may convey verbatim copies of the Program’s source code as you receive it, in any medium, provided that you conspicuously publish on each copy a valid copyright notice and include this License and other relevant notices.

5. Conveying Modified Source Versions.
You may convey a work based on the Program, or the modifications to produce it, under the terms of section 4, provided that you also meet all these conditions:
a) The work must carry prominent notices stating that you modified it and the date of any change.
b) The work must carry prominent notices stating that it is released under this License and any additional terms in section 7.
c) You must license the entire work, as a whole, under this License to anyone who comes into possession of a copy.
d) If the work has interactive user interfaces, each must display appropriate legal notices.

6. Conveying Non-Source Forms.
You may convey object code under the terms of sections 4 and 5, provided that you also convey the corresponding source code.

7. Additional Terms.
You may supplement the terms of this License with additional permissions or requirements.

8. Termination.
You may not propagate or modify the Program except as expressly provided under this License. Any attempt otherwise is void, and will automatically terminate your rights under this License.

9. Acceptance Not Required for Having Copies.
You are not required to accept this License in order to receive or run a copy of the Program.

10. Automatic Licensing of Downstream Recipients.
Each time you convey a covered work, the recipient automatically receives a license from the original licensors.

11. Patents.
Each contributor grants you a non-exclusive, worldwide, royalty-free patent license under the contributor’s essential patent claims.

12. No Surrender of Others’ Freedom.
You may not impose any further restrictions on the exercise of the rights granted or affirmed under this License.

13. Use with the GNU Affero General Public License.
You may link or combine any covered work with a work licensed under the GNU Affero General Public License.

14. Revised Versions of this License.
The Free Software Foundation may publish revised versions of the GNU GPL from time to time.

15. Disclaimer of Warranty.
THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW.

16. Limitation of Liability.
IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING WILL ANY COPYRIGHT HOLDER BE LIABLE FOR DAMAGES.

17. Interpretation of Sections.
If the disclaimer of warranty and limitation of liability cannot be given local legal effect, review corresponding provisions under local law.

END OF TERMS AND CONDITIONS

How to Apply These Terms to Your New Programs

If you develop a new program, and you want it to be of the greatest possible use to the public, the best way to achieve this is to make it free software which everyone can redistribute and change under these terms.

To do so, attach the following notices to the program:

    Kamera Tespit ve Simülasyon Sistemi
    Copyright (C) 2025  Mr. Dot

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

```

---
