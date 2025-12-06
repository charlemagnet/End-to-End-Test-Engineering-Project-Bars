# main.py - MONGODB SÜRÜMÜ
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field, BeforeValidator
from typing import Optional, Annotated, List
from bson import ObjectId

# Import hatası alırsan bu dosyanın main.py ile aynı klasörde olduğundan emin ol
from pricing_engine import calculate_dynamic_price, calculate_refund
# database.py dosyasını oluşturduğunu varsayıyorum
from database import reservations_collection 

app = FastAPI(
    title="Fitness Center API (NoSQL)",
    description="Dynamic Pricing and Reservation Service with MongoDB"
)

# Kapasite Ayarları
CAPACITIES = {
    "Yoga": 50, "Boxing": 40, "Fitness": 250,
    "Basketball": 20, "Tennis": 15, "Tenis": 15, "Swimming": 30
}

# --- Pydantic Modelleri ---
PyObjectId = Annotated[str, BeforeValidator(str)]

class ReservationModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    class_type: str
    member_name: str
    date: str  # Format: "YYYY-MM-DD"
    hour: int
    price: Optional[float] = None
    status: str = "Active"

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "class_type": "Yoga",
                "member_name": "Mehmet Yilmaz",
                "date": "2025-10-18",
                "hour": 14
            }
        }

# --- Endpointler ---

@app.get("/")
def read_root():
    return {"message": "API Calisiyor (MongoDB Baglantili)"}

@app.post("/reservations", response_model=ReservationModel, status_code=201)
def create_reservation(reservation: ReservationModel):
    # 1. Kapasite Kontrolü
    max_capacity = CAPACITIES.get(reservation.class_type)
    if not max_capacity:
        raise HTTPException(status_code=400, detail="Gecersiz ders tipi.")

    # MongoDB'den doluluk oranını sorgula
    current_count = reservations_collection.count_documents({
        "class_type": reservation.class_type,
        "date": reservation.date,
        "hour": reservation.hour,
        "status": "Active"
    })

    if current_count >= max_capacity:
        raise HTTPException(status_code=400, detail=f"Kontenjan Dolu! ({current_count}/{max_capacity})")

    # 2. Fiyat Hesaplama
    # Burada hata alıyorsan pricing_engine.py kaydedilmemiştir!
    calculated_price = calculate_dynamic_price(reservation.class_type, reservation.hour)
    if calculated_price is None:
        raise HTTPException(status_code=400, detail="Fiyat hesaplanamadi.")

    # 3. Kayıt
    new_reservation = reservation.model_dump(by_alias=True, exclude=["id"])
    new_reservation["price"] = round(calculated_price, 2)
    new_reservation["status"] = "Active"

    insert_result = reservations_collection.insert_one(new_reservation)
    
    created_reservation = reservations_collection.find_one(
        {"_id": insert_result.inserted_id}
    )
    return created_reservation

@app.post("/reservations/{reservation_id}/cancel")
def cancel_reservation(reservation_id: str, entrances_used: int = Body(..., embed=True)):
    if not ObjectId.is_valid(reservation_id):
        raise HTTPException(status_code=400, detail="Gecersiz ID formati")

    reservation = reservations_collection.find_one({"_id": ObjectId(reservation_id)})
    if not reservation:
        raise HTTPException(status_code=404, detail="Rezervasyon bulunamadi")

    refund = calculate_refund(reservation["class_type"], entrances_used)

    reservations_collection.update_one(
        {"_id": ObjectId(reservation_id)},
        {"$set": {"status": "Cancelled"}}
    )

    return {"status": "success", "refund": refund}