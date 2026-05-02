from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Task
from .forms import TaskForm
from accounts.forms import CustomUserCreationForm, LoginForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.utils import timezone
from accounts.models import User
from django.contrib import messages


def index(request):
    # tasks = Task.objects.all()

    context = {
        
    }

    return render(request, "index.html", context)


@login_required(login_url='login')
def dashboard(request):
    today = timezone.now().date()
    user = request.user
    # print(f"user = {user.id}")
    tasks = Task.objects.all().filter(user=user, created__date=today)

    context = {
        "tasks": tasks,
        "user": user,
    }
    # print(f"dashboard tasks = {tasks}")

    return render(request, "profile/dashboard.html", context)


@login_required(login_url='login')
def create_task(request):
    form = TaskForm()

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("dashboard")
    
    context = {
        "form": form,
    }

    return render(request, "profile/create-task.html", context)


@login_required(login_url='login')
def update_task(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
        return redirect("dashboard")
    
    context = {
        "form": form,
    }

    return render(request, "profile/update-task.html", context)


@login_required(login_url='login')
def delete_task(request, pk):
    task = Task.objects.get(id=pk)

    if request.method == "POST":
        task.delete()
        return redirect("dashboard")
    
    context = {
        "task": task,
    }

    return render(request, "profile/delete-task.html", context)


def user_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        user_error_msg = "Invalid username or password"
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = auth.authenticate(request, username=username, password=password)
            print(f"user = {user}")
            if user is not None:
                print(f"user authenticated")
                auth.login(request, user)
                return redirect("dashboard")
            else:
                messages.error(request, user_error_msg)
        else:
            messages.error(request, user_error_msg)
    else:
        form = LoginForm()
        
    context = {
        "form": form,
    }

    return render(request, "login.html", context)


def register(request):
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your registration is successful! Login now")
            return redirect("login")
    
    context = {
        "form": form,
    }

    return render(request, "register.html", context)


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect("")


@login_required(login_url='login')
def all_tasks(request):
    # today = timezone.now().date()
    user = request.user
    # print(f"user = {user.id}")
    tasks = Task.objects.all().filter(user=user).order_by("-id")

    context = {
        "tasks": tasks,
        "user": user,
    }
    # print(f"dashboard tasks = {tasks}")

    return render(request, "profile/all-tasks.html", context)


@login_required(login_url='login')
def account_settings(request):
    if request.method == "POST":
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect("dashboard")
        
    user_form = CustomUserChangeForm(instance=request.user)
    
    # today = timezone.now().date()
    # user = request.user
    # print(f"user = {user.id}")
    # tasks = Task.objects.all().filter(user=user).order_by("-id")

    context = {
        "user_form": user_form,
    }
    # print(f"dashboard tasks = {tasks}")

    return render(request, "profile/account-settings.html", context)


@login_required(login_url='login')
def delete_account(request):
    if request.method == "POST":
        del_user = User.objects.get(username=request.user.username)
        del_user.delete()
        return redirect("")
    
    context = {

    }

    return render(request, "profile/delete-account.html", context)
