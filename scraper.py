import os
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_dizipal():
    options = uc.ChromeOptions()
    options.add_argument('--headless')  # GitHub'da arayüzsüz çalışmalı
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    try:
        # Sürücüyü başlat
        driver = uc.Chrome(options=options)
        driver.get("https://dizipal.bar/")
        
        print("Sayfa yükleniyor, 10 saniye bekleniyor...")
        time.sleep(10) # Sayfanın oturması için ek süre

        # Hata ayıklama için ekran görüntüsü al (Klasörde 'error.png' olarak gözükür)
        driver.save_screenshot("debug.png")

        # Elementin yüklenmesini bekle
        wait = WebDriverWait(driver, 20)
        # Sadece section'ın varlığını kontrol edelim (daha garanti)
        target_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "section")))
        
        # HTML içeriğini al
        content = driver.page_source
        
        with open("sonuc.html", "w", encoding="utf-8") as f:
            f.write(content)
        
        print("İşlem başarılı! Veri 'sonuc.html' dosyasına yazıldı.")

    except Exception as e:
        print(f"Hata detayı: {e}")
        # Hata anında ekranı çek ki neden bulamadığını görelim
        if 'driver' in locals():
            driver.save_screenshot("hata_aninda_ekran.png")
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    scrape_dizipal()
