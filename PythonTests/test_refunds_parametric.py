import pytest
from pricing_engine import calculate_refund

# (Ders Tipi, Baz Fiyat, Katılım Sayısı, Beklenen İade)
refund_scenarios = [
    # YOGA (Baz: 200 kabul edelim test için)
    # < 2 giriş -> Tam iade, >= 2 giriş -> %30 iade
    ("Yoga", 200, 0, 200.0),
    ("Yoga", 200, 1, 200.0),
    ("Yoga", 200, 2, 60.0),  # 200 * 0.3 = 60
    ("Yoga", 200, 5, 60.0),
    ("Yoga", 200, 10, 60.0),

    # BOXING (Baz: 120)
    # < 2 giriş -> Tam iade, >= 2 giriş -> %50 iade
    ("Boxing", 120, 0, 120.0),
    ("Boxing", 120, 1, 120.0),
    ("Boxing", 120, 2, 60.0), # 120 * 0.5 = 60
    ("Boxing", 120, 3, 60.0),
    ("Boxing", 120, 8, 60.0),

    # FITNESS (Baz: 80)
    # < 2 giriş -> Tam iade, >= 2 giriş -> %10 iade
    ("Fitness", 80, 0, 80.0),
    ("Fitness", 80, 1, 80.0),
    ("Fitness", 80, 2, 8.0),  # 80 * 0.1 = 8
    ("Fitness", 80, 4, 8.0),
    ("Fitness", 80, 20, 8.0),
    
    # BASKETBALL (Baz: 40) -> %40 iade
    ("Basketball", 40, 0, 40.0),
    ("Basketball", 40, 1, 40.0),
    ("Basketball", 40, 2, 16.0), # 40 * 0.4 = 16

    # TENNIS (Baz: 90) -> %80 iade
    ("Tennis", 90, 0, 90.0),
    ("Tennis", 90, 1, 90.0),
    ("Tennis", 90, 2, 72.0), # 90 * 0.8 = 72

    # SWIMMING (Baz: 30) -> %15 iade
    ("Swimming", 30, 0, 30.0),
    ("Swimming", 30, 1, 30.0),
    ("Swimming", 30, 2, 4.5), # 30 * 0.15 = 4.5
    
    # GEÇERSİZ DERS
    ("Futbol", 100, 1, 0),
]

@pytest.mark.parametrize("class_type, base_price, entrances, expected_refund", refund_scenarios)
def test_refund_calculations_parametric(class_type, base_price, entrances, expected_refund):
    # DÜZELTME: Fonksiyonu 3 parametre ile çağırıyoruz
    calculated = calculate_refund(base_price, entrances, class_type)
    
    assert calculated == pytest.approx(expected_refund), \
        f"Failed for {class_type} with {entrances} entrances. Expected {expected_refund}, got {calculated}"
