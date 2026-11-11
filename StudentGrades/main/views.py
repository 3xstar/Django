from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login

from .forms import LoginForm, RegistrationForm
from .models import Student


def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegistrationForm()

    return render(request, "grades/registration.html", {"form": form})


def login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("student_list")
    else:
        form = LoginForm(request)

    return render(request, "grades/login.html", {"form": form})


@login_required
def main(request):
    grades = list(request.user.grade_set.all())
    grade_average = (
        round(sum(grade.grade for grade in grades) / len(grades), 1)
        if grades
        else None
    )
    return render(
        request,
        "grades/main.html",
        {
            "grades": grades,
            "grade_count": len(grades),
            "grade_average": grade_average,
        },
    )


@login_required
def student_list(request):
    students = Student.objects.prefetch_related("grade_set").order_by(
        "name", "username"
    )
    return render(request, "grades/students_list.html", {"students": students})