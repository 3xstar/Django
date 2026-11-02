from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.all_tasks, name='index'),
    path('', views.all_tasks, name='all_tasks'),
    path('task/add_task/', views.add_task, name='add_task'),
    path('task/delete_task/<int:id>/', views.delete_task, name='delete_task'),
    path('task/update_task/<int:id>/', views.update_task, name='update_task'),
]