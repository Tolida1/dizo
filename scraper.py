import requests
import json
import os

# Ayarlar
BASE_URL = "https://direniyoruz77.store/palx/"
TARGET_API = "https://tivorlisusan.site/1/receiver.php" # Veriyi göndereceğimiz adres
SECRET_KEY = "ozel_anahtar_123" # Güvenlik için

headers = {
    'User-Agent': 'Android Vinebre Software',
    'X-Requested-With': 'com.bynetvgoldv10',
    'Referer': 'https://direniyoruz77.store/palx/'
}

def fetch_data(path=""):
    try:
        response = requests.get(BASE_URL + path, headers=headers, timeout=15)
        if response.status_code == 200:
            return response.text
        return None
    except Exception as e:
        print(f"Hata: {e}")
        return None

def main():
    # Ana sayfayı çek
    content = fetch_data()
    if content:
        # Burada istersen BeautifulSoup ile veriyi parçalayabilir (parse) 
        # veya ham HTML olarak gönderebilirsin.
        payload = {
            'key': SECRET_KEY,
            'path': 'home',
            'html': content
        }
        # Kendi sitene gönder
        requests.post(TARGET_API, data=payload)
        print("Veri başarıyla gönderildi.")

if __name__ == "__main__":
    main()
