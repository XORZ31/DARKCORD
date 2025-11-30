# 🖤 DARKCORD ANALYZER V4 — ULTIMATE EDITION  
Discord ID Intelligence • OSINT • Local Dataset Analyzer

Darkcord Analyzer V4, Discord kullanıcı ID’lerini hem **lokal veri setlerinden** hem de **FindCord API üzerinden** tarayarak gelişmiş analizler sunan bir terminal tabanlı OSINT aracıdır.

✔ Snowflake çözümlemesi  
✔ Risk analizi  
✔ Bulk scan  
✔ FindCord API entegrasyonu  
✔ Export sistemi  
✔ History kayıtları  
✔ Ayarlar & API key yönetimi  

---

# 🚀 Özellikler

## 🔹 Lokal Veri Analizi
Program şu dosyalardan veri çeker:
- `data.txt`
- `ID DATA.txt`
- `dcıdsorgudata.txt`
- `discord_data.txt`
- `pdh50i.txt`

Destekler:
- Username → ID eşleştirme  
- ID → kullanıcı profili  
- Ek IP tespiti  
- Forged kayıt analizi  

---

## 🔹 FindCord API Entegrasyonu
- İlk çalıştırmada API key sorulur → config dosyasına kaydedilir  
- Ayarlardan:
  - API key değiştirilebilir  
  - API key silinebilir  
- Canlı kullanıcı bilgisi:
  - username / global name  
  - bio  
  - avatar & banner  
  - sunucu istatistikleri  
  - diğer public metadata  

---

## 🔹 Snowflake Decoder
Snowflake ID üzerinden:
- oluşturulma zamanı  
- hesap yaşı (gün/saat formatında)  
- worker id  
- process id  
- increment id  

tam çözümlenir.

---

## 🔹 Risk Analyzer
Lokal + FindCord verilerine göre risk puanı hesaplar:

**Risk kriterleri:**
- yeni hesap  
- ek IP tespiti  
- forged hit sayısı  
- lokal veri yoksa uyarı  
- FindCord profil durumu  

Sonuç:
- DÜŞÜK / ORTA / YÜKSEK risk  
- Tüm nedenleri listeler  

---

## 🔹 History Kayıt Sistemi
Her sorgu otomatik olarak:

`/history/USERID.json`  

şeklinde kaydedilir.

Kaydedilenler:
- yerel profil verisi  
- IP kayıtları  
- forged veriler  
- FindCord API çıktısı  
- snowflake sonucu  
- risk analizi  
- timestamp  

---

## 🔹 Export — HTML & JSON Rapor
Analiz sonunda:
- JSON export  
- HTML rapor  

çıktıları `/exports/` klasörüne oluşturulur.

---

## 🔹 Bulk Scan (Toplu Analiz)
Bir `.txt` dosyasında ID listesi varsa hepsini sırayla analiz eder:

```txt
714099961549160508
123123123123123
983298329832983

AYARLAR MENÜSÜ

1) Animasyon hızını değiştir
2) Stealth mod aç/kapat
3) FindCord API aç/kapat
4) API key değiştir
5) API key sil




darkcord/
 ├── main.py
 ├── README.md
 ├── requirements.txt
 ├── data_files/
 │     ├── data.txt
 │     ├── ID DATA.txt
 │     ├── dcıdsorgudata.txt
 │     ├── discord_data.txt
 │     ├── pdh50i.txt
 ├── history/      (otomatik oluşturulur)
 ├── exports/          (otomatik oluşturulur)
 └── darkcord_config.json   (otomatik oluşturulur)









🔨 Kurulum
1) Bağımlılık kurulumu
pip install -r requirements.txt

2) Çalıştır
python main.py

3) İlk açılışta API key gir

Uygulama sadece bir kez sorar ve kaydeder.







------------------------------------------------------------
                 DARKCORD ANALYZER - ID ANALİZ
------------------------------------------------------------

[LOCAL LOOKUP]
username: creativespace3704
email: discord9@aefnet.com
...

[FINDCORD LOOKUP]
username: test#0001
bio: hello world
banner: URL
avatar: URL
...

[RISK ANALYZER]
Risk skoru: 70 (YÜKSEK)
- Hesap genç
- Ek IP tespiti
- Forged kayıtlarında bulunuyor

[EXPORT]
1) JSON rapor
2) HTML rapor



Snowflake Decoder Örneği

-timestamp: 2025-07-29T01:23:15Z
-age_days: 112
-worker_id: 3
-process_id: 1
-increment: 842


🧷 Bulk Scan Örneği

[1/3] ID: 714099961549160508 → RISK: YÜKSEK
[2/3] ID: 123123123123123     → RISK: ORTA
[3/3] ID: 999999999999999     → RISK: DÜŞÜK



🚨 Hata Çözümleri
❌ "FindCord error: unauthorized"

--API key yanlış → Ayarlardan değiştir.

❌ JSON decode error

--data_files içindeki dosyalardan biri bozuk → düzelt.

❌ "requests bulunamadı"

Şunu yükle:

  "pip install requests"

❌ Windows Türkçe karakter bozuk

CMD’de:

  "chcp 65001"

📦 requirements.txt
  "requests"

📜 Lisans

Bu proje tamamen eğitim, analiz ve OSINT amaçlıdır.
Kötüye kullanım geliştiricinin sorumluluğu değildir.

✉️ İletişim / Destek

Yeni özellik istersen, hata bildirirsen veya geliştirmek istersen — yazman yeterli.
🌐https://l9ga.com.tr
🐈‍⬛https://github.com/XORZ31

Oluşturan: XORZ