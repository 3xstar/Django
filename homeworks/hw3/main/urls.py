from django.urls import path
from . import views


urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<int:course_id>/edit/', views.course_edit, name='course_edit'),
]
