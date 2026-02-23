from seleniumbase import SB
import os

def run_scraper():
    # 'uc=True' Cloudflare bypass modunu açar
    # 'headless=True' GitHub Actions için gereklidir
    with SB(uc=True, headless=True, agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36") as sb:
        try:
            url = "https://dizipal.bar/"
            print(f"Siteye özel mod ile gidiliyor: {url}")
            
            # Cloudflare'i aşmak için 'reconnect' yöntemiyle açıyoruz
            sb.uc_open_with_reconnect(url, 5)
            
            # Eğer hala doğrulama ekranındaysa, captcha kutucuğuna tıklamayı dene
            try:
                sb.uc_gui_click_captcha()
                print("Captcha kutucuğu denendi.")
            except:
                pass

            # Sayfanın tamamen yüklenmesi için 15 saniye bekle
            sb.sleep(15) 
            
            # İçeriğin gelip gelmediğini kontrol et
            if sb.is_element_present('section.mt-4'):
                content = sb.get_html('div.max-w-\[1180px\]')
                with open("sonuc.html", "w", encoding="utf-8") as f:
                    f.write(content)
                print("Başarılı: İçerik alındı.")
            else:
                # Başarısız olursa o anki durumu çek
                print("İçerik bulunamadı, ekran görüntüsü alınıyor...")
                sb.save_screenshot("hata_aninda_ekran.png")
                # Sayfa kaynağını yazdır (hata ayıklama için)
                with open("page_source.txt", "w", encoding="utf-8") as f:
                    f.write(sb.get_page_source())

        except Exception as e:
            print(f"Hata: {e}")
            sb.save_screenshot("debug.png")

if __name__ == "__main__":
    run_scraper()
