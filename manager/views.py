from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.db.models import Count
from django.utils import timezone


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')

@login_required
def dashboard(request):
    total_tasks = Task.objects.filter(user=request.user).count()
    completed_tasks = Task.objects.filter(user=request.user, completion_status=True).count()
    overdue_tasks = Task.objects.filter(user=request.user, due_date__lt=timezone.now().date(), completion_status=False).count()
    tasks_due_soon = Task.objects.filter(user=request.user, due_date__range=[timezone.now().date(), (timezone.now() + timezone.timedelta(days=7)).date()]).count()
    task_completion_rate = completed_tasks / total_tasks * 100 if total_tasks > 0 else 0

    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'overdue_tasks': overdue_tasks,
        'tasks_due_soon': tasks_due_soon,
        'task_completion_rate': task_completion_rate,
    }
    return render(request, 'dashboard.html', context)


