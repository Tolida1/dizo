import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_dizipal():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # GitHub Actions için şart
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        url = "https://dizipal.bar/"
        driver.get(url)

        # İçeriğin yüklenmesini bekle (max 20 saniye)
        # 'home-content' sınıfının gelmesini bekliyoruz
        wait = WebDriverWait(driver, 20)
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "home-content")))

        # İstediğin bölümün HTML'ini al
        # Not: max-w-[1180px] gibi sınıflar CSS seçici ile özel karakter kaçışı gerektirir
        content = driver.find_element(By.CSS_SELECTOR, "div.max-w-\[1180px\]").get_attribute('outerHTML')

        with open("sonuc.html", "w", encoding="utf-8") as f:
            f.write(content)
        
        print("Veri başarıyla çekildi ve sonuc.html dosyasına kaydedildi.")

    except Exception as e:
        print(f"Hata oluştu: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_dizipal()
