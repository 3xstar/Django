from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("register/", views.signup, name="register"),
    path("logout/", views.logout, name="logout"),
    path("books/", views.books, name="books"),
    path("books/<int:book_id>/add/", views.borrow_book, name="borrow_book"),
    path(
        "my-books/<int:borrowed_book_id>/delete/",
        views.delete_borrowed_book,
        name="delete_borrowed_book",
    ),
]
