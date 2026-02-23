import random
from seleniumbase import SB

def run_scraper():
    # En yaygın gerçek kullanıcı tarayıcı kimliklerinden biri
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    
    # uc=True: Bot engelini aşma modu
    # headless=True: GitHub Actions için gerekli (Arayüzsüz)
    with SB(uc=True, headless=True, agent=user_agent) as sb:
        try:
            url = "https://dizipal.bar/"
            print(f"Site açılıyor: {url}")
            
            # 1. Adım: Siteye bağlan (Cloudflare algılarsa otomatik yeniden bağlanır)
            sb.uc_open_with_reconnect(url, reconnect_time=6)
            
            # 2. Adım: "İnsan gibi" rastgele bekle (3-7 saniye arası)
            bekleme_suresi = random.uniform(3.5, 7.2)
            print(f"İnsan gibi bekleniyor: {bekleme_suresi:.2f} saniye...")
            sb.sleep(bekleme_suresi)
            
            # 3. Adım: Eğer doğrulama kutucuğu varsa tıkla (En kritik yer)
            print("Doğrulama kutucuğu taranıyor ve tıklanıyor...")
            try:
                sb.uc_gui_click_captcha() 
                print("Kutucuğa tıklandı veya kutucuk geçildi.")
            except Exception as e:
                print("Kutucuk tıklanamadı veya zaten geçildi.")

            # 4. Adım: İçeriğin yüklenmesi için biraz daha bekle
            sb.sleep(10)
            
            # Ekran görüntüsü al (Başarıyı veya engeli görmek için)
            sb.save_screenshot("son_durum.png")
            
            # 5. Adım: Hedef bölümü (section) kontrol et
            if sb.is_element_present('section'):
                print("BAŞARILI: Site içeriğine girildi!")
                # İstediğin div içeriğini al
                try:
                    content = sb.get_html('div.max-w-\[1180px\]')
                    with open("sonuc.html", "w", encoding="utf-8") as f:
                        f.write(content)
                except:
                    # Div bulunamazsa tüm sayfayı al
                    with open("sonuc.html", "w", encoding="utf-8") as f:
                        f.write(sb.get_page_source())
            else:
                print("HATA: Hala doğrulama ekranında takılıyız.")
                with open("hata_sayfasi.html", "w", encoding="utf-8") as f:
                    f.write(sb.get_page_source())

        except Exception as e:
            print(f"Sistem Hatası: {e}")
            sb.save_screenshot("hata_debug.png")

if __name__ == "__main__":
    run_scraper()
