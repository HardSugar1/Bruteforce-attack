import pyautogui
import time
import random
import os
import pyperclip

# --- AYARLAR ---
pyautogui.FAILSAFE = True
BEKLEME_SURESI = 5          # Her denemeden sonra beklenecek süre (Saniye)
RAKAM_KARISTIRMA_SAYISI = 2 # Her varyasyon için kaç kere rakamları karıştırıp deneyelim?

def dosya_oku(dosya_adi):
    if not os.path.exists(dosya_adi):
        print(f"HATA: '{dosya_adi}' bulunamadı! Lütfen dosyanın script ile aynı yerde olduğundan emin olun.")
        return []
    with open(dosya_adi, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def hizli_yaz(yazi):
    """
    Panoya kopyala ve yapıştır (Ctrl+V) yöntemi.
    En hızlı ve hatasız yöntemdir.
    """
    try:
        pyperclip.copy(yazi)
        time.sleep(0.05) # Panonun dolması için minik bekleme
        pyautogui.hotkey("ctrl", "v")
    except Exception as e:
        print(f"Yazma hatası: {e}")

def rakamlari_karistir(metin):
    """
    Kelimenin harflerine dokunmaz, sadece içindeki rakamların yerlerini rastgele değiştirir.
    Örn: 'admin_123' -> 'admin_312'
    """
    liste = list(metin)
    rakamlar = [c for c in liste if c.isdigit()]
    
    # Karıştırılacak rakam yoksa veya tek rakam varsa aynısını döndür
    if len(rakamlar) < 2:
        return metin

    random.shuffle(rakamlar)
    rakam_iter = iter(rakamlar)
    
    yeni_metin = []
    for char in liste:
        if char.isdigit():
            yeni_metin.append(next(rakam_iter))
        else:
            yeni_metin.append(char)
            
    return "".join(yeni_metin)

def bolgesel_alt_tire_varyasyonlari(kelime):
    """
    Kelimeyi '_' işaretinden ikiye böler.
    Sol ve Sağ tarafın tamamını BÜYÜK/küçük yaparak 4 kombinasyon üretir.
    """
    if "_" not in kelime:
        return []

    # İlk '_' işaretine göre kelimeyi Sol ve Sağ olarak ikiye ayır
    # Örn: "Emirhan_Kuri123" -> sol="Emirhan", sag="Kuri123"
    try:
        sol, sag = kelime.split("_", 1)
    except ValueError:
        return [] # Birden fazla _ varsa veya yapı bozuksa boş dön

    varyasyonlar = []

    # 1. Küçük - Küçük (emirhan_kuri123)
    v1 = sol.lower() + "_" + sag.lower()
    varyasyonlar.append(v1)

    # 2. Büyük - Büyük (EMIRHAN_KURI123)
    v2 = sol.upper() + "_" + sag.upper()
    varyasyonlar.append(v2)

    # 3. Küçük - Büyük (emirhan_KURI123)
    v3 = sol.lower() + "_" + sag.upper()
    varyasyonlar.append(v3)

    # 4. Büyük - Küçük (EMIRHAN_kuri123)
    v4 = sol.upper() + "_" + sag.lower()
    varyasyonlar.append(v4)
    
    return varyasyonlar

def main():
    dosya_adi = "wordlist.txt"
    kelimeler = dosya_oku(dosya_adi)
    
    if not kelimeler:
        return

    print("--- TAM BLOK VARYASYON MODU ---")
    print(f"Hedef: Sol/Sağ blokların tamamını büyük/küçük yapma.")
    print(f"Rakam Karıştırma: Her seçenek için {RAKAM_KARISTIRMA_SAYISI} kez.")
    print(f"Bekleme: {BEKLEME_SURESI} saniye.")
    print("\nLütfen 5 saniye içinde yazılacak alana tıklayın!")

    for i in range(5, 0, -1):
        print(f"{i}...", end=" ", flush=True)
        time.sleep(1)
    print("\nBAŞLADI!\n")

    try:
        for ana_kelime in kelimeler:
            print(f">>> Ana Kelime İşleniyor: {ana_kelime}")
            
            # --- ADIM 1: Aday Listesi Oluştur ---
            # Önce orijinal kelimeyi ekle
            aday_listesi = [ana_kelime]
            
            # Sonra alt tire kurallarını uygula ve ekle
            aday_listesi.extend(bolgesel_alt_tire_varyasyonlari(ana_kelime))
            
            # --- ADIM 2: Rakamları Karıştır ve Son Listeyi Yap ---
            final_deneme_listesi = []
            gorulenler = set()
            
            for aday in aday_listesi:
                # 1. Adayın kendisini (rakamları karışmamış halini) ekle
                if aday not in gorulenler:
                    final_deneme_listesi.append(aday)
                    gorulenler.add(aday)
                
                # 2. Rakam varsa, belirtilen sayıda karıştırıp onları da ekle
                if any(c.isdigit() for c in aday):
                    for _ in range(RAKAM_KARISTIRMA_SAYISI):
                        karisik = rakamlari_karistir(aday)
                        if karisik not in gorulenler:
                            final_deneme_listesi.append(karisik)
                            gorulenler.add(karisik)
            
            # --- ADIM 3: Yazdırma İşlemi ---
            for i, deneme in enumerate(final_deneme_listesi, 1):
                print(f"   [{i}] Deneniyor: {deneme}")
                
                hizli_yaz(deneme)
                pyautogui.press('enter')
                
                # Her denemeden sonra bekle
                time.sleep(BEKLEME_SURESI)
            
            print("-" * 40)

        print("\nTüm liste tamamlandı.")

    except KeyboardInterrupt:
        print("\nİşlem durduruldu.")

if __name__ == "__main__":
    main()