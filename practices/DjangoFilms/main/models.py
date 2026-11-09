from django.db import models


class Director(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)


class Genre(models.Model):
    name = models.CharField(max_length=200, unique=True)


class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    rating = models.IntegerField()
    duration_minutes = models.IntegerField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name="movies")
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, related_name="movies")