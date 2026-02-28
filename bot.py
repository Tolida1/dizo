import cloudscraper
import json
import re

def maclari_cek():
    scraper = cloudscraper.create_scraper()
    
    # Kaynak adresler
    source_url = "https://patronsports2.cfd/matches.php"
    domain_api = "https://patronsports2.cfd/domain.php"
    
    headers = {
        'Origin': 'https://restmacizle42.cfd',
        'Referer': 'https://restmacizle42.cfd/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    try:
        # 1. ADIM: Yayın sunucusunu (BaseURL) çek
        base_url = "https://restmacizle42.cfd/" 
        domain_res = scraper.get(domain_api, headers=headers)
        if domain_res.status_code == 200:
            base_url = domain_res.json().get('baseurl', base_url)
        
        if not base_url.endswith('/'):
            base_url += '/'

        # 2. ADIM: Maç listesini çek
        response = scraper.get(source_url, headers=headers)
        if response.status_code == 200:
            raw_data = response.text.strip()
            if not raw_data.startswith('['):
                raw_data = f"[{raw_data}]"
            
            raw_maclar = json.loads(raw_data)
            
            final_json = {
                "list": {
                    "service": "iptv",
                    "title": "Reklamsız Yayınlar",
                    "item": []
                }
            }

            for mac in raw_maclar:
                match_id = ""
                if 'URL' in mac:
                    # ID'yi çek (Örn: b2)
                    id_match = re.search(r"id=([a-zA-Z0-9_-]+)", mac['URL'])
                    if id_match:
                        match_id = id_match.group(1)

                if match_id:
                    # REKLAM ENGELLEME STRATEJİSİ:
                    # Site ch.html içinde 'prerollVideo' oynatıyor. 
                    # Biz o sayfayı hiç çağırmıyoruz, doğrudan sunucudaki .m3u8 dosyasına gidiyoruz.
                    # Bu sayede ne reklam çıkar ne de 'Reklamı Geç' butonu bekletir.
                    
                    m3u8_link = f"{base_url}{match_id}/mono.m3u8"

                    item = {
                        "service": "iptv",
                        "title": f"{mac.get('HomeTeam', 'Maç')} - {mac.get('AwayTeam', '')}",
                        "playlistURL": "",
                        "media_url": m3u8_link,
                        "url": m3u8_link, # Artık URL de doğrudan m3u8, reklamlı sayfa değil!
                        "h1Key": "User-Agent",
                        "h1Val": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                        "h2Key": "Referer",
                        "h2Val": "https://restmacizle42.cfd/", # Bu referer olmazsa yayın açılmaz
                        "h3Key": "Origin",
                        "h3Val": "https://restmacizle42.cfd",
                        "h4Key": "0",
                        "h5Key": "0",
                        "thumb_square": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj5nfCOsK9y3unVOT0SrM0fDpKVP4q_Baa_oT1ceUiMik6VRzVl4PNYuyMvmTJL2laGuaVRaR5rNV9sbUSjhKZTdI0Cbi-BRn5JWnHR9Z2PIioNsveAaVNpDPlQIvAGedbWrT_1tIuss64Rk21PQL9_7SAGI6_Bd9zYDlpbYjdXsbgDU3VbTIeCaW39Vgk/s1600/mac_canli.png",
                        "group": mac.get('Time', 'Canlı')
                    }
                    final_json["list"]["item"].append(item)

            with open('maclar.json', 'w', encoding='utf-8') as f:
                json.dump(final_json, f, ensure_ascii=False, indent=4)
            
            print("BAŞARILI: Reklamlı sayfalar bypass edildi, direkt m3u8 linkleri hazır.")

    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    maclari_cek()
