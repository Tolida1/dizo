import cloudscraper
import json
import os

def maclari_cek():
    scraper = cloudscraper.create_scraper()
    
    # Hedef API ve Ana Domain
    url = "https://patronsports2.cfd/matches.php"
    base_domain = "https://patronsports2.cfd"
    
    headers = {
        'Origin': 'https://restmacizle42.cfd',
        'Referer': 'https://restmacizle42.cfd/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    try:
        response = scraper.get(url, headers=headers)
        if response.status_code == 200:
            raw_data = response.text.strip()
            
            if raw_data:
                # Liste formatı kontrolü ve düzeltme
                if not raw_data.startswith('['):
                    raw_data = f"[{raw_data}]"
                
                try:
                    maclar = json.loads(raw_data)
                    
                    # URL'leri tam bağlantıya dönüştürme döngüsü
                    for mac in maclar:
                        if 'URL' in mac and mac['URL'].startswith('/'):
                            # "/ch.html?id=..." kısmını tam link yapar
                            mac['URL'] = f"{base_domain}{mac['URL']}"
                    
                    # JSON dosyasını kaydet
                    with open('maclar.json', 'w', encoding='utf-8') as f:
                        json.dump(maclar, f, ensure_ascii=False, indent=4)
                    
                    print("BAŞARILI: Veriler tam URL formatında listeye kaydedildi.")
                except json.JSONDecodeError:
                    print("HATA: JSON ayrıştırma hatası.")
            else:
                print("UYARI: Kaynak veri boş.")
        else:
            print(f"HATA: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"Sistem Hatası: {e}")

if __name__ == "__main__":
    maclari_cek()
