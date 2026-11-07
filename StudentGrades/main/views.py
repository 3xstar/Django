from django.http import Http404
from django.shortcuts import render, redirect

from .forms import LoginForm, RegistrationForm
from .models import Student

students_data = {
    1: {
        "name": "Захар",
        "group": "РПО",
        "grades": {"Flask": 1, "Django": 1},
    },
    2: {
        "name": "Вадим",
        "group": "РПО",
        "grades": {"Flask": 5, "Django": 5},
    },
}


def students_list1(request):
    return render(request, "grades/students_list.html", {"students": students_data})


def student_info1(request, student_id):
    student = students_data.get(student_id)
    if student is None:
        raise Http404("Student not found")

    return render(request, "grades/student_detail.html", {"student": student})


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
        form = LoginForm(request.POST)
        if form.is_valid():
            login_name = form.cleaned_data["login"]
            password = form.cleaned_data["password"]
            try:
                Student.objects.get(login=login_name, password=password)
                return redirect("student_list")
            except Student.DoesNotExist:
                form.add_error(None, "Неверный логин или пароль")
    else:
        form = LoginForm()

    return render(request, "grades/login.html", {"form": form})