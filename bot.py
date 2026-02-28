import cloudscraper
import json
import os

def maclari_cek():
    scraper = cloudscraper.create_scraper()
    url = "https://patronsports2.cfd/matches.php"
    headers = {
        'Origin': 'https://restmacizle42.cfd',
        'Referer': 'https://restmacizle42.cfd/'
    }

    try:
        response = scraper.get(url, headers=headers)
        if response.status_code == 200:
            raw_data = response.text.strip()
            # JSON formatını düzelt
            if not raw_data.startswith('['):
                raw_data = f"[{raw_data}]"
            
            # Veriyi dosyaya kaydet (PHP siten bu dosyayı okuyabilir)
            with open('maclar.json', 'w', encoding='utf-8') as f:
                f.write(raw_data)
            print("Veri başarıyla güncellendi: maclar.json")
        else:
            print(f"Hata: {response.status_code}")
    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    maclari_cek()
