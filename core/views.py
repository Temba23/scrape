from django.shortcuts import render, HttpResponse, redirect
from .forms import LoginForm, RegisterForm, SymbolForm, AlertForm
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .models import Alert

PATH = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome()

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
    driver = webdriver.Chrome()

    driver.get("https://www.sharesansar.com/today-share-price")
    time.sleep(2)

    table = driver.find_element(By.ID, 'headFixed')    
    rows = table.find_elements(By.TAG_NAME, 'tr')
    
    stock_data = []

    for row in rows[1:]:
        columns = row.find_elements(By.TAG_NAME, 'td')
        
        if len(columns) >= 9: 
            sn = columns[0].text
            company_name = columns[1].text
            open = columns[3].text
            max_price = columns[4].text
            min_price = columns[5].text
            closing_price = columns[6].text
            traded_shares = columns[8].text
            previous_closing = columns[9].text

            stock = {
                'SN': sn,
                'Company': company_name,
                'Open': open,
                'Max_Price': max_price,
                'Min_Price': min_price,
                'Closing_Price': closing_price,
                'Traded_Shares': traded_shares,
                'Previous_Closing': previous_closing,
            }
            stock_data.append(stock)

    driver.quit()

    context = {
        'stock_data': stock_data,
    }

    return render(request, 'home.html', context)


def symbol(request):
    if request.method == "POST":
        form = SymbolForm(request.POST)
        if form.is_valid():
            scrip = form.cleaned_data['symbol']
            try:
                driver.get("https://www.sharesansar.com/today-share-price")
                search = driver.find_element(By.ID, 'company_search')
                search.send_keys(f"{scrip}")
                time.sleep(4)
                search.send_keys(Keys.RETURN)
                company_price = driver.find_element(By.CLASS_NAME, 'comp-price')
                price = company_price.text
                messages.success(request, f"The price of {scrip} is {price}.")
                return redirect('symbol')
            except Exception as e:
                messages.error(f"{e} occured.")
        else:
            return HttpResponse("Form Invalid.")
    
    else:
        form = SymbolForm()
        return render(request, "symbol.html", {"form":form})
        

def alert(request):
    if request.method == "POST":
        form = AlertForm(request.POST)
        if form.is_valid():
            scrip = form.cleaned_data['symbol']
            target = form.cleaned_data['target']
            try:
                driver.get("https://www.sharesansar.com/today-share-price")
                search = driver.find_element(By.ID, 'company_search')
                search.send_keys(f"{scrip}")
                time.sleep(4)
                search.send_keys(Keys.RETURN)
                company_price = driver.find_element(By.CLASS_NAME, 'comp-price')
                price = company_price.text

                taken_date = driver.find_element(By.CLASS_NAME, 'comp-ason')
                date = taken_date.text
                user = request.user

                alert = Alert.objects.get_or_create(user=user, scrip=scrip, alert_on=target, date=date, today=price)
                alert.save()
                messages.success(request, f"The alert for {scrip} is set to {target}.")
                return redirect('alert')
            except Exception as e:
                messages.error(f"{e} occured.")
        else:
            return HttpResponse("Form Invalid.")
    
    else:
        form = AlertForm()
        return render(request, "alert.html", {"form":form})
