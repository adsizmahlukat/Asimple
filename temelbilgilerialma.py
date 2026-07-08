import tkinter as tk # Python'ın standart arayüz kütüphanesini 'tk' takma adıyla içeri aktarırız.
from tkinter import filedialog # Windows'un dosya seçme penceresini açmak için kullanılan özel alt modül.
from tkinter import messagebox

import os #Python'da bir dosyanın boyutunu öğrenmek için os modülünün içindeki path.getsize() fonksiyonunu kullanırız
from datetime import datetime
#"Gün.Ay.Yıl Saat:Dakika" formatına çevirmek için Python'ın içindeki datetime kütüphanesini kullanırız.

def dosya_bilgilerini_oku():
    # Sabit yol yerine Windows dosya seçme penceresini açıyoruz:
    # askopenfilename() fonksiyonu Windows dosya seçme penceresini açar.
    # Kullanıcı bir dosya seçtiğinde, o dosyanın tam yolunu (C:\... veya D:\...) döndürür ve 'mainfile' değişkenine eşitleyecektir.
    mainfile = filedialog.askopenfilename()
    # Eğer kullanıcı dosya seçmeden iptale bastıysa altındaki kodların çalışmasını engelle:
    if not mainfile:
        return

    rapor = ""
    #os.path.exists(),
    # Python'da belirtilen bir dosya veya klasörün bilgisayarınızda gerçekten var olup olmadığını kontrol eden bir fonksiyondur.

    #DOSYA BOYUTUNU ALMA

    if os.path.exists(mainfile):
        # Eski hali: print("Dosya yolundaki dosya bulundu.")
        # Yeni hali: Rapor metnine bu yazıyı ekle ve (\n) ile alt satıra geç
        rapor += "✅ Dosya yolundaki dosya bulundu.\n"

        file_byte = os.path.getsize(mainfile)
        size = file_byte / (1024 * 1024)
        rapor += (f"📂 Dosya Adı: {mainfile}\n")
        rapor += (f"⚖️ Boyut: {size:.2f} MB\n")

        #Dosya içindekileri listeler:
        #for isim in os.listdir(mainfile):
            #print(f"- {isim}")
    else:
        print(f"D diskindeki '{mainfile}' klasörü bulunamadı!")

    #DOSYA OLUŞTURULMA TARİHİNİ ALMA

    #Dosyanın bilgisayardaki ham zaman damgasını alın

    if os.path.exists(mainfile):
        zaman_damgasi = os.path.getctime(mainfile)
        okunabilir_zaman = datetime.fromtimestamp(zaman_damgasi) #Bu sayıyı bizim okuyabileceğimiz "Gün.Ay.Yıl Saat:Dakika" formatına çevirmek için Python'ın içindeki datetime kütüphanesini kullanırız.
        düzenli_zaman = okunabilir_zaman.strftime("%d/%m/%Y %H:%M:%S") #Bizim günlük hayatta bu hassasiyete ihtiyacımız olmadığı için o kısmı gizlemek isteriz. İşte burada devreye strftime() (string format time) fonksiyonu giriyor.
        rapor += (f"📅 Dosyanın zaman damgası: {düzenli_zaman}\n")

    else:
        print("Dosyanın zaman değişkenine ulaşılamıyor")

    #SON AÇILMA TARİHİ

    if os.path.exists(mainfile):
        son_zaman_damgasi = os.path.getatime(mainfile)
        okunabilir_son_zaman_damgasi = datetime.fromtimestamp(son_zaman_damgasi)
        düzenli_son_zaman_damgasi = okunabilir_son_zaman_damgasi.strftime("%d/%m/%Y %H:%M:%S")
        rapor += (f"👁️ Dosya en son şu vakit açılmış: {düzenli_son_zaman_damgasi}\n")

        sonuc_etiketi.config(text=rapor)


pencere = tk.Tk() # tk.Tk() komutu, uygulamamızın ana gövdesini oluşturan boş ve görünmez bir pencere (tuval) üretir.
pencere.title("Asimple")  #Ekranda açılacak olan pencerenin sol üst köşesindeki başlık metnini belirler.
pencere.geometry("400x300") # Pencerenin genişlik ve yükseklik boyutunu piksel cinsinden ayarlar (Genişlik x Yükseklik).


# pady değerini 80 yerine 40 yaparak butonu biraz daha yukarı aldık
# tk.Button() fiziksel bir buton oluşturur.
# 'pencere' parametresi butonun bu pencere içinde yer alacağını söyler.
# 'text' butonun üzerindeki yazıdır.
# 'command' ise en kritik yerdir: Butona tıklandığında yukarıda yazdığımız hangi görevin (fonksiyonun) tetikleneceğini söyler. (Parantez () açılmadan sadece adı yazılır).
buton = tk.Button(pencere, text= "Dosya Seç ve Bilgi Oku",  command=dosya_bilgilerini_oku)
# pack() fonksiyonu, oluşturulan butonu pencerenin içine fiziksel olarak yerleştirir (paketi açar).
# 'pady=40' parametresi, butonun üstünden ve altından 40 piksellik dikey boşluk bırakarak sayfada sıkışık durmamasını sağlar.
buton.pack(pady=20)

sonuc_etiketi = tk.Label(pencere, text= "Lütfen bir dosya seçin...", justify="left", font=("Times New Roman", 10))
sonuc_etiketi.pack(pady=20)

# mainloop() Python'a "Bu pencereyi ekranda çiz ve kullanıcı kapatma (X) butonuna basana kadar sürekli açık tut, arkada döngüye al" emrini verir.
# Bu satırın altında kalan hiçbir kod pencere kapatılmadan çalışmaz. O yüzden her zaman en sonda yer alır.
pencere.mainloop()




