from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
from models import IlceVerisi
import os


load_dotenv()


MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ilceler/{ilce_adi}", response_model=IlceVerisi)
def get_ilce_verisi(ilce_adi: str):
    try:
        veri = collection.find_one({"ilce": ilce_adi})
        if not veri:
            raise HTTPException(status_code=404, detail="İlçe verisi bulunamadı")
        veri.pop("_id", None)  # ObjectId JSON ile uyumlu değil
        return IlceVerisi(**veri)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hata: {e}")


@app.get("/yesil_alanlar/{ilce_adi}")
def get_yesil_alanlar(ilce_adi: str):
    eslesme = db["ilce_yesil_eslesme"].find_one({"ilce": ilce_adi})
    if not eslesme:
        raise HTTPException(status_code=404, detail="İlçe bulunamadı")

    return eslesme.get("yesil_alan_geojson", {
        "type": "FeatureCollection",
        "features": []
    })