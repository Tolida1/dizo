import cloudscraper
import json
import re

def maclari_cek():
    scraper = cloudscraper.create_scraper()
    
    # Veri kaynakları
    source_url = "https://patronsports2.cfd/matches.php"
    domain_api = "https://patronsports2.cfd/domain.php"
    
    headers = {
        'Origin': 'https://restmacizle42.cfd',
        'Referer': 'https://restmacizle42.cfd/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    try:
        # 1. ADIM: Gerçek Yayın Sunucusunu (BaseURL) Al
        base_url = "https://restmacizle42.cfd/" 
        try:
            domain_res = scraper.get(domain_api, headers=headers, timeout=10)
            if domain_res.status_code == 200:
                base_url = domain_res.json().get('baseurl', base_url)
        except:
            print("Domain API alınamadı, varsayılan kullanılıyor.")

        # URL sonunda / olduğundan emin olalım
        if not base_url.endswith('/'):
            base_url += '/'

        # 2. ADIM: Maç Listesini Al
        response = scraper.get(source_url, headers=headers)
        if response.status_code == 200:
            raw_data = response.text.strip()
            if not raw_data.startswith('['):
                raw_data = f"[{raw_data}]"
            
            raw_maclar = json.loads(raw_data)
            
            final_json = {
                "list": {
                    "service": "iptv",
                    "title": "iptv",
                    "item": []
                }
            }

            for mac in raw_maclar:
                # ID Ayıklama (Örn: b2, patron)
                match_id = ""
                if 'URL' in mac:
                    id_match = re.search(r"id=([a-zA-Z0-9_-]+)", mac['URL'])
                    if id_match:
                        match_id = id_match.group(1)
                
                # 3. ADIM: M3U8 Linkini Oluştur (Klasörsüz Direkt Format)
                # SONUÇ: https://domain.com/b2.m3u8
                if match_id:
                    m3u8_link = f"{base_url}{match_id}.m3u8"
                else:
                    m3u8_link = ""

                # JSON Item Yapısı
                item = {
                    "service": "iptv",
                    "title": f"{mac.get('HomeTeam', '')} - {mac.get('AwayTeam', '')}",
                    "playlistURL": "",
                    "media_url": m3u8_link,
                    "url": m3u8_link,
                    "h1Key": "accept",
                    "h1Val": "*/*",
                    "h2Key": "referer",
                    "h2Val": "https://restmacizle42.cfd/",
                    "h3Key": "origin",
                    "h3Val": "https://restmacizle42.cfd",
                    "h4Key": "0",
                    "h4Val": "0",
                    "h5Key": "0",
                    "h5Val": "0",
                    "thumb_square": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj5nfCOsK9y3unVOT0SrM0fDpKVP4q_Baa_oT1ceUiMik6VRzVl4PNYuyMvmTJL2laGuaVRaR5rNV9sbUSjhKZTdI0Cbi-BRn5JWnHR9Z2PIioNsveAaVNpDPlQIvAGedbWrT_1tIuss64Rk21PQL9_7SAGI6_Bd9zYDlpbYjdXsbgDU3VbTIeCaW39Vgk/s1600/mac_canli.png",
                    "group": mac.get('Time', '00:00')
                }
                
                final_json["list"]["item"].append(item)

            # 4. ADIM: Dosyayı Kaydet
            with open('maclar.json', 'w', encoding='utf-8') as f:
                json.dump(final_json, f, ensure_ascii=False, indent=4)
            
            print(f"BAŞARILI: {len(raw_maclar)} maç tekil klasör formatıyla kaydedildi.")
            
    except Exception as e:
        print(f"Sistem Hatası: {e}")

if __name__ == "__main__":
    maclari_cek()
