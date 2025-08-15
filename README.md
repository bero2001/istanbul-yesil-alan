# İstanbul Kişi Başı Yeşil Alan Analizi

Bu proje, İstanbul ilçelerinin kişi başına düşen yeşil alan miktarını hesaplayan ve harita üzerinde görselleştiren bir **Coğrafi Bilgi Sistemleri (CBS)** uygulamasıdır.  
Backend kısmı **FastAPI** ve **MongoDB** kullanılarak geliştirilmiştir. Frontend kısmında **MapLibre GL JS** ve **Turf.js** ile harita üzerinde görselleştirme yapılmaktadır.

## 🚀 Özellikler
- İlçelere ait kişi başı yeşil alan verilerini MongoDB’den API ile sunar.
- İlçelere ait yeşil alan GeoJSON verilerini döndürür.
- CORS desteği ile harita tabanlı frontend uygulamalardan veri çekilebilir.
- `.env` dosyası ile hassas bilgiler gizlenir.

## 📂 Proje Yapısı
ISTANBUL-YESIL-ALAN/
├─ backend/
│  └─ fastapi_backend/
│     ├─ Configs/                  # GeoJSON veri dosyaları
│     ├─ main.py                    # FastAPI uygulaması
│     ├─ models.py
│     ├─ yukle_geojson.py
│     ├─ yesil_ilce_eslesme.py
│     └─ hesapla_ve_kaydet.py
├─ frontend/
│  ├─ index.html
│  ├─ script.js
│  ├─ style.css
├─ .env.example
├─ .gitignore
├─ README.md
└─ requirements.txt

## ⚙️ Kurulum

1. **Repoyu klonlayın**
```bash
git clone https://github.com/kullanici-adi/ISTANBUL-YESIL-ALAN.git
cd ISTANBUL-YESIL-ALAN

python -m venv .venv
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

MONGO_URI=mongodb+srv://<username>:<password>@<cluster-url>/<dbname>



uvicorn backend.fastapi_backend.main:app --reload
Tarayıcıdan http://127.0.0.1:8000/docs adresine giderek API uç noktalarını görebilirsiniz.

## 📌 API Uç Noktaları

### İlçe Verisi Getirme
```http
GET /ilceler/{ilce_adi}
{
  "ilce": "Beşiktaş",
  "yesil_alan_m2": 1637770.0065245286,
  "nufus": 167264,
  "kisi_basi_m2": 9.79152720564215
}

GET /yesil_alanlar/{ilce_adi}

{
  "type": "FeatureCollection",
  "features": [...]
}

## 🛠 Kullanılan Teknolojiler
- **Backend:** FastAPI, PyMongo
- **Database:** MongoDB
- **Frontend:** MapLibre GL JS, Turf.js
- **Ortam Değişkenleri:** python-dotenv

---

## 📜 Lisans
Bu proje MIT lisansı altında sunulmaktadır. Detaylar için [LICENSE](LICENSE) dosyasına bakabilirsiniz.
"# istanbul-yesil-alan" 
