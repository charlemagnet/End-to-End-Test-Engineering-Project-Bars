# database.py (DÜZELTİLMİŞ HALİ)
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# URL'i al
MONGO_URI = os.getenv("MONGO_URL", "mongodb://localhost:27017")

try:
    client = MongoClient(MONGO_URI)
    # Bağlantı testi
    client.admin.command('ping')
    print("✅ Başarıyla MongoDB Atlas (Bulut) veritabanına bağlandı!")
except Exception as e:
    print(f"❌ Veritabanı bağlantı hatası: {e}")

# --- KRİTİK DÜZELTME BURADA ---
# Veritabanı objesi
db = client["fitness_db"]

# Diğer dosyaların import etmeye çalıştığı koleksiyonlar
reservations_collection = db["reservations"]
members_collection = db["members"]

def get_db():
    return db