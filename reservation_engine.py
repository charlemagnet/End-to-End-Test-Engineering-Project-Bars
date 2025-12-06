from database import get_db

RESERVATION_ID_COUNTER = 1 # Not: Gerçek projede UUID kullanılır ama şimdilik kalsın.

CAPACITY_LIMITS = {
    "Yoga": 50,
    "Boxing": 40,
    "Fitness": 250,
    "Basketball": 20,
    "Tenis": 15,
    "Swimming": 30
}

def check_capacity(class_type, date, hour):
    """
    MongoDB'den o gün ve saatteki rezervasyon sayısını sorgular.
    """
    db = get_db()
    reservations_collection = db["reservations"]
    
    limit = CAPACITY_LIMITS.get(class_type, 0)
    
    # SORGULA: class_type, date, hour eşleşen ve durumu Active olanları say
    current_occupancy = reservations_collection.count_documents({
        "class_type": class_type,
        "date": date,
        "hour": hour,
        "status": "Active"
    })
    
    return current_occupancy < limit

def create_reservation(member_id, class_type, date, hour):
    # ID üretimi için basit bir yöntem (Mongo normalde kendi ObjectId'sini üretir)
    # Tutarlılık için rastgele sayı kullanalım veya counter mantığını değiştirelim.
    import random
    res_id = random.randint(10000, 99999) 
    
    if not check_capacity(class_type, date, hour):
        raise ValueError(f"Capacity full for {class_type} on {date} at {hour}:00")

    db = get_db()
    
    reservation = {
        "_id": res_id,
        "member_id": member_id,
        "class_type": class_type,
        "date": date,
        "hour": hour,
        "status": "Active"
    }
    
    db["reservations"].insert_one(reservation)
    
    # API uyumluluğu için _id'yi id olarak dönüştürelim
    reservation["id"] = reservation["_id"]
    return reservation

def cancel_reservation(reservation_id):
    db = get_db()
    reservations_collection = db["reservations"]
    
    # Güncelleme işlemi ($set)
    result = reservations_collection.find_one_and_update(
        {"_id": reservation_id},
        {"$set": {"status": "Cancelled"}},
        return_document=True # Güncel halini döndür
    )
    
    if result is None:
        raise KeyError("Reservation not found")
        
    result["id"] = result["_id"]
    return result   