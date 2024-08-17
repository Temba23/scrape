from django.urls import path
from .views import login, signout, register, home, symbol, alert

urlpatterns = [
    path('login/', login, name="login"),
    path('logout/', signout, name="logout"),
    path('register/', register, name="register"),
    # path('', home, name="home"),
    path('home/', home, name="home"),
    path('symbol/', symbol, name="symbol"),
    path('alert/', alert, name="alert")

]