from django.shortcuts import redirect, render

from .forms import DirectorForm, GenreForm, MovieForm
from .models import Director, Genre, Movie


def movie_list(request):
    movies = Movie.objects.select_related("director", "genre")

    genre_id = request.GET.get("genre")
    director_id = request.GET.get("director")
    search_query = request.GET.get("q", "").strip()

    if genre_id:
        movies = movies.filter(genre_id=genre_id)
    if director_id:
        movies = movies.filter(director_id=director_id)
    if search_query:
        movies = movies.filter(title__icontains=search_query)

    sort_options = {
        "title": "title",
        "year": "year",
        "-year": "-year",
        "-rating": "-rating",
        "duration": "duration_minutes",
    }
    selected_sort = request.GET.get("sort", "title")

    context = {
        "movies": movies.order_by(sort_options.get(selected_sort, "title"), "title"),
        "genres": Genre.objects.order_by("name"),
        "directors": Director.objects.order_by("name"),
        "selected_genre": genre_id or "",
        "selected_director": director_id or "",
        "search_query": search_query,
        "selected_sort": selected_sort,
    }
    return render(request, "main/movie_list.html", context)


def add_movie(request):
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("movie_list")
    else:
        form = MovieForm()

    return render(request, "main/form.html", {
        "form": form,
        "title": "Добавить фильм",
    })


def add_director(request):
    if request.method == "POST":
        form = DirectorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("movie_list")
    else:
        form = DirectorForm()

    return render(request, "main/form.html", {
        "form": form,
        "title": "Добавить режиссёра",
    })


def add_genre(request):
    if request.method == "POST":
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("movie_list")
    else:
        form = GenreForm()

    return render(request, "main/form.html", {
        "form": form,
        "title": "Добавить жанр",
    })
