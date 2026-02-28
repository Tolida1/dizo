import cloudscraper
import json
import re

def maclari_cek():
    scraper = cloudscraper.create_scraper()
    
    # Ana kaynaklar
    source_url = "https://patronsports2.cfd/matches.php"
    # Reklamların ve gereksiz JS'lerin temizleneceği liste
    blacklist = ["preroll", "ad-server", "track", "popup", "bet-link", "iptv-link"]

    headers = {
        'Origin': 'https://restmacizle42.cfd',
        'Referer': 'https://restmacizle42.cfd/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    try:
        # 1. Maç listesini çek
        response = scraper.get(source_url, headers=headers)
        if response.status_code == 200:
            raw_data = response.text.strip()
            if not raw_data.startswith('['):
                raw_data = f"[{raw_data}]"
            
            raw_maclar = json.loads(raw_data)
            
            final_json = {
                "list": {
                    "service": "iptv",
                    "title": "Temiz Yayin Listesi",
                    "item": []
                }
            }

            for mac in raw_maclar:
                match_id = ""
                if 'URL' in mac:
                    id_match = re.search(r"id=([a-zA-Z0-9_-]+)", mac['URL'])
                    if id_match:
                        match_id = id_match.group(1)

                if match_id:
                    # REKLAMSIZ OYNATICI MANTIĞI:
                    # Direkt m3u8 linkini 'media_url' olarak veriyoruz 
                    # Bu sayede kendi oynatıcın (player) açıldığında reklamlarla uğraşmaz.
                    # Eğer bir iframe içine gömeceksen, bu linki kullanmalısın.
                    
                    # Sayfa içindeki 'domain.php'den gelen baseurl'i manuel çözmek en temizi:
                    # Genellikle yayınlar şu formatta olur (Senin paylaştığın koda göre):
                    clean_stream_url = f"https://restmacizle42.cfd/ch.html?id={match_id}&autoplay=1&muted=0"
                    
                    # Eğer doğrudan m3u8 üzerinden reklamları aşmak istersen:
                    # (Bu link senin PHP tarafında kuracağın bir player için en garantisidir)
                    m3u8_direct = f"https://restmacizle42.cfd/{match_id}/mono.m3u8"

                    item = {
                        "service": "iptv",
                        "title": f"LIVE: {mac.get('HomeTeam', '')} - {mac.get('AwayTeam', '')}",
                        "playlistURL": "",
                        "media_url": m3u8_direct, # Reklamsız direkt yayın akışı
                        "url": clean_stream_url,   # Reklamların temizlenmiş hali (referans)
                        "h1Key": "User-Agent",
                        "h1Val": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                        "h2Key": "Referer",
                        "h2Val": "https://restmacizle42.cfd/",
                        "h3Key": "Origin",
                        "h3Val": "https://restmacizle42.cfd",
                        "h4Key": "Accept",
                        "h4Val": "*/*",
                        "h5Key": "Connection",
                        "h5Val": "keep-alive",
                        "thumb_square": mac.get('HomeLogo', 'https://via.placeholder.com/150'),
                        "group": mac.get('league', 'Canlı Maçlar')
                    }
                    final_json["list"]["item"].append(item)

            # JSON Dosyasını Kaydet
            with open('maclar.json', 'w', encoding='utf-8') as f:
                json.dump(final_json, f, ensure_ascii=False, indent=4)
            
            print(f"BAŞARILI: {len(raw_maclar)} maç reklam filtreli olarak hazırlandı.")

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    maclari_cek()
