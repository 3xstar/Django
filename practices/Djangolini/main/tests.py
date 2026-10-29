from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .forms import DeliveryForm
from .models import Order
from .views import calculate_price


def delivery_data(**overrides):
    data = {
        "sender_name": "Алексей Иванов",
        "phone": "+79991234567",
        "origin_city": "Москва",
        "destination_city": "Сочи",
        "weight": "10",
        "delivery_type": "standard",
        "terms": "on",
        "insured": "",
        "declared_value": "",
        "promo_code": "",
    }
    return data | overrides


class DeliveryFormTests(TestCase):
    def test_equal_cities_are_rejected_case_insensitively(self):
        form = DeliveryForm(delivery_data(destination_city=" мОсква "))
        self.assertFalse(form.is_valid())
        self.assertIn("destination_city", form.errors)

    def test_express_weight_limit(self):
        form = DeliveryForm(delivery_data(delivery_type="express", weight="20.01"))
        self.assertFalse(form.is_valid())
        self.assertIn("weight", form.errors)

    def test_insurance_requires_declared_value(self):
        form = DeliveryForm(delivery_data(insured="on"))
        self.assertFalse(form.is_valid())
        self.assertIn("declared_value", form.errors)

    def test_unknown_promo_code_is_rejected(self):
        form = DeliveryForm(delivery_data(promo_code="UNKNOWN"))
        self.assertFalse(form.is_valid())
        self.assertIn("promo_code", form.errors)


class DeliveryViewTests(TestCase):
    def test_prices_include_multiplier_insurance_and_discount(self):
        price = calculate_price({
            "weight": Decimal("10"),
            "delivery_type": "express",
            "insured": True,
            "declared_value": Decimal("1000"),
            "promo_code": "ISLAND10",
        })
        self.assertEqual(price["shipping"], Decimal("900.00"))
        self.assertEqual(price["insurance"], Decimal("20.00"))
        self.assertEqual(price["discount"], Decimal("92.00"))
        self.assertEqual(price["total"], Decimal("828.00"))

    def test_successful_calculation_is_shown_and_saved(self):
        response = self.client.post(reverse("delivery"), delivery_data())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "600,00 ₽")
        self.assertEqual(Order.objects.count(), 1)

    def test_invalid_submission_keeps_values_and_is_not_saved(self):
        response = self.client.post(
            reverse("delivery"),
            delivery_data(destination_city="Москва"),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Алексей Иванов")
        self.assertContains(response, "должны отличаться")
        self.assertEqual(Order.objects.count(), 0)

    def test_history_shows_only_five_recent_calculations(self):
        for number in range(6):
            self.client.post(
                reverse("delivery"),
                delivery_data(origin_city=f"Город {number}"),
            )
        self.assertEqual(Order.objects.count(), 6)
        response = self.client.get(reverse("delivery"))
        self.assertEqual(len(response.context["history"]), 5)
        self.assertNotContains(response, "Алексей Иванов")
