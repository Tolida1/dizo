import cloudscraper
import json
import os

def maclari_cek():
    # Cloudflare engelini aşmak için scraper oluştur
    scraper = cloudscraper.create_scraper()
    
    url = "https://patronsports2.cfd/matches.php"
    headers = {
        'Origin': 'https://restmacizle42.cfd',
        'Referer': 'https://restmacizle42.cfd/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    try:
        response = scraper.get(url, headers=headers)
        if response.status_code == 200:
            raw_data = response.text.strip()
            
            # Eğer veri boş değilse işle
            if raw_data:
                # KRİTİK: Veri [ ile başlamıyorsa liste formatına getir
                if not raw_data.startswith('['):
                    # Eğer objeler arasında virgül yoksa veya hatalıysa düzeltme denenebilir
                    # Ama genellikle {...},{...} şeklinde gelir, başına [ sonuna ] eklemek yeterlidir
                    raw_data = f"[{raw_data}]"
                
                # JSON geçerli mi diye kontrol et
                try:
                    json_test = json.loads(raw_data)
                    
                    # Dosyayı temiz bir liste olarak kaydet
                    with open('maclar.json', 'w', encoding='utf-8') as f:
                        json.dump(json_test, f, ensure_ascii=False, indent=4)
                    
                    print("BAŞARILI: maclar.json liste formatında güncellendi.")
                except json.JSONDecodeError:
                    print("HATA: Gelen veri geçerli bir JSON formatına dönüştürülemedi.")
            else:
                print("UYARI: Kaynaktan boş veri döndü.")
        else:
            print(f"HATA: Sunucu {response.status_code} kodunu döndürdü.")
            
    except Exception as e:
        print(f"Sistem Hatası: {e}")

if __name__ == "__main__":
    maclari_cek()
