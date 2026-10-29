from django.shortcuts import render
from django.contrib import messages
from . import forms


notes = {
}


def index(request):
    return render(request, "main/index.html")


def login(request):
    form = forms.LoginForm(request.POST if request.method == "POST" else None)

    if request.method == "POST" and form.is_valid():
        return render(
            request,
            "notes/profile.html",
            {"email": form.cleaned_data["email_field"]},
        )

    return render(request, "notes/login.html", {"form": form})


def all_notes(request):
    form = forms.Note()

    if request.method == "POST":
        form = forms.Note(request.POST)
        name = form["name"].data
        text = form["text"].data
        notes[name] = text
        messages.success(request, "Your note has been added!")

    return render(request, "notes/indexform.html", {"notes":notes, "form":form})
    # if request.method == "POST":
    #     note = request.POST.get("note")
    #     notes[list(notes.keys())[-1] + 1] = str(note)
    # return render(request, "notes/index.html", {"notes":notes})

def profile(request, email):
    return render(request, "notes/profile.html", {"email":email})