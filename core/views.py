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
from django.contrib.auth.decorators import login_required

from .models import Alert, Scrip

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


@login_required
def home(request):
    user = request.user
    driver = webdriver.Chrome()

    driver.get("https://www.sharesansar.com/today-share-price")
    time.sleep(2)

    table = driver.find_element(By.ID, 'headFixed')    
    rows = table.find_elements(By.TAG_NAME, 'tr')
    taken_date = driver.find_element(By.XPATH, '//*[@id="todayshareprice_data"]/h5/span')
    date = taken_date.text
    
    stock_data = []
    user_alerts = Alert.objects.filter(user=user)

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

            for alert in user_alerts:
                if alert.scrip.scrip == company_name:
                    alert.today = int(closing_price.replace(',', ''))
                    alert.save()
                
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
        'date' : date
    }

    return render(request, 'home.html', context)

@login_required
def symbol(request):
    if request.method == "POST":
        form = SymbolForm(request.POST)
        if form.is_valid():
            scrip = form.cleaned_data['symbol']
            scrip_data, created = Scrip.objects.get_or_create(scrip=scrip)
            scrip_data.save()
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
                messages.success(request, f"The price of {scrip} is {price} on {date}.")
                return redirect('symbol')
            except Exception as e:
                messages.error(f"{e} occured.")
            finally:
                driver.quit()
        else:
            return HttpResponse("Form Invalid.")
    
    else:
        form = SymbolForm()
        return render(request, "symbol.html", {"form":form})
        
@login_required
def alert(request):
    if request.method == "POST":
        form = AlertForm(request.POST)
        if form.is_valid():
            scrip = form.cleaned_data['scrip']
            target = form.cleaned_data['alert_on']
            user = request.user
            try:
                driver.get("https://www.sharesansar.com/today-share-price")
                search = driver.find_element(By.ID, 'company_search')
                search.send_keys(f'{scrip}')
                time.sleep(5)
                search.send_keys(Keys.RETURN)

                company_price = driver.find_element(By.CLASS_NAME, 'comp-price')
                price = company_price.text
                alert, created = Alert.objects.get_or_create(
                    user=user, 
                    scrip=scrip, 
                    alert_on=target, 
                    today= price
                )
                if created:
                    messages.success(request, f"The alert for {scrip} is set to {target}.")
                else:
                    messages.info(request, f"Alert for {scrip} already exists.")

                return redirect('alert')

            except Exception as e:
                messages.error(request, f"An error occurred: {e}")

            finally:
                driver.quit()
            
        else:
            messages.error(request, "Form is invalid. Please correct the errors.")

    else:
        form = AlertForm()

    return render(request, "alert.html", {"form": form})

@login_required
def base(request):
    return render(request, "dash.html")

def watchlist(request):
    if request.method=="GET":
        user = request.user
        alert = Alert.objects.filter(user=user.id)
        try:
            context = {
                "user" : request.user,
                "scrip" : alert.scrip.scrip,
                "alert_on" : alert.alert_on,
                "today" : alert.today
            }
            return render(request, "watchlist.html", context=context)
        except Alert.DoesNotExist:
            messages.error(f'No watchlist for {user}') 
            return redirect('watchlist')
    else:
        messages.error("Method Not Allowed.")
        return redirect('watchlist')
    
def del_watchlist(request):
    if request.method == "POST":
        form = SymbolForm(request.POST)
        if form.is_valid():
            scrip = form.cleaned_data['symbol']

            req_scrip = Scrip.objects.filter(scrip=scrip).first()
            if not req_scrip:
                messages.error(request, f"{scrip} does not exist.")
                return redirect('del_watchlist')

            d_scrip = Alert.objects.filter(scrip=req_scrip, user=request.user).first()
            if d_scrip:
                d_scrip.delete()
                messages.success(request, f"{scrip} deleted successfully.")
            else:
                messages.error(request, f"{scrip} does not exist in your watchlist.")

            return redirect('del_watchlist')

        else:
            messages.error(request, "Form is invalid.")
            return redirect('del_watchlist')

    else:
        form = SymbolForm()
        return render(request, "symbol.html", {"form": form})

