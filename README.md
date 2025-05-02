# HoloControl
Bu proje, kullanıcıların el hareketlerini algılayarak bilgisayarı kontrol etmelerini sağlayan bir sistemdir. MediaPipe ve OpenCV kullanılarak geliştirilen sistem, jest tabanlı etkileşimle mouse hareketi, tıklama, pencere geçişi gibi işlemleri gerçekleştirebilir. Hedef, dokunmadan tamamen doğal ve temassız bir kullanıcı deneyimi sunmaktır.
# kameraAcma.py
## Amaç:
İlk prototip. Klavye tuşlarını ekran üzerinde çizip, işaret parmağı ile bir tuşun üzerine geldiğinde karakter giren basit sanal klavye.

## Özellikler:
Sabit sanal klavye yerleşimi
- İşaret parmağı koordinatları ile tuş seçimi
- Space, Backspace ve Enter desteği
- Hover mantığı ile yazım (basma yerine sabit bekleme)
# güncelleme1.py
## Amaç:
Kod yapısı sadeleştirildi, tuşlar hover süresiyle algılanıyor. Tuş yazımı daha kontrollü hale getirildi.

## Yeni Özellikler:
- Daha net yazı kutusu
- Hover süresi ile tuş yazımı (15 frame)
- Renkli ve stilize tuşlar
- Temiz modülerlik: draw_keyboard() fonksiyonu
![Ekran görüntüsü 2025-05-02 172123](https://github.com/user-attachments/assets/d67aefc0-b7c6-4963-b8e4-5efbdcbd9696)

# güncelleme2.py
## Amaç:
Dairesel tuşlara geçiş, tuş türlerine göre farklı görselleştirme, emoji ve özel tuşlar eklendi.

## Yeni Özellikler:
- Daire şeklinde tuş çizimi
- Space, Emoji, Return, 123 gibi geniş tuşlar
- Hover threshold uygulanmaya devam ediyor
- Sanal klavye düzeni mobil görünüm gibi
![Ekran görüntüsü 2025-05-02 172626](https://github.com/user-attachments/assets/0937ccba-9fe5-41b9-8f08-86263ff71622)

# güncelleme3.py
## Amaç:
El jestleriyle bilgisayar kontrolü! Klavye yerini tamamen jestler aldı. Mouse ve sistem kısayolları kontrol edilebiliyor.

## Eklenen Jestler:
| Jest | İşlev |
|--------------------------|------------------|
| 👌 Baş + işaret birleşimi | Mouse click |
| ✋ Avuç açık | Mouse takip |
| ✊ Yumruk | Alt + Tab geçiş |
| 👉 İşaret sağa hareket | Sağ ok tuşu |

## Sonradan eklenen:
- Tek tıklama
- Çift tıklama desteği
- Cooldown sistemi (spam engelleyici)






