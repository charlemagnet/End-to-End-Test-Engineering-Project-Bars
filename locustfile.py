from locust import HttpUser, task, between
import random

class FitnessUser(HttpUser):
    # Her kullanıcı işlem yapmadan önce 1 ile 3 saniye arası beklesin (Gerçekçi olsun)
    wait_time = between(1, 3)
    
    # Kullanıcı sisteme girdiğinde ilk yapacağı iş (on_start)
    def on_start(self):
        # Önce sisteme üye olsun
        response = self.client.post("/members", json={
            "name": f"Locust User {random.randint(1, 10000)}",
            "membership_type": "Fitness"
        })
        
        if response.status_code == 201:
            self.member_id = response.json()["member_id"]
        else:
            self.member_id = None

    @task(3) # Bu görevi yapma ihtimali 3 kat daha fazla (Sık yapılan işlem)
    def check_prices(self):
        # Rastgele bir ders ve saat seçip fiyat sorsun
        classes = ["Yoga", "Boxing", "Fitness"]
        hour = random.randint(6, 23)
        class_type = random.choice(classes)
        
        self.client.get(f"/price/{class_type}/{hour}", name="/price")

    @task(1) # Bu görevi daha az yapsın
    def make_reservation(self):
        if self.member_id:
            # Rastgele rezervasyon yapmayı denesin
            self.client.post("/reservations", json={
                "member_id": self.member_id,
                "class_type": "Fitness",
                "date": "2025-06-01",
                "hour": random.randint(6, 22)
            }, name="/reservations")