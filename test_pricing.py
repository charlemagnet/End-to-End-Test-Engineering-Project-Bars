# test_pricing.py dosyasına ekle
from hypothesis import given, strategies as st
from pricing_engine import get_base_price, calculate_refund

@given(
    class_type=st.sampled_from(["Yoga", "Boxing", "Fitness"]),
    entrances=st.integers(min_value=0, max_value=20)
)
def test_refund_never_exceeds_base_price(class_type, entrances):
    # Kural: İade, hiçbir zaman dersin taban fiyatından fazla olmamalıdır.
    base_price = get_base_price(class_type)
    refund = calculate_refund(class_type, entrances)
    assert refund <= base_price
    assert refund >= 0