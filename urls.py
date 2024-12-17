# accounts/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("login2/", views.login2, name="login2"),
    path("home/", views.home, name="home"),
    path("mypage/",views.mypage, name="mypage"),
    #path("login/", auth_views.LoginView.as_view(template_name='accounts/login.html'), name="login"),
]