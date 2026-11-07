from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100, blank=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    year = models.IntegerField(blank=False)

    def __str__(self):
        return self.title