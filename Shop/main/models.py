from django.db import models

class Category(models.Model):
    name = models.CharField("Категория", max_length=100, unique=True)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField("Название", max_length=100)
    art = models.IntegerField("Артикул", unique=True)
    price = models.FloatField("Цена")
    count = models.IntegerField("Количество", default=0)

    def __str__(self):
        return f"{self.name} - {self.price}"
