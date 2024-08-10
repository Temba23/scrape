from django.shortcuts import render, HttpResponse, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(username, password)
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect("home")
            else:
                messages.error(request, "Invalid email or password. Please try again.")
        else:
            messages.error(request, "Form is invalid. Please correct the errors below.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def signout(request):
    logout(request)
    messages.success(request, "Logout Successfull.")
    return redirect("login")

def home(request):
    pass

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                messages.error(request, f"User already exists with {email}. Please use another one.")
            else:
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                if password == form.cleaned_data['password2']:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    messages.success(request, f"Account created successfully for {username}.")
                    return redirect('login')
                else:
                    messages.error(request, "Passwords don't match.")
        else:
            messages.error(request, "Form is invalid. Please correct the errors below.")
            return redirect("register")
    
    else:
        form = RegisterForm()
        return render(request, "register.html", {"form":form})
