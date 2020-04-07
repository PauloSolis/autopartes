from django.urls import path,include
from . import views

app_name = 'users'


urlpatterns = [
    path('crear/', views.RegisterView.as_view(), name='crear'),
    path('ver/', views.displayUsers, name='ver'),
    path('', views.HomeView.as_view(), name='home'),


    ]