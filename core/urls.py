from django.urls import path
from .views import login, signout, register, home, symbol, alert, base

urlpatterns = [
    path('login/', login, name="login"),
    path('logout/', signout, name="logout"),
    path('register/', register, name="register"),
    path('', base, name="base"),
    path('home/', home, name="home"),
    path('symbol/', symbol, name="symbol"),
    path('alert/', alert, name="alert")

]