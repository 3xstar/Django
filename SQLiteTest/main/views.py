from django.shortcuts import get_object_or_404, render, redirect
from .models import Task
from .forms import TaskForm


def all_tasks(request):
    tasks = Task.objects.all()
    return render(request, "index.html", {"tasks": tasks})


def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            status = form.cleaned_data.get("status", False)
            task = Task(title=title, status=status)
            task.save()
            return redirect("main:all_tasks")
    else:
        form = TaskForm()

    return render(request, "add_task.html", {"form": form})


def delete_task(request, id):
    task = get_object_or_404(Task, id=id)
    task.delete()
    return redirect("main:all_tasks")


def update_task(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task.title = form.cleaned_data["title"]
            task.status = form.cleaned_data["status"]
            task.save()
            return redirect("main:all_tasks")
    else:
        title = task.title
        status = task.status
        form = TaskForm(initial={"title": title, "status": status})
    return render(request, "update_task.html", {"form": form})