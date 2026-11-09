from django.urls import path

from . import views


urlpatterns = [
    path("", views.movie_list, name="movie_list"),
    path("movies/add/", views.add_movie, name="add_movie"),
    path("directors/add/", views.add_director, name="add_director"),
    path("genres/add/", views.add_genre, name="add_genre"),
]
