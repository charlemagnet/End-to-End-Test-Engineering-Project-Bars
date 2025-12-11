def get_base_price(class_type):
    """
    Ders tipine göre baz fiyatı döndürür.
    """
    prices = {
        "Yoga": 100,       # Testin beklediği değer (Eskiden 200 kalmış olabilir)
        "Boxing": 120,
        "Fitness": 80,
        "Swimming": 150,
        "Basketball": 90,
        "Tennis": 130,
        "Tenis": 130
    }
    # Bilinmeyen dersler için varsayılan fiyat 100
    return prices.get(class_type, 100)

def calculate_dynamic_price(base_price, hour):
    """
    Saate göre fiyat çarpanı uygular.
    """
    if hour < 0 or hour > 24:
        raise ValueError("Invalid hour")
        
    if 6 <= hour < 10:       # Sabah İndirimi (%20)
        return base_price * 0.8
    elif 18 <= hour < 22:    # Akşam Zammı (%50) -> Hatayı düzelttik
        return base_price * 1.5
    else:                    # Standart
        return base_price * 1.0

def calculate_refund(paid_amount, attendance_count, class_type):
    """
    Gelişmiş İade Politikası
    """
    
    # İade oranları tablosu
    refund_rates = {
        "Yoga": 0.3,
        "Boxing": 0.5,
        "Fitness": 0.1,
        "Basketball": 0.4,
        "Swimming": 0.15,
        "Tennis": 0.8,
        "Tenis": 0.8
    }

    # KRİTİK DÜZELTME: Önce dersin geçerli olup olmadığına bakmalıyız!
    # Eğer ders listede yoksa, katılım sayısı ne olursa olsun 0 iade dönmeli.
    if class_type not in refund_rates:
        return 0.0

    # KURAL: Ders geçerliyse ve katılım 2'den azsa -> TAM İADE
    if attendance_count < 2:
        return paid_amount * 1.0
    
    # KURAL: Katılım 2 ve üzeriyse -> Tablodaki oran
    rate = refund_rates.get(class_type, 0.0)
    
    return paid_amount * rate
