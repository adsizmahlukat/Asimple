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


def klasor_okuma():
    # 'su_anki_klasor' değişkenini global yaparak, tüm fonksiyonların bu yola erişmesini sağlıyoruz.
    global su_anki_klasor

    su_anki_klasor = filedialog.askdirectory()
    if not su_anki_klasor:
        return

    liste_kutusu.delete(0, tk.END)

    if os.path.exists(su_anki_klasor):
        icerik_listesi = os.listdir(su_anki_klasor)
        for isim in icerik_listesi:
            liste_kutusu.insert(tk.END, f"📄 {isim}")

    else:
        liste_kutusu.insert(tk.END, "HATA: Klasör yoluna ulaşılamadı!")

            # TEST İÇİN BUNU EKLEYİN: Bilgiler etikete gitmiyorsa terminale basıyor mu bakalım
    print("Döngü bitti, hazırlanan metin:\n", file)

        # Hazırladığımız bu yeni listeyi ekrandaki etiketimize basıyoruz.
    sonuc_etiketi.config(text=file)


# 'event' parametresi, çift tıklama eyleminin tüm bilgilerini (koordinat, tıklanan yer vb.) otomatik taşır.
def listeye_cift_tıklandi(event):
    # 1. Kullanıcının listeden hangi satırı seçtiğini index (sıra numarası) olarak alıyoruz.
    secilen_index = liste_kutusu.curselection()

    # Eğer kullanıcı boş bir yere tıkladıysa işlem yapma
    if not secilen_index:
        return

    # 2. Seçilen satırdaki yazıyı alıyoruz (Örn: "📄 Vilog.mp4")
    secilen_metin = liste_kutusu.get(secilen_index)
    dosya_adi = secilen_metin.replace("📄 ", "")

    # os.path.join() klasör yolu ile dosya adını güvenli bir şekilde birleştirir.
    # Örn: "D:\Videolar" + "Vilog.mp4" -> "D:\Videolar\Vilog.mp4"

    tam_dosya_yolu = os.path.join(su_anki_klasor, dosya_adi)

    # os.startfile() fonksiyonu, Windows'ta o dosyaya çift tıklamışsınız gibi
    # dosyayı kendi varsayılan programıyla (VLC, Fotoğraflar, Word vb.) açar.
    if os.path.exists(tam_dosya_yolu):
        os.startfile(tam_dosya_yolu)

    # 3. Başındaki "📄 " emojisini temizleyip sadece gerçek dosya adını alıyoruz.
    # .replace() fonksiyonu metindeki bir karakteri başka bir karakterle değiştirir.
    dosya_adi = secilen_metin.replace("📄 ", "")

    # Şimdi çok önemli bir sorunumuz var: Bilgisayar bu dosyanın HANGİ klasörde olduğunu bilmiyor.
    # Bunu çözmek için 'klasor_icerigini_listele' fonksiyonunda seçtiğimiz klasör yoluna ihtiyacımız var!


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

klasor_butonu = tk.Button(pencere, text="Klasör Seç ve İçeriğini Listele", command=klasor_okuma)
klasor_butonu.pack(pady=10)

sonuc_etiketi = tk.Label(pencere, text= "Lütfen bir dosya seçin...", justify="left", font=("Times New Roman", 10))
sonuc_etiketi.pack(pady=20)

# mainloop() Python'a "Bu pencereyi ekranda çiz ve kullanıcı kapatma (X) butonuna basana kadar sürekli açık tut, arkada döngüye al" emrini verir.
# Bu satırın altında kalan hiçbir kod pencere kapatılmadan çalışmaz. O yüzden her zaman en sonda yer alır.

# 1. Klasör listesini göstereceğimiz kutu (Listbox)
# 'width' genişliği, 'height' ise ekranda tek seferde kaç satır görüneceğini belirler.
liste_kutusu = tk.Listbox(pencere, width=70, height=15, font=("Arial", 10))

# 2. Sağa koyacağımız dikey kaydırma çubuğu (Scrollbar)
kaydirma_cubugu = tk.Scrollbar(pencere, orient="vertical")

# 3. Bu iki parçayı birbirine evlendiriyoruz (Bağlıyoruz)
# Liste kutusu kaydırıldığında çubuğu hareket ettir, çubuk çekildiğinde listeyi kaydır.
liste_kutusu.config(yscrollcommand=kaydirma_cubugu.set)
kaydirma_cubugu.config(command=liste_kutusu.yview)

# 4. Ekrana yerleştirme (Pack)
# 'side=tk.RIGHT' çubuğu sağa yaslar, 'fill=tk.Y' yukarıdan aşağıya uzatır.
kaydirma_cubugu.pack(side=tk.RIGHT, fill=tk.Y)
# Liste kutusunu da sola yaslayıp kalan boşluğu doldurtuyoruz.
liste_kutusu.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=10)
# '<Double-Button-1>' ifadesi, fare sol tuşuna çift tıklama anlamına gelen evrensel bir Git/Tkinter kodudur.
liste_kutusu.bind('<Double-Button-1>', listeye_cift_tıklandi)




pencere.mainloop()




