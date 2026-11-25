from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} - {self.author}"


class BorrowBooks(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reader = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.book.title