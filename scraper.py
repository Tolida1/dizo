from seleniumbase import SB
import os

def scrape_dizipal():
    # Hedef URL ve User-Agent (Gerçek bir tarayıcı gibi görünmek için)
    target_url = "https://dizipal2026.com/"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

    # uc=True: Undetected Mode'u aktif eder
    with SB(uc=True, headless=True, agent=user_agent) as sb:
        try:
            print(f"Siteye giriş yapılıyor: {target_url}")
            sb.uc_open_with_reconnect(target_url, 6)
            
            # 1. Aşama: Cloudflare/Captcha kontrolü ve tıklama
            sb.sleep(5) # Sayfanın oturması için bekle
            try:
                sb.uc_gui_click_captcha()
                print("Doğrulama kutucuğuna tıklandı.")
            except:
                print("Doğrulama kutucuğu bulunamadı, muhtemelen direkt geçildi.")

            # 2. Aşama: İçeriğin yüklenmesini bekle
            # 'Son Eklenen Diziler' yazısını içeren section'ı bekliyoruz
            print("İçerik yüklenmesi bekleniyor...")
            sb.wait_for_element("section.content-section", timeout=20)
            
            # 3. Aşama: Veriyi çek
            # Birden fazla content-section olabilir, biz başlığı kontrol edelim
            sections = sb.find_elements("section.content-section")
            target_html = ""
            
            for section in sections:
                if "Son Eklenen Diziler" in section.text:
                    target_html = section.get_attribute("outerHTML")
                    break
            
            if target_html:
                with open("sonuc.html", "w", encoding="utf-8") as f:
                    f.write(target_html)
                print("BAŞARILI: 'Son Eklenen Diziler' bölümü kaydedildi.")
            else:
                print("HATA: Belirtilen bölüm bulunamadı.")
                sb.save_screenshot("hata_bulunamadi.png")

        except Exception as e:
            print(f"Bir hata oluştu: {e}")
            sb.save_screenshot("hata_debug.png")
            with open("hata_sayfa_kaynagi.html", "w", encoding="utf-8") as f:
                f.write(sb.get_page_source())

if __name__ == "__main__":
    scrape_dizipal()
