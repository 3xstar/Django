from django.urls import path
from .views import delivery

urlpatterns = [
    path("", delivery, name="delivery"),
    path("demo/", delivery, name="demo"),
]