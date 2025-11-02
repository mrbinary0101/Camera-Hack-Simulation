#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kamera Tespit ve Simülasyon Sistemi
Nmap ile ağ tarama ve kamera tespit simülasyonu
"""

import subprocess
import socket
import random
import time
import threading
from datetime import datetime
import json

class KameraSimulasyon:
    def __init__(self):
        self.hedef_ag = "192.168.1.0/24"  # Varsayılan ağ aralığı
        self.tespit_edilen_kameralar = []
        self.kamera_markalari = [
            "hikvision", "hikingson", "dahua", "axis", "bosch", 
            "samsung", "sony", "panasonic", "canon", "apple"
        ]
        self.kamera_modelleri = {
            "hikvision": ["DS-2CD2xxx", "DS-7604NI", "DS-7732NI"],
            "hikingson": ["HS-IP-2000", "HS-IP-3000", "HS-IP-4000"],
            "dahua": ["IPC-HFW4431R", "NVR4104", "DHI-NVR2104"],
            "axis": ["M3004", "P1365", "Q1615"],
            "apple": ["HomeKit Camera", "iSight Pro", "FaceTime HD"],
            "samsung": ["SNV-6013", "SNV-6014", "SNV-6015"],
            "sony": ["SNC-VB600", "SNC-VB630", "SNC-VB635"],
            "bosch": ["FLEXIDOME", "AUTODOME", "MIC"],
            "panasonic": ["WV-SP102", "WV-SP103", "WV-SP104"],
            "canon": ["VB-C50i", "VB-C60i", "VB-C70i"]
        }
        
    def ag_tarama_simulasyonu(self, ag_araligi=None):
        """Nmap ile ağ tarama simülasyonu"""
        if ag_araligi:
            self.hedef_ag = ag_araligi
            
        print(f"\n🔍 Ağ Tarama Başlatılıyor: {self.hedef_ag}")
        print("=" * 50)
        
        # Simüle edilmiş nmap çıktısı
        simulasyon_cihazlar = [
            {"ip": "192.168.1.1", "port": 80, "service": "http", "os": "Linux", "banner": "Apache/2.4.41"},
            {"ip": "192.168.1.10", "port": 80, "service": "http", "os": "Linux", "banner": "Hikvision Web Server"},
            {"ip": "192.168.1.15", "port": 80, "service": "http", "os": "Linux", "banner": "Hikingson Camera System"},
            {"ip": "192.168.1.20", "port": 80, "service": "http", "os": "Linux", "banner": "Dahua NVR"},
            {"ip": "192.168.1.25", "port": 80, "service": "http", "os": "Linux", "banner": "Axis Camera"},
            {"ip": "192.168.1.30", "port": 80, "service": "http", "os": "macOS", "banner": "Apple HomeKit"},
            {"ip": "192.168.1.35", "port": 80, "service": "http", "os": "Linux", "banner": "Samsung IP Camera"},
            {"ip": "192.168.1.40", "port": 80, "service": "http", "os": "Linux", "banner": "Sony Network Camera"},
            {"ip": "192.168.1.45", "port": 80, "service": "http", "os": "Linux", "banner": "Bosch Security"},
            {"ip": "192.168.1.50", "port": 80, "service": "http", "os": "Linux", "banner": "Panasonic IP Camera"},
            {"ip": "192.168.1.55", "port": 80, "service": "http", "os": "Linux", "banner": "Canon Network Camera"},
            {"ip": "192.168.1.100", "port": 22, "service": "ssh", "os": "Linux", "banner": "OpenSSH 8.2"},
            {"ip": "192.168.1.101", "port": 23, "service": "telnet", "os": "Linux", "banner": "BusyBox telnetd"},
        ]
        
        print("📡 Tarama sonuçları:")
        for cihaz in simulasyon_cihazlar:
            time.sleep(0.1)  # Gerçekçi tarama efekti
            print(f"   {cihaz['ip']}:{cihaz['port']} - {cihaz['service']} - {cihaz['os']} - {cihaz['banner']}")
            
        return simulasyon_cihazlar
    
    def kamera_tespit(self, tarama_sonuclari):
        """OS ve banner bilgilerinden kamera tespiti"""
        print(f"\n🎥 Kamera Tespit Analizi Başlatılıyor...")
        print("=" * 50)
        
        kameralar = []
        
        for cihaz in tarama_sonuclari:
            banner_lower = cihaz['banner'].lower()
            os_lower = cihaz['os'].lower()
            
            # Banner ve OS bilgilerinden kamera tespiti
            for marka in self.kamera_markalari:
                if marka in banner_lower or marka in os_lower:
                    model = random.choice(self.kamera_modelleri.get(marka, ["Unknown Model"]))
                    
                    kamera_bilgi = {
                        "ip": cihaz['ip'],
                        "port": cihaz['port'],
                        "marka": marka.upper(),
                        "model": model,
                        "os": cihaz['os'],
                        "banner": cihaz['banner'],
                        "tespit_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "guvenlik_seviyesi": random.choice(["Düşük", "Orta", "Yüksek"]),
                        "acik_portlar": [cihaz['port'], random.randint(8000, 9000)]
                    }
                    
                    kameralar.append(kamera_bilgi)
                    break
        
        self.tespit_edilen_kameralar = kameralar
        return kameralar
    
    def kamera_listesi_yazdir(self, kameralar):
        """Tespit edilen kameraları ekrana yazdır"""
        if not kameralar:
            print("❌ Hiç kamera tespit edilmedi!")
            return
            
        print(f"\n📹 Tespit Edilen Kameralar ({len(kameralar)} adet):")
        print("=" * 60)
        
        for i, kamera in enumerate(kameralar, 1):
            print(f"\n🎯 Kamera #{i}")
            print(f"   IP Adresi: {kamera['ip']}")
            print(f"   Port: {kamera['port']}")
            print(f"   Marka: {kamera['marka']}")
            print(f"   Model: {kamera['model']}")
            print(f"   İşletim Sistemi: {kamera['os']}")
            print(f"   Banner: {kamera['banner']}")
            print(f"   Güvenlik Seviyesi: {kamera['guvenlik_seviyesi']}")
            print(f"   Açık Portlar: {', '.join(map(str, kamera['acik_portlar']))}")
            print(f"   Tespit Tarihi: {kamera['tespit_tarihi']}")
    
    def sahte_exploit_simulasyonu(self, kameralar):
        """Sahte exploit simülasyonu"""
        if not kameralar:
            print("❌ Exploit edilecek kamera bulunamadı!")
            return
            
        print(f"\n💥 Exploit Simülasyonu Başlatılıyor...")
        print("=" * 50)
        
        exploit_sonuclari = []
        
        for kamera in kameralar:
            print(f"\n🎯 Hedef: {kamera['ip']} ({kamera['marka']} {kamera['model']})")
            
            # Sahte exploit adımları
            exploit_adimlari = [
                "Port tarama yapılıyor...",
                "Servis versiyonu tespit ediliyor...",
                "Zafiyet analizi yapılıyor...",
                "Exploit payload hazırlanıyor...",
                "Bağlantı kuruluyor...",
                "Komut çalıştırılıyor...",
                "Shell erişimi sağlanıyor..."
            ]
            
            for adim in exploit_adimlari:
                time.sleep(0.5)
                print(f"   ⚡ {adim}")
            
            # Sahte başarı durumu
            basari_orani = random.randint(60, 95)
            if basari_orani > 70:
                durum = "✅ BAŞARILI"
                shell_tipi = random.choice(["root", "admin", "user"])
                print(f"   {durum} - Shell erişimi: {shell_tipi}")
                
                exploit_sonuc = {
                    "ip": kamera['ip'],
                    "marka": kamera['marka'],
                    "model": kamera['model'],
                    "durum": "BAŞARILI",
                    "shell_tipi": shell_tipi,
                    "exploit_zamani": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "saglanan_erisim": [
                        "Kamera görüntüsüne erişim",
                        "Sistem konfigürasyonu",
                        "Kullanıcı hesapları",
                        "Ağ ayarları"
                    ]
                }
            else:
                durum = "❌ BAŞARISIZ"
                print(f"   {durum} - Güvenlik önlemleri aktif")
                
                exploit_sonuc = {
                    "ip": kamera['ip'],
                    "marka": kamera['marka'],
                    "model": kamera['model'],
                    "durum": "BAŞARISIZ",
                    "neden": "Güvenlik önlemleri aktif",
                    "exploit_zamani": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            
            exploit_sonuclari.append(exploit_sonuc)
        
        return exploit_sonuclari
    
    def exploit_sonuclari_yazdir(self, sonuclar):
        """Exploit sonuçlarını yazdır"""
        print(f"\n📊 Exploit Sonuçları:")
        print("=" * 50)
        
        basarili = [s for s in sonuclar if s['durum'] == 'BAŞARILI']
        basarisiz = [s for s in sonuclar if s['durum'] == 'BAŞARISIZ']
        
        print(f"✅ Başarılı: {len(basarili)}")
        print(f"❌ Başarısız: {len(basarisiz)}")
        print(f"📈 Başarı Oranı: {len(basarili)/len(sonuclar)*100:.1f}%")
        
        if basarili:
            print(f"\n🎯 Başarılı Exploitler:")
            for sonuc in basarili:
                print(f"   • {sonuc['ip']} ({sonuc['marka']}) - Shell: {sonuc['shell_tipi']}")
                print(f"     Erişim: {', '.join(sonuc['saglanan_erisim'])}")
    
    def simulasyon_raporu(self, kameralar, exploit_sonuclari):
        """Simülasyon raporu oluştur"""
        print(f"\n📋 Simülasyon Raporu")
        print("=" * 50)
        
        rapor = {
            "simulasyon_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "hedef_ag": self.hedef_ag,
            "tespit_edilen_kameralar": len(kameralar),
            "exploit_edilen_kameralar": len([s for s in exploit_sonuclari if s['durum'] == 'BAŞARILI']),
            "detaylar": {
                "kameralar": kameralar,
                "exploit_sonuclari": exploit_sonuclari
            }
        }
        
        # JSON dosyasına kaydet
        rapor_dosyasi = f"kamera_simulasyon_raporu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(rapor_dosyasi, 'w', encoding='utf-8') as f:
            json.dump(rapor, f, ensure_ascii=False, indent=2)
        
        print(f"📄 Rapor kaydedildi: {rapor_dosyasi}")
        print(f"🎯 Toplam Kamera: {rapor['tespit_edilen_kameralar']}")
        print(f"💥 Başarılı Exploit: {rapor['exploit_edilen_kameralar']}")
        
        return rapor

def main():
    """Ana simülasyon fonksiyonu"""
    print("🎬 Kamera Tespit ve Exploit Simülasyonu")
    print("=" * 50)
    print("⚠️  Bu bir simülasyondur! Gerçek sistemlere zarar vermez.")
    print("=" * 50)
    
    # Kullanıcıdan ağ aralığı al
    try:
        ag_araligi = input("\n🌐 Hedef ağ aralığını girin (örn: 192.168.1.0/24): ").strip()
        if not ag_araligi:
            ag_araligi = "192.168.1.0/24"
    except EOFError:
        ag_araligi = "192.168.1.0/24"
        print(f"🌐 Varsayılan ağ aralığı kullanılıyor: {ag_araligi}")
    
    # Simülasyon nesnesini oluştur
    simulasyon = KameraSimulasyon()
    
    try:
        # 1. Ağ tarama
        tarama_sonuclari = simulasyon.ag_tarama_simulasyonu(ag_araligi)
        
        # 2. Kamera tespit
        kameralar = simulasyon.kamera_tespit(tarama_sonuclari)
        
        # 3. Kamera listesini yazdır
        simulasyon.kamera_listesi_yazdir(kameralar)
        
        if kameralar:
            # 4. Exploit simülasyonu
            try:
                input("\n⏸️  Exploit simülasyonunu başlatmak için Enter'a basın...")
            except EOFError:
                print("\n⏸️  Exploit simülasyonu otomatik başlatılıyor...")
                time.sleep(2)
            exploit_sonuclari = simulasyon.sahte_exploit_simulasyonu(kameralar)
            
            # 5. Exploit sonuçlarını yazdır
            simulasyon.exploit_sonuclari_yazdir(exploit_sonuclari)
            
            # 6. Rapor oluştur
            simulasyon.simulasyon_raporu(kameralar, exploit_sonuclari)
        
        print(f"\n🎉 Simülasyon tamamlandı!")
        
    except KeyboardInterrupt:
        print(f"\n⏹️  Simülasyon kullanıcı tarafından durduruldu.")
    except Exception as e:
        print(f"\n❌ Hata oluştu: {e}")

if __name__ == "__main__":
    main()
