from django.db import models

class Category(models.Model):
    name = models.CharField("название", max_length=100, unique=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)

    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.title