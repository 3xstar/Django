from django.test import TestCase
from django.urls import reverse

from .models import Author, Book


class MiniLibraryTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Анна Соколова')
        self.book = Book.objects.create(
            title='Серебряный замок',
            author=self.author,
            year=1897,
        )

    def test_book_list_shows_books_and_loads_authors_efficiently(self):
        with self.assertNumQueries(1):
            response = self.client.get(reverse('main:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.title)
        self.assertContains(response, self.author.name)
        self.assertContains(response, '1897')

    def test_homepage_shows_book_list(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.title)

    def test_book_create_displays_empty_form(self):
        response = self.client.get(reverse('main:book_create'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Название книги')
        self.assertContains(response, 'Введите имя автора')
        self.assertNotContains(response, '<select')
        self.assertEqual(response.context['form'].instance.pk, None)

    def test_valid_book_create_saves_and_redirects_to_list(self):
        response = self.client.post(reverse('main:book_create'), {
            'title': 'Лунный архив',
            'author': self.author.name,
            'year': 1902,
        })

        self.assertRedirects(response, reverse('main:index'))
        self.assertTrue(Book.objects.filter(title='Лунный архив').exists())

    def test_book_create_adds_a_new_author_by_name(self):
        response = self.client.post(reverse('main:book_create'), {
            'title': 'Новая книга',
            'author': 'Новый автор',
            'year': 2024,
        })

        self.assertRedirects(response, reverse('main:index'))
        self.assertTrue(Author.objects.filter(name='Новый автор').exists())
        self.assertTrue(Book.objects.filter(title='Новая книга', author__name='Новый автор').exists())

    def test_book_create_trims_author_name(self):
        response = self.client.post(reverse('main:book_create'), {
            'title': 'Книга с пробелами',
            'author': '  Новый автор  ',
            'year': 2024,
        })

        self.assertRedirects(response, reverse('main:index'))
        self.assertTrue(Author.objects.filter(name='Новый автор').exists())

    def test_invalid_book_create_renders_errors_without_saving(self):
        response = self.client.post(reverse('main:book_create'), {
            'title': '',
            'author': self.author.name,
            'year': 'не год',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(Book.objects.count(), 1)

    def test_deleting_author_deletes_related_books(self):
        self.author.delete()

        self.assertFalse(Book.objects.filter(pk=self.book.pk).exists())
