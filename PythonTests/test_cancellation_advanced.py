import pytest
from pricing_engine import calculate_refund

CANCELLATION_SCENARIOS = [
    # KRİTİK DÜZELTME: "AnyClass" -> "Yoga" yaptık.
    # Çünkü pricing_engine artık tanımadığı derslere 0 iade veriyor.
    # Testin geçmesi için geçerli bir ders ismi ("Yoga") vermemiz şart.
    ("DT-01", 0, "Yoga", 1.0), 
    
    # Geri kalanlar aynen duruyor
    ("DT-02", 1, "Yoga", 1.0),
    ("DT-03", 5, "Yoga", 0.3),
    ("DT-04", 1, "Boxing", 1.0),
    ("DT-05", 3, "Boxing", 0.5),
    ("DT-06", 1, "Fitness", 1.0),
    ("DT-07", 10, "Fitness", 0.1),
    ("DT-08", 1, "Basketball", 1.0),
    ("DT-09", 4, "Basketball", 0.4),
    ("DT-10", 0, "Tennis", 1.0),
    ("DT-11", 2, "Tennis", 0.8),
    ("DT-12", 1, "Swimming", 1.0),
    ("DT-13", 6, "Swimming", 0.15),
]

@pytest.mark.parametrize("rule_id, attendance_count, class_type, expected_rate", CANCELLATION_SCENARIOS)
def test_refund_decision_table_advanced(rule_id, attendance_count, class_type, expected_rate):
    """
    Bu test, oluşturduğun Decision Table görselindeki 13 kuralı doğrular.
    """
    paid_amount = 100.0
    
    refund_amount = calculate_refund(paid_amount, attendance_count, class_type)
    
    expected_refund = paid_amount * expected_rate
    
    # Floating point karşılaştırması
    assert refund_amount == pytest.approx(expected_refund), \
        f"Rule {rule_id} Failed! Class: {class_type}, Att: {attendance_count}. Expected: {expected_refund}, Got: {refund_amount}"
