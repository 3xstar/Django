from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class LoginTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="student",
            password="SecurePassword123!",
            name="Student",
            date="2000-01-01",
        )

    def test_valid_credentials_log_user_in(self):
        response = self.client.post(
            reverse("login"),
            {"username": "student", "password": "SecurePassword123!"},
        )

        self.assertRedirects(response, reverse("student_list"))
        self.assertEqual(
            str(self.client.session["_auth_user_id"]),
            str(self.user.pk),
        )

    def test_invalid_credentials_show_form_error(self):
        response = self.client.post(
            reverse("login"),
            {"username": "student", "password": "wrong-password"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_redirects_to_private_profile(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("main"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Мой профиль")
        self.assertContains(response, 'href="/static/grades/css/style.css?v=20261111-8"')

    def test_profile_shows_only_current_users_grades(self):
        from main.models import Grade

        Grade.objects.create(student=self.user, subject="Mathematics", grade=5)
        other_user = get_user_model().objects.create_user(
            username="other",
            password="SecurePassword456!",
            name="Other Student",
            date="2001-02-03",
        )
        Grade.objects.create(student=other_user, subject="Physics", grade=3)
        self.client.force_login(self.user)

        response = self.client.get(reverse("main"))

        self.assertContains(response, "Mathematics")
        self.assertNotContains(response, "Physics")

    def test_student_hub_is_separate_and_links_to_own_profile(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("student_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your student hub.")
        self.assertContains(response, reverse("main"))
        self.assertNotContains(response, "ЛИЧНЫЙ КАБИНЕТ")

    def test_registration_page_renders_styled_form_fields(self):
        response = self.client.get(reverse("registration"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="form-grid"')
        self.assertContains(response, 'id="id_password1"')
        self.assertContains(response, 'id="id_date"')

    def test_audio_player_is_available_site_wide(self):
        response = self.client.get(reverse("registration"))

        self.assertContains(response, 'id="siteAudio"')
        self.assertContains(response, 'id="audioFileInput"')
        self.assertContains(response, 'src="/static/grades/js/site-effects.js?v=20261111-1"')
