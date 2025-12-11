import pytest
from pricing_engine import calculate_refund

def test_refund_before_two_entrances():
    # Yoga (200 TL ödenmiş olsun) -> Giriş < 2 -> %100 İade (200)
    # Yeni İmza: calculate_refund(paid_amount, attendance, class_type)
    assert calculate_refund(200, 1, "Yoga") == 200

def test_refund_after_limit_yoga():
    # Yoga (200 TL) -> Giriş 3 (Limit üstü) -> Tabloya göre %30 iade (60 TL)
    assert calculate_refund(200, 3, "Yoga") == 60

def test_refund_after_limit_boxing():
    # Boxing (120 TL) -> Giriş 5 (Limit üstü) -> Tabloya göre %50 iade (60 TL)
    assert calculate_refund(120, 5, "Boxing") == 60

def test_refund_invalid_class():
    # Geçersiz ders -> 0 iade
    assert calculate_refund(100, 1, "Karate") == 0
