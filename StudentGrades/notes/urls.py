from django.urls import path
from . import views

urlpatterns = [
    path("", views.all_notes, name="all_notes"),
    path("login/", views.login, name="login"),
    path("profile/<str:email>/", views.profile, name="profile"),
]
