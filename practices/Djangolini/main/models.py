from django.db import models


class Order(models.Model):
    origin_city = models.CharField(max_length=80)
    destination_city = models.CharField(max_length=80)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    delivery_type = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.origin_city} — {self.destination_city}: {self.price} ₽"
