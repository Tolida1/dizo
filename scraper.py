from seleniumbase import SB
import os

def run_scraper():
    # En güncel User-Agent'ı manuel ekleyelim
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    
    with SB(uc=True, headless=True, agent=user_agent) as sb:
        try:
            url = "https://dizipal.bar/"
            print(f"Hedef: {url}")
            
            # 1. Adım: Reconnect ile aç (Cloudflare'i şaşırtır)
            sb.uc_open_with_reconnect(url, 6)
            
            # 2. Adım: Captcha varsa tıkla
            try:
                sb.uc_gui_click_captcha()
            except:
                pass
            
            # 3. Adım: Sayfanın tam oturması için bekle
            sb.sleep(20) 
            
            # Her ihtimale karşı ekranı çek (Artifact için ismini sabitliyoruz)
            sb.save_screenshot("debug.png")

            # 4. Adım: İçeriği kontrol et
            if sb.is_element_present('section'):
                # Sınıf ismi karmaşık olduğu için tag üzerinden alıyoruz
                content = sb.get_html('section.mt-4')
                with open("sonuc.html", "w", encoding="utf-8") as f:
                    f.write(content)
                print("BAŞARILI: Veri alındı.")
            else:
                print("BAŞARISIZ: İçerik hala yüklenmedi.")
                # Sayfa kaynağını da kaydedelim ki nedenini görelim
                with open("page_source.html", "w", encoding="utf-8") as f:
                    f.write(sb.get_page_source())

        except Exception as e:
            print(f"Hata: {e}")
            if not os.path.exists("debug.png"):
                sb.save_screenshot("debug.png")

if __name__ == "__main__":
    run_scraper()
