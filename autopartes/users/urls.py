from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView



app_name = 'users'

urlpatterns = [
    path('signup/', views.RegisterView.as_view(), name='signup'),
    path('ver/', views.displayUsers, name='ver'),
    path('ver/rol/<int:id>/', views.changeRole, name='rol'),
    path('', views.HomeView.as_view(), name='home'),
    path(r'^logout/$', LogoutView.as_view(), name='logout'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
]
