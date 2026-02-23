from seleniumbase import SB
import os

def scrape_dizipal_detay():
    # Yeni hedef URL
    url = "https://dizipal2026.com/dizi/all-her-fault"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

    with SB(uc=True, headless=True, agent=user_agent) as sb:
        try:
            print(f"Dizi sayfasına gidiliyor: {url}")
            sb.uc_open_with_reconnect(url, 7)
            
            # Cloudflare bypass denemesi
            sb.sleep(5)
            try:
                sb.uc_gui_click_captcha()
            except:
                pass

            # 1. Aşama: Bölümler sekmesinin (tab-episodes) yüklenmesini bekle
            print("Bölüm listesi bekleniyor...")
            sb.wait_for_element("#tab-episodes", timeout=25)
            
            # 2. Aşama: Sezon butonlarını kontrol et ve aktif olanı doğrula
            if sb.is_element_present(".season-btn"):
                print("Sezon butonları bulundu.")
            
            # 3. Aşama: İstediğin div içeriğini (tab-episodes) çek
            # Bu alan tüm sezon ve bölüm listesini içerir
            content = sb.get_html("#tab-episodes")
            
            with open("bolumler.html", "w", encoding="utf-8") as f:
                f.write(content)
            
            print("BAŞARILI: Bölüm ve sezon verileri 'bolumler.html' dosyasına kaydedildi.")
            sb.save_screenshot("sayfa_son_hali.png")

        except Exception as e:
            print(f"Hata detayı: {e}")
            sb.save_screenshot("hata_detay.png")
            with open("hata_kaynak.html", "w", encoding="utf-8") as f:
                f.write(sb.get_page_source())

if __name__ == "__main__":
    scrape_dizipal_detay()
