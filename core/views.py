from django.shortcuts import render, HttpResponse, redirect
from .forms import LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


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
    
    
def home(request):
    pass