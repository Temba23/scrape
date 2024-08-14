from django.shortcuts import render, HttpResponse, redirect
from .forms import LoginForm, RegisterForm
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
    driver.get("https://www.sharesansar.com/today-share-price")

    time.sleep(5)

    rows = driver.find_elements(By.ID, 'headFixed_wrapper')
    time.sleep(5)
    # columns = driver.find_elements(By.CLASS_NAME, 'sorting')
    # for i in columns:
    #     print(i.text)

    # print("hello")
    stock_data = []

    for row in rows:
        columns= row.find_elements(By.TAG_NAME, 'tr')
        
        if columns:
            # Extract data for each column
            sn = columns[0].text
            company_name = columns[1].text
            no_of_transactions = columns[2].text
            max_price = columns[3].text
            min_price = columns[4].text
            closing_price = columns[5].text
            traded_shares = columns[6].text
            amount = columns[7].text
            previous_closing = columns[8].text

            # Store the data in a dictionary
            stock = {
                'SN': sn,
                'Company': company_name,
                'Transactions': no_of_transactions,
                'Max_Price': max_price,
                'Min_Price': min_price,
                'Closing_Price': closing_price,
                'Traded_Shares': traded_shares,
                'Amount': amount,
                'Previous_Closing': previous_closing,
            }

            # Append the stock data to the list
            stock_data.append(stock)

    # Close the WebDriver
    driver.quit()
    print(stock_data)
    # Render the scraped data to the template
    context = {
        'stock_data': stock_data,
    }

    return render(request, 'home.html', context)


def symbol(request):
    driver.get("https://www.sharesansar.com/today-share-price")
    search = driver.find_element(By.ID, 'company_search')
    search.send_keys("MFIL")
    time.sleep(4)
    search.send_keys(Keys.RETURN)
    company_price = driver.find_element(By.CLASS_NAME, 'comp-price')
    price = company_price.text
    print(price)
    return HttpResponse("DOne")


