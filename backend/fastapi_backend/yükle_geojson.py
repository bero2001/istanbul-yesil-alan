import json
from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()


MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")


client = MongoClient(MONGO_URI)
db = client[DB_NAME]


ilce_koleksiyonu = db["ilce_geojson"]
yesil_alan_koleksiyonu = db["yesil_alanlar"]


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ilce_geojson_path = os.path.join(BASE_DIR, "Configs", "ilce_geojson.json")
yesil_alan_path = os.path.join(BASE_DIR, "Configs", "yesil_alanlar.geojson")


with open(ilce_geojson_path, "r", encoding="utf-8") as f:
    ilce_data = json.load(f)
    if "features" in ilce_data:
        ilce_koleksiyonu.delete_many({})  
        ilce_koleksiyonu.insert_many(ilce_data["features"])
        print(" İlçe GeoJSON MongoDB'ye yüklendi.")
    else:
        print(" ilce_geojson.json dosyasında 'features' alanı eksik.")


with open(yesil_alan_path, "r", encoding="utf-8") as f:
    yesil_alan_data = json.load(f)
    if "features" in yesil_alan_data:
        yesil_alan_koleksiyonu.delete_many({})
        yesil_alan_koleksiyonu.insert_many(yesil_alan_data["features"])
        print(" Yeşil alan GeoJSON MongoDB'ye yüklendi.")
    else:
        print(" yesil_alanlar.geojson dosyasında 'features' alanı eksik.")