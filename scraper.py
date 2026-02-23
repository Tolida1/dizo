import requests

BASE_URL = "https://direniyoruz77.store/palx/"
TARGET_API = "https://tivorlisusan.site/1/receiver.php"
SECRET_KEY = "ozel_anahtar_123"

def process(path, label):
    headers = {
        'User-Agent': 'Android Vinebre Software',
        'X-Requested-With': 'com.bynetvgoldv10'
    }
    try:
        r = requests.get(BASE_URL + path, headers=headers)
        if r.status_code == 200:
            requests.post(TARGET_API, data={
                'key': SECRET_KEY,
                'path': label,
                'html': r.text
            })
            print(f"{label} başarıyla işlendi.")
    except:
        pass

# Kategorileri sırayla gönder
process("", "index")
process("Movies/?v=aHR0cHM6Ly9kaXppcGFsLmJhci9maWxtbGVy&all=true", "Movies")
process("Series/?v=aHR0cHM6Ly9kaXppcGFsLmJhci9kaXppbGVy", "Series")
