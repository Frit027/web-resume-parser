from django.contrib import admin
from django.urls import path, include
from resume import views


urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('account/', include('account.urls')),
    path('analysis/', views.analysis, name='analysis'),
    path('admin/', admin.site.urls),
]
