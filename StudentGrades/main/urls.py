from django.urls import path
from . import views

urlpatterns = [
    path("", views.students_list1, name="student_list"),
    path("student/<int:student_id>/", views.student_info1, name="student_detail"),
    path("registration/", views.registration, name="registration"),
    path("login/", views.login, name="login"),
]
