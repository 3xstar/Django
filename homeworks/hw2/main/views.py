from django.shortcuts import redirect, render
from .forms import BookForm
from .models import Author, Book


def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.author, _ = Author.objects.get_or_create(
                name=form.cleaned_data['author'].strip(),
            )
            book.save()
            return redirect('main:index')
    else:
        form = BookForm()

    return render(request, 'book_create.html', {'form': form})


def book_list(request):
    books = Book.objects.select_related('author').all()
    return render(request, 'index.html', {'books': books})
