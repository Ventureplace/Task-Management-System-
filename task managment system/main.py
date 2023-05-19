# Import required modules
from django.db import models
from django.contrib.auth.models import User

# Define models

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.IntegerField()
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# Implement user authentication and authorization using Django's built-in authentication system

# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import TaskForm

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assignee = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task/create.html', {'form': form})

# Include features like task assignment, due dates, and priority levels

# forms.py
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'due_date', 'priority', 'assignee')

# urls.py
from django.urls import path
from .views import create_task

urlpatterns = [
    path('task/create/', create_task, name='create_task'),
    # other URLs for task list, update, delete, etc.
]

# Allow users to create, update, and delete tasks

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskForm

@login_required
def task_list(request):
    tasks = Task.objects.filter(assignee=request.user)
    return render(request, 'task/list.html', {'tasks': tasks})

@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, assignee=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task/update.html', {'form': form, 'task': task})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, assignee=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'task/delete.html', {'task': task})

# Ensure you have the necessary templates (create.html, list.html, update.html, delete.html) for rendering the views.

