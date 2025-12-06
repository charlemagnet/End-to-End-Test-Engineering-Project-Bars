# database.py
from pymongo import MongoClient

# Lokal MongoDB bağlantısı (Docker veya yerel kurulum)
# Eğer MongoDB Atlas (Cloud) kullanıyorsan buraya connection string'ini yazmalısın.
MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)

# Veritabanı adı
db = client["fitness_db"]

# Koleksiyonlar (SQL'deki tabloların karşılığı)
reservations_collection = db["reservations"]
members_collection = db["members"]