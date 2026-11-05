from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path("add_post/", views.add_post, name="add_post"),
    path("post_info/<int:post_id>/", views.post_info, name="post_info"),
    path("post_delete/<int:post_id>/", views.post_delete, name="post_delete"),
]