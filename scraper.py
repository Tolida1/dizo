from seleniumbase import SB
import os

def run_scraper():
    # UC (Undetected) modunda ve headless (arayüzsüz) başlatıyoruz
    with SB(uc=True, headless=True) as sb:
        try:
            url = "https://dizipal.bar/"
            print(f"Siteye gidiliyor: {url}")
            sb.open(url)

            # Cloudflare doğrulaması için biraz bekle ve içeriği kontrol et
            sb.sleep(10) 
            
            # Eğer 'home-content' yüklenmezse hata vermemesi için kontrol
            if sb.is_element_present('section.mt-4'):
                # İstediğin bölümün içeriğini al
                content = sb.get_html('div.max-w-\[1180px\]')
                
                with open("sonuc.html", "w", encoding="utf-8") as f:
                    f.write(content)
                print("Başarıyla kaydedildi: sonuc.html")
            else:
                print("Hedef element bulunamadı, muhtemelen Cloudflare engeline takıldı.")
            
            # Her durumda hata ayıklama için ekran görüntüsü al
            sb.save_screenshot("debug.png")

        except Exception as e:
            print(f"Hata oluştu: {e}")
            if not os.path.exists("debug.png"):
                try: sb.save_screenshot("debug.png")
                except: pass

if __name__ == "__main__":
    run_scraper()
