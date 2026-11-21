from django.test import TestCase
from django.urls import reverse
from .forms import CourseForm
from .models import Course


class CourseFormTests(TestCase):
    def test_seats_boundaries(self):
        for seats in (0, 31):
            form = CourseForm({
                'title': 'Курс',
                'description': 'Описание',
                'seats': seats,
            })
            self.assertFalse(form.is_valid())
            self.assertIn('seats', form.errors)

        for seats in (1, 30):
            form = CourseForm({
                'title': 'Курс',
                'description': 'Описание',
                'seats': seats,
            })
            self.assertTrue(form.is_valid())

    def test_course_edit_updates_course(self):
        course = Course.objects.create(
            title='Старое название',
            description='Старое описание',
            seats=10,
        )

        response = self.client.post(
            reverse('course_edit', args=[course.pk]),
            {
                'title': 'Новое название',
                'description': 'Новое описание',
                'seats': 30,
            },
        )

        self.assertRedirects(response, reverse('course_list'))
        course.refresh_from_db()
        self.assertEqual(course.title, 'Новое название')
        self.assertEqual(course.description, 'Новое описание')
        self.assertEqual(course.seats, 30)
