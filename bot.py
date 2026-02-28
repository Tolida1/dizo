import cloudscraper
import json
import re
from bs4 import BeautifulSoup

def m3u8_coz(url, scraper):
    try:
        # Maçın izleme sayfasına gir
        headers = {'Referer': 'https://restmacizle42.cfd/'}
        response = scraper.get(url, headers=headers)
        if response.status_code != 200: return None

        content = response.text
        
        # 1. Adım: Sayfa içindeki ID'yi bul (id=patron gibi)
        match_id = None
        id_search = re.search(r"get\(['\"]id['\"]\);.*?if\(!b\)return null;.*?return currentBaseUrl\+b\+['\"]/mono.m3u8['\"]", content, re.DOTALL)
        # Daha basit bir regex ile URL'den veya CONFIG'den ID çekme:
        id_param = re.search(r"id=([a-zA-Z0-9_-]+)", url)
        if id_param:
            match_id = id_param.group(1)

        # 2. Adım: Base URL'yi domain.php'den çek (Sitedeki CONFIG yapısına göre)
        # Not: Site içindeki domain.php dinamik olduğu için genellikle sabit bir baseurl kullanılır 
        # veya domain.php'ye istek atılır.
        domain_api = "https://patronsports2.cfd/domain.php"
        domain_res = scraper.get(domain_api, headers=headers)
        base_url = ""
        if domain_res.status_code == 200:
            base_url = domain_res.json().get('baseurl', '')

        if base_url and match_id:
            return f"{base_url}{match_id}/mono.m3u8"
            
    except Exception as e:
        print(f"Link çözme hatası: {e}")
    return None

def maclari_cek():
    scraper = cloudscraper.create_scraper()
    source_url = "https://patronsports2.cfd/matches.php"
    target_domain = "https://restmacizle42.cfd"
    
    headers = {
        'Origin': 'https://restmacizle42.cfd',
        'Referer': 'https://restmacizle42.cfd/',
    }

    try:
        response = scraper.get(source_url, headers=headers)
        if response.status_code == 200:
            raw_data = response.text.strip()
            if not raw_data.startswith('['): raw_data = f"[{raw_data}]"
            
            maclar = json.loads(raw_data)
            
            for mac in maclar:
                # Orijinal İzleme Linkini Oluştur
                path = mac['URL'].replace('https://patronsports2.cfd', '')
                if not path.startswith('/'): path = '/' + path
                izle_linki = f"https://restmacizle42.cfd{path}"
                
                # M3U8 Linkini Çöz ve Ekle
                print(f"Çözülüyor: {mac['HomeTeam']}...")
                m3u8_url = m3u8_coz(izle_linki, scraper)
                
                mac['m3u8'] = m3u8_url # Yeni alanı ekle
                mac['URL'] = izle_linki # Normal linki de güncelle

            with open('maclar.json', 'w', encoding='utf-8') as f:
                json.dump(maclar, f, ensure_ascii=False, indent=4)
            
            print("BAŞARILI: M3U8 linkleri dahil edildi.")
            
    except Exception as e:
        print(f"Sistem Hatası: {e}")

if __name__ == "__main__":
    maclari_cek()
