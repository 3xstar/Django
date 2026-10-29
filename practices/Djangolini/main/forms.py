from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


PROMO_CODES = {"TROPIC5": 5, "ISLAND10": 10, "SUN15": 15}


class DeliveryForm(forms.Form):
    sender_name = forms.CharField(label="ФИО отправителя", max_length=120, min_length=2)
    phone = forms.CharField(
        label="Телефон",
        validators=[RegexValidator(r"^\+?[0-9\s()-]{10,20}$", "Введите корректный номер телефона.")],
        widget=forms.TextInput(attrs={"autocomplete": "tel"}),
    )
    origin_city = forms.CharField(label="Город отправки", max_length=80)
    destination_city = forms.CharField(label="Город получения", max_length=80)
    weight = forms.DecimalField(
        label="Вес, кг",
        min_value=0.1,
        max_value=100,
        max_digits=5,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"min": "0.1", "max": "100", "step": "0.1"}),
    )
    delivery_type = forms.ChoiceField(
        label="Тип доставки",
        choices=[
            ("standard", "Стандартная"),
            ("express", "Экспресс"),
            ("same_day", "В тот же день"),
        ],
    )
    terms = forms.BooleanField(label="Согласен с условиями")
    insured = forms.BooleanField(label="Застраховать посылку", required=False)
    declared_value = forms.DecimalField(
        label="Объявленная стоимость, ₽",
        min_value=0.01,
        max_value=10000000,
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={"min": "0.01", "step": "0.01"}),
    )
    promo_code = forms.CharField(
        label="Промокод",
        max_length=20,
        required=False,
        help_text="TROPIC5, ISLAND10 или SUN15 — скидка 5–15%.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = (
                "check-control" if isinstance(field, forms.BooleanField) else "control"
            )

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if not 10 <= sum(char.isdigit() for char in phone) <= 15:
            raise ValidationError("Номер должен содержать от 10 до 15 цифр.")
        return phone

    def clean_promo_code(self):
        code = self.cleaned_data["promo_code"].upper()
        if code and code not in PROMO_CODES:
            raise ValidationError("Промокод не найден.")
        return code

    def clean(self):
        cleaned = super().clean()
        origin = cleaned.get("origin_city", "").strip()
        destination = cleaned.get("destination_city", "").strip()
        if origin and destination and origin.casefold() == destination.casefold():
            self.add_error("destination_city", "Города отправки и получения должны отличаться.")
        if cleaned.get("delivery_type") == "express" and cleaned.get("weight", 0) > 20:
            self.add_error("weight", "Для экспресс-доставки вес не может превышать 20 кг.")
        if cleaned.get("insured") and not cleaned.get("declared_value"):
            self.add_error("declared_value", "Укажите объявленную стоимость для страховки.")
        return cleaned
