from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.book_list, name='home'),
    path('books/', views.book_list, name='index'),
    path('books/create/', views.book_create, name='book_create'),
]
