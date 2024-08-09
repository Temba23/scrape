from django.urls import path
from .views import login, home

urlpatterns = [
    path('login/', login, name="login"),
    path('', home, name="home"),
]