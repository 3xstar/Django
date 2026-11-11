from django.shortcuts import render
from .models import Task


def index(request):
    tasks = Task.objects.all().order_by('id')
    return render(request, 'main/index.html', {'tasks': tasks})