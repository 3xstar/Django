from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    author = forms.CharField(
        max_length=100,
        label='Автор',
        help_text='Если автора ещё нет в списке, он будет добавлен.',
        widget=forms.TextInput(attrs={'placeholder': 'Введите имя автора'}),
    )

    class Meta:
        model = Book
        fields = ('title', 'year')
        labels = {
            'title': 'Название книги',
            'year': 'Год издания',
        }

    def clean_author(self):
        author = self.cleaned_data['author'].strip()
        if not author:
            raise forms.ValidationError('Укажите имя автора.')
        return author