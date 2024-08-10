from django.shortcuts import render, HttpResponse, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect("home")
            else:
                return HttpResponse("Error")

    else:
        forms = LoginForm()
        return render(request, 'login.html', {'form':forms})

def logout(request):
    logout(request)
    return HttpResponse("Logout Successfull.")

def home(request):
    pass

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                return HttpResponse(f"User already exists with {email}. Please another one.")
            else:
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                if password==password2:
                    user = User.objects.create(username=username, email=email, password=password)
                    user.save()
                    return redirect('login')
                else:
                    return HttpResponse("Passwords dont match to each other.")
        else:
            return HttpResponse("Form Invalid.")
    
    else:
        form = RegisterForm()
        return render(request, "register.html", {"form":form})
