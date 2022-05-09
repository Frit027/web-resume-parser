from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import CustomLoginForm
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(authentication_form=CustomLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout-then-login/', auth_views.logout_then_login, name='logout_then_login'),

    path('password-change/', views.PasswordsChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('register/', views.register, name='register'),
]
