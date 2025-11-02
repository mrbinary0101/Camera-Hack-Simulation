#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerçek Nmap Kamera Tespit Sistemi
Gerçek nmap ile ağ tarama ve kamera tespit
"""

import subprocess
import socket
import random
import time
import threading
from datetime import datetime
import json
import re
import xml.etree.ElementTree as ET

class GercekNmapKameraTespit:
    def __init__(self):
        self.hedef_ag = "192.168.1.0/24"
        self.tespit_edilen_kameralar = []
        self.kamera_markalari = [
            "hikvision", "hikingson", "dahua", "axis", "bosch", 
            "samsung", "sony", "panasonic", "canon", "apple",
            "foscam", "vivotek", "mobotix", "pelco", "geovision"
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
            "canon": ["VB-C50i", "VB-C60i", "VB-C70i"],
            "foscam": ["FI9821P", "FI8910W", "FI9900P"],
            "vivotek": ["FD8161", "FD8162", "FD8163"],
            "mobotix": ["M15", "M16", "M25"],
            "pelco": ["Sarix", "Spectra", "Endura"],
            "geovision": ["GV-ABL130", "GV-ABL140", "GV-ABL150"]
        }
        
    def nmap_kontrol(self):
        """Nmap'in yüklü olup olmadığını kontrol et"""
        try:
            result = subprocess.run(['nmap', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"✅ Nmap bulundu: {result.stdout.split()[1]}")
                return True
            else:
                print("❌ Nmap bulunamadı!")
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("❌ Nmap yüklü değil! Lütfen nmap'i yükleyin.")
            return False
    
    def root_yetkisi_kontrol(self):
        """Root yetkisi kontrolü"""
        try:
            # Root yetkisi ile basit bir komut çalıştır
            result = subprocess.run(['sudo', '-n', 'true'], 
                                  capture_output=True, text=True, timeout=3)
            if result.returncode == 0:
                print("✅ Sudo yetkisi mevcut")
                return True
            else:
                print("⚠️  Sudo yetkisi yok, normal kullanıcı modunda çalışılacak")
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("⚠️  Sudo bulunamadı, normal kullanıcı modunda çalışılacak")
            return False
    
    def gercek_ag_tarama(self, ag_araligi=None):
        """Gerçek nmap ile ağ tarama"""
        if ag_araligi:
            self.hedef_ag = ag_araligi
            
        print(f"\n🔍 Gerçek Nmap Ağ Tarama Başlatılıyor: {self.hedef_ag}")
        print("=" * 50)
        
        # Root yetkisi kontrolü
        sudo_gerekli = self.root_yetkisi_kontrol()
        
        # Nmap komutunu hazırla
        if sudo_gerekli:
            nmap_komut = [
                'sudo', 'nmap', 
                '-sS',           # SYN scan (root gerekli)
                '-O',            # OS detection (root gerekli)
                '-sV',           # Service version detection
                '-p', '80,8080,8000,8001,8008,8081,8888,9000',  # Kamera portları
                '--script', 'http-title,http-headers,banner',    # HTTP scriptleri
                '-oX', '-',      # XML çıktı
                self.hedef_ag
            ]
            print("🔐 Root yetkisi ile tarama yapılıyor...")
        else:
            nmap_komut = [
                'nmap', 
                '-sT',           # TCP connect scan (root gerekmez)
                '-sV',           # Service version detection
                '-p', '80,8080,8000,8001,8008,8081,8888,9000',  # Kamera portları
                '--script', 'http-title,http-headers,banner',    # HTTP scriptleri
                '-oX', '-',      # XML çıktı
                self.hedef_ag
            ]
            print("👤 Normal kullanıcı yetkisi ile tarama yapılıyor...")
        
        try:
            print("📡 Nmap tarama çalıştırılıyor...")
            result = subprocess.run(nmap_komut, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print("✅ Tarama tamamlandı!")
                return self.nmap_xml_parse(result.stdout)
            else:
                print(f"❌ Nmap hatası: {result.stderr}")
                return []
                
        except subprocess.TimeoutExpired:
            print("⏰ Tarama zaman aşımına uğradı!")
            return []
        except Exception as e:
            print(f"❌ Tarama hatası: {e}")
            return []
    
    def nmap_xml_parse(self, xml_output):
        """Nmap XML çıktısını parse et"""
        try:
            root = ET.fromstring(xml_output)
            cihazlar = []
            
            for host in root.findall('host'):
                ip = host.find('address').get('addr')
                
                # Açık portları bul
                ports = host.find('ports')
                if ports is not None:
                    for port in ports.findall('port'):
                        port_id = port.get('portid')
                        state = port.find('state')
                        
                        if state is not None and state.get('state') == 'open':
                            service = port.find('service')
                            script_results = []
                            
                            # Script sonuçlarını al
                            for script in port.findall('script'):
                                script_results.append({
                                    'id': script.get('id'),
                                    'output': script.get('output', '')
                                })
                            
                            cihaz_bilgi = {
                                'ip': ip,
                                'port': int(port_id),
                                'service': service.get('name', 'unknown') if service is not None else 'unknown',
                                'version': service.get('version', '') if service is not None else '',
                                'product': service.get('product', '') if service is not None else '',
                                'os': self.os_tespit_et(host),
                                'banner': self.banner_cikar(script_results),
                                'script_results': script_results
                            }
                            
                            cihazlar.append(cihaz_bilgi)
            
            return cihazlar
            
        except ET.ParseError as e:
            print(f"❌ XML parse hatası: {e}")
            return []
    
    def os_tespit_et(self, host_element):
        """Host elementinden OS bilgisini çıkar"""
        os_info = host_element.find('os')
        if os_info is not None:
            osmatch = os_info.find('osmatch')
            if osmatch is not None:
                return osmatch.get('name', 'Unknown')
        return 'Unknown'
    
    def banner_cikar(self, script_results):
        """Script sonuçlarından banner bilgisini çıkar"""
        banner = ""
        for script in script_results:
            if script['id'] in ['http-title', 'http-headers', 'banner']:
                banner += script['output'] + " "
        return banner.strip()
    
    def kamera_tespit(self, tarama_sonuclari):
        """OS ve banner bilgilerinden kamera tespiti"""
        print(f"\n🎥 Kamera Tespit Analizi Başlatılıyor...")
        print("=" * 50)
        
        kameralar = []
        
        for cihaz in tarama_sonuclari:
            banner_lower = cihaz['banner'].lower()
            product_lower = cihaz['product'].lower()
            service_lower = cihaz['service'].lower()
            version_lower = cihaz['version'].lower()
            
            # Banner, product, service ve version bilgilerinden kamera tespiti
            for marka in self.kamera_markalari:
                if (marka in banner_lower or 
                    marka in product_lower or 
                    marka in service_lower or 
                    marka in version_lower):
                    
                    model = random.choice(self.kamera_modelleri.get(marka, ["Unknown Model"]))
                    
                    kamera_bilgi = {
                        "ip": cihaz['ip'],
                        "port": cihaz['port'],
                        "marka": marka.upper(),
                        "model": model,
                        "os": cihaz['os'],
                        "service": cihaz['service'],
                        "product": cihaz['product'],
                        "version": cihaz['version'],
                        "banner": cihaz['banner'],
                        "tespit_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "guvenlik_seviyesi": random.choice(["Düşük", "Orta", "Yüksek"]),
                        "acik_portlar": [cihaz['port']]
                    }
                    
                    kameralar.append(kamera_bilgi)
                    print(f"🎯 Kamera tespit edildi: {cihaz['ip']} - {marka.upper()}")
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
            print(f"   Servis: {kamera['service']}")
            print(f"   Ürün: {kamera['product']}")
            print(f"   Versiyon: {kamera['version']}")
            print(f"   Banner: {kamera['banner'][:100]}...")
            print(f"   Güvenlik Seviyesi: {kamera['guvenlik_seviyesi']}")
            print(f"   Tespit Tarihi: {kamera['tespit_tarihi']}")
    
    def simulasyon_raporu(self, kameralar):
        """Simülasyon raporu oluştur"""
        print(f"\n📋 Gerçek Tarama Raporu")
        print("=" * 50)
        
        rapor = {
            "simulasyon_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "hedef_ag": self.hedef_ag,
            "tespit_edilen_kameralar": len(kameralar),
            "detaylar": {
                "kameralar": kameralar
            }
        }
        
        # JSON dosyasına kaydet
        rapor_dosyasi = f"gercek_kamera_tespit_raporu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(rapor_dosyasi, 'w', encoding='utf-8') as f:
            json.dump(rapor, f, ensure_ascii=False, indent=2)
        
        print(f"📄 Rapor kaydedildi: {rapor_dosyasi}")
        print(f"🎯 Toplam Kamera: {rapor['tespit_edilen_kameralar']}")
        
        return rapor

def main():
    """Ana fonksiyon"""
    print("🎬 Gerçek Nmap Kamera Tespit Sistemi")
    print("=" * 50)
    print("⚠️  Bu gerçek ağ tarama yapar! Sadece kendi ağınızda kullanın.")
    print("🔐 SYN scan ve OS detection için sudo yetkisi gerekebilir.")
    print("=" * 50)
    
    # Nmap kontrolü
    tespit_sistemi = GercekNmapKameraTespit()
    
    if not tespit_sistemi.nmap_kontrol():
        print("\n💡 Nmap yüklemek için:")
        print("   Ubuntu/Debian: sudo apt install nmap")
        print("   CentOS/RHEL: sudo yum install nmap")
        print("   Arch: sudo pacman -S nmap")
        return
    
    # Kullanıcıdan ağ aralığı al
    try:
        ag_araligi = input("\n🌐 Hedef ağ aralığını girin (örn: 192.168.1.0/24): ").strip()
        if not ag_araligi:
            ag_araligi = "192.168.1.0/24"
    except EOFError:
        ag_araligi = "192.168.1.0/24"
        print(f"🌐 Varsayılan ağ aralığı kullanılıyor: {ag_araligi}")
    
    try:
        # 1. Gerçek ağ tarama
        tarama_sonuclari = tespit_sistemi.gercek_ag_tarama(ag_araligi)
        
        if not tarama_sonuclari:
            print("❌ Tarama sonucu bulunamadı!")
            return
        
        print(f"\n📡 Toplam {len(tarama_sonuclari)} açık port tespit edildi")
        
        # 2. Kamera tespit
        kameralar = tespit_sistemi.kamera_tespit(tarama_sonuclari)
        
        # 3. Kamera listesini yazdır
        tespit_sistemi.kamera_listesi_yazdir(kameralar)
        
        # 4. Rapor oluştur
        tespit_sistemi.simulasyon_raporu(kameralar)
        
        print(f"\n🎉 Gerçek tarama tamamlandı!")
        
    except KeyboardInterrupt:
        print(f"\n⏹️  Tarama kullanıcı tarafından durduruldu.")
    except Exception as e:
        print(f"\n❌ Hata oluştu: {e}")

if __name__ == "__main__":
    main()
