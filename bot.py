import cloudscraper
import json
import os

def maclari_cek():
    # Cloudflare engelini aşmak için scraper nesnesi
    scraper = cloudscraper.create_scraper()
    
    # Verinin çekileceği kaynak
    source_url = "https://patronsports2.cfd/matches.php"
    
    # Linklerin dönüştürüleceği hedef domain
    target_domain = "https://restmacizle42.cfd"
    
    headers = {
        'Origin': 'https://restmacizle42.cfd',
        'Referer': 'https://restmacizle42.cfd/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    try:
        response = scraper.get(source_url, headers=headers)
        if response.status_code == 200:
            raw_data = response.text.strip()
            
            if raw_data:
                # Liste formatı kontrolü ve düzeltme (başa [ sona ] ekleme)
                if not raw_data.startswith('['):
                    raw_data = f"[{raw_data}]"
                
                try:
                    maclar = json.loads(raw_data)
                    
                    # URL'leri senin istediğin domaine çevirme döngüsü
                    for mac in maclar:
                        if 'URL' in mac:
                            # Önce var olan domain kısmını temizle (eğer varsa) sadece path kalsın
                            path = mac['URL'].replace('https://patronsports2.cfd', '')
                            # Başına senin domainini ekle
                            if not path.startswith('/'):
                                path = '/' + path
                            
                            mac['URL'] = f"{target_domain}{path}"
                    
                    # JSON dosyasını liste olarak kaydet
                    with open('maclar.json', 'w', encoding='utf-8') as f:
                        json.dump(maclar, f, ensure_ascii=False, indent=4)
                    
                    print(f"BAŞARILI: Linkler {target_domain} olarak güncellendi.")
                except json.JSONDecodeError:
                    print("HATA: Gelen veri JSON formatına uygun değil.")
            else:
                print("UYARI: Kaynaktan veri gelmedi.")
        else:
            print(f"HATA: Sunucu hata kodu verdi: {response.status_code}")
            
    except Exception as e:
        print(f"Sistem Hatası: {e}")

if __name__ == "__main__":
    maclari_cek()
