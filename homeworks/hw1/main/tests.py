from django.test import TestCase


class ScheduleTests(TestCase):
    def test_homepage_shows_weekly_schedule_and_defaults_to_today(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Class schedule")
        self.assertContains(response, "Monday")
        self.assertContains(response, "href=\"?day=monday\"")
        self.assertContains(response, "css/style.css")

    def test_weekday_selection_shows_its_classes(self):
        response = self.client.get("/", {"day": "thursday"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django workshop")
        self.assertContains(response, "Git &amp; teamwork")
        self.assertContains(response, "3 classes")

    def test_weekend_has_a_friendly_empty_state(self):
        response = self.client.get("/", {"day": "saturday"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No classes today.")
        self.assertContains(response, "See Monday")
        self.assertContains(response, "0 classes")

    def test_invalid_day_falls_back_to_today(self):
        response = self.client.get("/", {"day": "not-a-day"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Class schedule")
