from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Course(models.Model):
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField()
    seats = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)])