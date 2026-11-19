from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.store, name="store"),
    path("store/", views.store, name="store_alias"),
]
