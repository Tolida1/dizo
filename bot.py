import cloudscraper
import json
import re

def maclari_cek():
    scraper = cloudscraper.create_scraper()
    
    source_url = "https://patronsports2.cfd/matches.php"
    # m3u8'lerin çözülmesi için gerekebilecek ana domain
    base_domain = "https://patronsports2.cfd"
    
    headers = {
        'Origin': 'https://restmacizle42.cfd',
        'Referer': 'https://restmacizle42.cfd/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    try:
        response = scraper.get(source_url, headers=headers)
        if response.status_code == 200:
            raw_data = response.text.strip()
            if not raw_data.startswith('['):
                raw_data = f"[{raw_data}]"
            
            raw_maclar = json.loads(raw_data)
            
            # Senin istediğin ana yapı
            final_json = {
                "list": {
                    "service": "iptv",
                    "title": "iptv",
                    "item": []
                }
            }

            for mac in raw_maclar:
                # m3u8 linkini oluştur (Eğer ID varsa oluşturur, yoksa boş bırakır)
                # Not: Önceki adımda çözdüğümüz mantığı buraya entegre ediyoruz
                match_id = ""
                if 'URL' in mac:
                    id_match = re.search(r"id=([a-zA-Z0-9_-]+)", mac['URL'])
                    if id_match:
                        match_id = id_match.group(1)
                
                # Örnek m3u8 yapısı (Site dinamik baseurl kullanıyorsa burası gelişebilir)
                # Şimdilik senin verdiğin formata uygun bir placeholder veya çözülmüş link koyuyoruz
                m3u8_link = f"https://restmacizle42.cfd/{match_id}/mono.m3u8" if match_id else ""

                # Yeni item yapısını oluştur
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

            # Dosyaya kaydet
            with open('maclar.json', 'w', encoding='utf-8') as f:
                json.dump(final_json, f, ensure_ascii=False, indent=4)
            
            print("BAŞARILI: JSON istenen hiyerarşik formatta kaydedildi.")
        else:
            print(f"Hata: {response.status_code}")
    except Exception as e:
        print(f"Sistem Hatası: {e}")

if __name__ == "__main__":
    maclari_cek()
