from django.urls import path
from .views import login, signout, register, home, symbol, alert, base, view_alerts, del_alerts, create_watchlist, view_watchlist

urlpatterns = [
    path('login/', login, name="login"),
    path('logout/', signout, name="logout"),
    path('register/', register, name="register"),
    path('', base, name="base"),
    path('home/', home, name="home"),
    path('symbol/', symbol, name="symbol"),
    path('alert/', alert, name="alert"),
    path('viewalerts/', view_alerts, name="view_alerts"),
    path('delalerts/', del_alerts, name="del_alerts"),
    path('watchlist/',create_watchlist, name="create_watchlist"),
    path('viewwatchlist/',view_watchlist, name="view_watchlist"),
]