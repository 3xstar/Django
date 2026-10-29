from django.contrib import admin
from django.urls import path, include
from notes import views as notes_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", notes_views.login, name="login"),
    path("", include("main.urls")),
    path("notes/", include("notes.urls")),
]
