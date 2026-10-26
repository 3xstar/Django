from django.urls import path
from . import views

urlpatterns = [
    path('', views.students_list, name="student_list"),
    path("student/<int:student_id>/", views.student_info, name="student_detail"),
]
