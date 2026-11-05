from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100, blank=False)
    author = models.CharField(max_length=100, default="anonim")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment")
    author = models.CharField(max_length=100, default="anonim")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)