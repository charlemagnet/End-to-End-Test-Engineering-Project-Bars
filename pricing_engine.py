def get_base_price(class_type):
    prices = {
        "Yoga": 200,
        "Boxing": 120,
        "Fitness": 80,
        "Basketball": 40,
        "Tenis": 90, 
        "Swimming": 30
    }
    return prices.get(class_type)

def calculate_dynamic_price(class_type, hour):
    base_price = get_base_price(class_type)
    
    if base_price is None:
        return None
    
    # İş Kuralları (Business Rules)
    if 6 <= hour < 12:
        return base_price * 0.80  # %20 indirim (Sabah)
    elif 12 <= hour < 17:
        return base_price * 1.00  # Standart
    elif 17 <= hour < 24:
        return base_price * 1.10  # %10 zam (Akşam)
    else:
        return base_price

def calculate_refund(class_type, entrances):
    base_price = get_base_price(class_type)
    
    # Geçersiz sınıf için 0 döndür
    if base_price is None:
        return 0
        
    # 2 girişten azsa tam iade
    if entrances < 2:
        return base_price 
    
    # İade oranları
    refund_rates = {
        "Yoga": 0.30,
        "Boxing": 0.50,
        "Fitness": 0.10,
        "Basketball": 0.40,
        "Tenis": 0.80,
        "Swimming": 0.15
    }
    
    # Oranı al ve hesapla
    rate = refund_rates.get(class_type, 0)
    
    return base_price * rate