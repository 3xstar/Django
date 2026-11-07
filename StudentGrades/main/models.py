from typing import cast

from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    login = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    grade = models.FloatField()