from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Task


@login_required(login_url="/signin")
def signout(request):
    logout(request)
    HttpResponse('You have been signed out')
    print('You have been signed out')
    return redirect('signin')


@login_required(login_url="/signin")
def home(request):
    current_date = timezone.now().date()
    completed_tasks = Task.objects.filter(user=request.user, completed=True)
    pending_tasks = Task.objects.filter(user=request.user, completed=False, completion_date__gt=current_date)
    not_completed_tasks = Task.objects.filter(user=request.user, completed=False, completion_date__lte=current_date)
    print(completed_tasks)
    print(not_completed_tasks)
    print(pending_tasks)

    context = {'completed_tasks': completed_tasks,
               'not_completed_tasks': not_completed_tasks,
               'pending_tasks': pending_tasks,
               'user': request.user}

    return render(request, 'index.html', context=context)


@login_required(login_url="/signin")
def createTask(request):
    if request.method == 'POST':
        name = request.POST.get('task_name')
        date = request.POST.get('completition_date')
        tasks = Task.objects.create(
            title=name,completion_date=date, user=request.user)
        tasks.save()
        return redirect("home")
    return render(request, 'create.html', {'user': request.user})


@login_required(login_url="/signin")
def mark_as_done(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = True
    task.save()
    return redirect("home")


@login_required(login_url="/signin")
def mark_as_undone(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = False
    task.save()
    return redirect("home")


def updateTask(request, task_id):
    update_task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        name = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('completion_date')

        update_task.title = name
        update_task.description = description
        update_task.completion_date = date
        update_task.save()

        return redirect("home")
    return render(request, 'update.html', {'task': update_task, 'user': request.user})


def deleteTask(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect("home")


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            print('Login successful')
            return redirect('home')
        elif user is None:
            print('Invalid email or password')
            return redirect('signin')

    if request.user.is_authenticated:
        print('Authentication successful')
        return redirect('home')

    return render(request, 'signin.html')


def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            HttpResponse('User already exists')
            print('User already exists')
        else:
            user = User.objects.create_user(
                username=name, email=email, password=password)
            user.first_name = name
            user.save()
            print('User created', user)
            login(request, user)
            return redirect('home')

    return render(request, 'register.html')
