
from pymongo import MongoClient

# MongoDB Bağlantı Stringi
# Eğer bilgisayarınızda yerel Mongo kuruluysa:
MONGO_URI = "mongodb://localhost:27017/"

def get_db():
    client = MongoClient(MONGO_URI)
    # Veritabanı adı: 'fitness_db'
    db = client["fitness_db"]
    return db
    