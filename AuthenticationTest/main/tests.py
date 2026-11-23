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
