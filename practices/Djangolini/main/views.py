from decimal import Decimal, ROUND_HALF_UP

from django.shortcuts import render

from .forms import DeliveryForm, PROMO_CODES
from .models import Order


MULTIPLIERS = {"standard": Decimal("1"), "express": Decimal("1.5"), "same_day": Decimal("2")}


def calculate_price(data):
    base = Decimal("300") + Decimal("30") * data["weight"]
    shipping = (base * MULTIPLIERS[data["delivery_type"]]).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    insurance = (
        (data["declared_value"] * Decimal("0.02")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        if data.get("insured") else Decimal("0")
    )
    subtotal = shipping + insurance
    discount = (subtotal * PROMO_CODES.get(data.get("promo_code"), 0) / 100).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    return {
        "shipping": shipping,
        "insurance": insurance,
        "discount": discount,
        "total": (subtotal - discount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
    }


def delivery(request):
    form = DeliveryForm(request.POST if request.method == "POST" else None)
    result = None

    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        result = calculate_price(data)
        result.update(
            origin_city=data["origin_city"].strip(),
            destination_city=data["destination_city"].strip(),
        )
        Order.objects.create(
            origin_city=data["origin_city"].strip(),
            destination_city=data["destination_city"].strip(),
            weight=data["weight"],
            delivery_type=data["delivery_type"],
            price=result["total"],
        )

    return render(request, "demo/delivery.html", {
        "form": form,
        "result": result,
        "history": Order.objects.order_by("-created_at")[:5],
    })
