from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView
from dashboard.views import ver_landing

app_name = 'users'

urlpatterns = [
    path('signup/', views.RegisterView.as_view(), name='signup'),
    path('ver/', views.displayUsers, name='ver'),
    path('ver/rol/<int:id>/', views.changeRole, name='rol'),
    path('index/', views.HomeView.as_view(), name='home'),
    path(r'^logout/$', LogoutView.as_view(), name='logout'),
    path('login/', views.CustomLoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('create_address/', views.create_address, name='create_address'),
    path('view_address/', views.view_address, name='view_address'),
    path('delete_address/<int:pk>/', views.delete_address, name="delete_address"),
    path('edit_address/<int:pk>/', views.edit_address, name="edit_address"),
    path('profile/edit/', views.EditView.as_view(), name='edit_profile'),
    path('', ver_landing, name='landing'),
    path('deactivate/<int:id>/', views.deactivate_profile, name='deactivateUser'),
    path('activate/<int:id>/', views.activate_profile, name='activateUser'),
]
