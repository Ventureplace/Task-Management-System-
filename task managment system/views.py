from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .models import Task

@login_required
def task_list(request):
    tasks = Task.objects.filter(assignee=request.user)
    filter_by = request.GET.get('filter')
    if filter_by == 'completed':
        tasks = tasks.filter(completed=True)
    elif filter_by == 'pending':
        tasks = tasks.filter(completed=False)
    return render(request, 'task/list.html', {'tasks': tasks})

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

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout(request):
    logout(request)
    return redirect('task_list')
