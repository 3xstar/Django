from django.test import TestCase
from django.urls import reverse


class AuthenticationViewTests(TestCase):
    def test_signup_redirects_to_login(self):
        response = self.client.post(
            reverse("main:register"),
            {
                "username": "newuser",
                "password1": "StrongPass!934",
                "password2": "StrongPass!934",
            },
        )

        self.assertRedirects(response, reverse("main:login"))

    def test_login_redirects_to_home(self):
        from django.contrib.auth.models import User

        User.objects.create_user(username="existinguser", password="StrongPass!934")

        response = self.client.post(
            reverse("main:login"),
            {"username": "existinguser", "password": "StrongPass!934"},
        )

        self.assertRedirects(response, reverse("main:home"))

    def test_home_redirects_anonymous_user_to_login(self):
        response = self.client.get(reverse("main:home"))

        self.assertRedirects(
            response,
            f"{reverse('main:login')}?next={reverse('main:home')}",
        )

    def test_home_displays_logout_button(self):
        from django.contrib.auth.models import User

        user = User.objects.create_user(username="homeuser", password="StrongPass!934")
        self.client.force_login(user)

        response = self.client.get(reverse("main:home"))

        self.assertContains(response, f'action="{reverse("main:logout")}"')
        self.assertContains(response, "Выйти")

    def test_logout_redirects_to_login(self):
        from django.contrib.auth.models import User

        user = User.objects.create_user(username="logoutuser", password="StrongPass!934")
        self.client.force_login(user)

        self.assertEqual(self.client.get(reverse("main:logout")).status_code, 405)

        response = self.client.post(reverse("main:logout"))

        self.assertRedirects(response, reverse("main:login"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_home_displays_users_borrowed_books(self):
        from django.contrib.auth.models import User
        from main.models import Book, BorrowBooks

        user = User.objects.create_user(username="reader", password="StrongPass!934")
        book = Book.objects.create(title="Example Book", author="Example Author")
        borrowed_book = BorrowBooks.objects.create(book=book, reader=user)
        self.client.force_login(user)

        response = self.client.get(reverse("main:home"))

        self.assertContains(response, user.username)
        self.assertContains(response, book.title)
        self.assertContains(response, book.author)
        self.assertContains(response, "Убрать из списка")
        self.assertContains(
            response,
            f'action="{reverse("main:delete_borrowed_book", args=[borrowed_book.id])}"',
        )

    def test_delete_borrowed_book_only_deletes_current_users_record(self):
        from django.contrib.auth.models import User
        from main.models import Book, BorrowBooks

        user = User.objects.create_user(username="reader", password="StrongPass!934")
        another_user = User.objects.create_user(
            username="anotherreader", password="StrongPass!934"
        )
        book = Book.objects.create(title="Example Book", author="Example Author")
        own_record = BorrowBooks.objects.create(book=book, reader=user)
        another_users_record = BorrowBooks.objects.create(book=book, reader=another_user)
        self.client.force_login(user)

        response = self.client.post(
            reverse(
                "main:delete_borrowed_book",
                args=[another_users_record.id],
            )
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(BorrowBooks.objects.filter(pk=another_users_record.id).exists())

        response = self.client.post(
            reverse("main:delete_borrowed_book", args=[own_record.id])
        )

        self.assertRedirects(response, reverse("main:home"))
        self.assertFalse(BorrowBooks.objects.filter(pk=own_record.id).exists())

    def test_catalog_adds_book_once_to_current_users_list(self):
        from django.contrib.auth.models import User
        from main.models import Book, BorrowBooks

        user = User.objects.create_user(username="reader", password="StrongPass!934")
        book = Book.objects.create(title="Example Book", author="Example Author")
        self.client.force_login(user)

        catalog_response = self.client.get(reverse("main:books"))

        self.assertContains(catalog_response, book.title)
        self.assertContains(
            catalog_response,
            f'action="{reverse("main:borrow_book", args=[book.id])}"',
        )

        response = self.client.post(reverse("main:borrow_book", args=[book.id]))

        self.assertRedirects(response, reverse("main:home"))
        self.assertEqual(
            BorrowBooks.objects.filter(reader=user, book=book).count(),
            1,
        )

        self.client.post(reverse("main:borrow_book", args=[book.id]))

        self.assertEqual(
            BorrowBooks.objects.filter(reader=user, book=book).count(),
            1,
        )
        self.assertContains(self.client.get(reverse("main:books")), "Уже на вашей полке")
