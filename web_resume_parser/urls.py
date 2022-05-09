from django.contrib import admin
from django.urls import path, include
from account import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('account/', include('account.urls')),
    path('admin/', admin.site.urls),
]
