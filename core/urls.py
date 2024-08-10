from django.urls import path
from .views import login, signout, register, home

urlpatterns = [
    path('login/', login, name="login"),
    path('logout/', signout, name="logout"),
    path('register/', register, name="register"),
    path('', home, name="home"),
]