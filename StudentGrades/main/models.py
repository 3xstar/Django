from django.db import models
from django.contrib.auth.models import AbstractUser

class Student(AbstractUser):
    name = models.CharField(max_length=200)
    date = models.DateField()

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    grade = models.FloatField()