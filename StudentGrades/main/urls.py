from django.urls import path
from . import views

urlpatterns = [
    path("registration/", views.registration, name="registration"),
    path("login/", views.login, name="login"),
    path("", views.student_list, name="student_list"),
    path("main/", views.main, name="main"),
]
