from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os


load_dotenv()


MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")


client = MongoClient(MONGO_URI)
db = client[DB_NAME]


eslesme_koleksiyonu = db["ilce_yesil_eslesme"]
yesil_koleksiyonu = db["yesil_alanlar"]


for ilce_doc in eslesme_koleksiyonu.find():
    yesil_ids = ilce_doc.get("yesil_alan_ids", [])
    if not yesil_ids:
        continue

    object_ids = [ObjectId(oid) if isinstance(oid, str) else oid for oid in yesil_ids]
    yesil_alanlar = yesil_koleksiyonu.find({"_id": {"$in": object_ids}})

    features = []
    for alan in yesil_alanlar:
        alan.pop("_id", None)  
        features.append(alan)

    feature_collection = {
        "type": "FeatureCollection",
        "features": features
    }

    eslesme_koleksiyonu.update_one(
        {"_id": ilce_doc["_id"]},
        {"$set": {"yesil_alan_geojson": feature_collection}}
    )

print(" Tüm ilçelere yesil_alan_geojson alanı eklendi.")