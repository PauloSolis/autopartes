from django.urls import path
from . import views

app_name = 'users'


urlpatterns = [
    path('crear/', views.RegisterView.as_view(), name='crear'),
    path('ver/', views.displayUsers, name='ver')
    ]