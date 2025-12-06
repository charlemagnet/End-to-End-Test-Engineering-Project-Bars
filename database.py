# database.py
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri yükle
load_dotenv()

# URL'i .env dosyasından al, bulamazsa localhost kullan (Fallback)
MONGO_URI = os.getenv("MONGO_URL", "mongodb://localhost:27017")

try:
    # Bulut bağlantısı
    client = MongoClient(MONGO_URI)
    
    # Bağlantıyı test et (Hata varsa catch bloğuna düşer)
    client.admin.command('ping')
    print("✅ Başarıyla MongoDB Atlas (Bulut) veritabanına bağlandı!")
    
except Exception as e:
    print(f"❌ Veritabanı bağlantı hatası: {e}")

# Veritabanı adı (Atlas linkinin sonuna /fitness_db yazmadıysan burada belirt)
# .env içindeki linkte /fitness_db varsa client.get_database() boş bırakılabilir
db = client["fitness_db"]

reservations_collection = db["reservations"]
members_collection = db["members"]