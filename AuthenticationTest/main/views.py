from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Book, BorrowBooks


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:login')
    else:
        form = UserCreationForm()

    return render(request, 'main/signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('main:home')
    else:
        form = AuthenticationForm()

    return render(request, 'main/login.html', {'form': form})


@require_POST
def logout(request):
    auth_logout(request)
    return redirect('main:login')


@login_required(login_url='main:login')
def home(request):
    my_books = BorrowBooks.objects.filter(reader=request.user).select_related('book')
    return render(request, 'main/home.html', {'my_books': my_books})


def books(request):
    all_books = Book.objects.order_by('title')
    my_book_ids = set()
    if request.user.is_authenticated:
        my_book_ids = set(
            BorrowBooks.objects.filter(reader=request.user).values_list('book_id', flat=True)
        )
    return render(
        request,
        'books.html',
        {'books': all_books, 'my_book_ids': my_book_ids},
    )


@login_required(login_url='main:login')
@require_POST
def borrow_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    _, created = BorrowBooks.objects.get_or_create(book=book, reader=request.user)
    if created:
        messages.success(request, f'«{book.title}» добавлена в ваши книги.')
    else:
        messages.info(request, f'«{book.title}» уже есть в ваших книгах.')
    return redirect('main:home')


@login_required(login_url='main:login')
@require_POST
def delete_borrowed_book(request, borrowed_book_id):
    borrowed_book = get_object_or_404(
        BorrowBooks, pk=borrowed_book_id, reader=request.user
    )
    borrowed_book.delete()
    messages.success(request, 'Книга удалена из ваших книг.')
    return redirect('main:home')