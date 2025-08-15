import geopandas as gpd
from pymongo import MongoClient
import pandas as pd
import json
from dotenv import load_dotenv
import os


load_dotenv()


MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")


ilce_nufus = {
    "Adalar": 16979,
    "Arnavutköy": 344868,
    "Ataşehir": 414866,
    "Avcılar": 440934,
    "Bağcılar": 713594,
    "Bahçelievler": 560086,
    "Bakırköy": 219893,
    "Başakşehir": 520467,
    "Bayrampaşa": 268303,
    "Beşiktaş": 167264,
    "Beykoz": 245440,
    "Beylikdüzü": 415290,
    "Beyoğlu": 216688,
    "Büyükçekmece": 280528,
    "Çatalca": 80399,
    "Çekmeköy": 306739,
    "Esenler": 423625,
    "Esenyurt": 988369,
    "Eyüpsultan": 420706,
    "Fatih": 354472,
    "Gaziosmanpaşa": 479931,
    "Güngören": 264831,
    "Kadıköy": 462189,
    "Kağıthane": 444820,
    "Kartal": 475859,
    "Küçükçekmece": 789033,
    "Maltepe": 524921,
    "Pendik": 749356,
    "Sancaktepe": 502077,
    "Sarıyer": 342582,
    "Şile": 48936,
    "Silivri": 232156,
    "Şişli": 263063,
    "Sultanbeyli": 369193,
    "Sultangazi": 532601,
    "Tuzla": 301400,
    "Ümraniye": 727819,
    "Üsküdar": 512981,
    "Zeytinburnu": 278344
}




gdf_ilce = gpd.read_file("Configs/ilce_geojson.json")
gdf_yesil = gpd.read_file("Configs/yesil_alanlar.geojson")

with open("Configs/ilce_geojson.json", encoding="utf-8") as f:
    raw_geojson = json.load(f)


ilce_adlari = []
for feat in raw_geojson["features"]:
    props = feat.get("properties", {})
    address = props.get("address", {})
    town = address.get("town")
    ilce_adlari.append(town)

gdf_ilce["ilce"] = ilce_adlari
gdf_ilce = gdf_ilce[gdf_ilce["ilce"].isin(ilce_nufus.keys())]

print(f" İlçe CRS: {gdf_ilce.crs}")
print(f" Yeşil Alan CRS: {gdf_yesil.crs}")


gdf_ilce = gdf_ilce.to_crs(epsg=3857)
gdf_yesil = gdf_yesil.to_crs(epsg=3857)


gdf_ilce["geometry"] = gdf_ilce.geometry.buffer(0)
gdf_yesil["geometry"] = gdf_yesil.geometry.buffer(0)

print(" İlçe adları:", gdf_ilce["ilce"].unique())
print(" Toplam ilçe sayısı:", len(gdf_ilce))
print(" Toplam yeşil alan sayısı:", len(gdf_yesil))


kesisimler = []
for _, ilce in gdf_ilce.iterrows():
    for _, yesil in gdf_yesil.iterrows():
        try:
            if ilce.geometry.intersects(yesil.geometry):
                intersection = ilce.geometry.intersection(yesil.geometry)
                if not intersection.is_empty:
                    alan = intersection.area
                    kesisimler.append({
                        "ilce": ilce["ilce"],
                        "yesil_alan_m2": alan
                    })
        except Exception as e:
            print(f" Hata: {e}")
            continue

print(f"\n Toplam kesişim sayısı: {len(kesisimler)}")
if not kesisimler:
    print(" Hiçbir yeşil alan ilçelerle kesişmedi.")
else:
    print(" Kesişim verileri başarıyla toplandı.")


summary = pd.DataFrame(kesisimler)
if not summary.empty:
    summary = summary.groupby("ilce", as_index=False)["yesil_alan_m2"].sum()
    summary["nufus"] = summary["ilce"].map(ilce_nufus)
    summary["kisi_basi_m2"] = summary["yesil_alan_m2"] / summary["nufus"]
else:
    print(" Uyarı: Kesişim verisi boş, MongoDB'ye ekleme yapılmadı.")


if not summary.empty:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    col = db[COLLECTION_NAME]
    col.delete_many({})
    col.insert_many(summary.to_dict(orient="records"))
    print(" MongoDB'ye veri kaydedildi.")
    print(summary)
else:
    print(" Uyarı: MongoDB'ye veri yazılmadı.")
