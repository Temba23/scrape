from django.urls import path
from .views import login, signout, register, home, symbol, alert, base, view_alerts, del_alerts

urlpatterns = [
    path('login/', login, name="login"),
    path('logout/', signout, name="logout"),
    path('register/', register, name="register"),
    path('', base, name="base"),
    path('home/', home, name="home"),
    path('symbol/', symbol, name="symbol"),
    path('alert/', alert, name="alert"),
    path('watchlist/', view_alerts, name="view_alerts"),
    path('del_watchlist/', del_alerts, name="del_alerts"),
]