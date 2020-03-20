from django.urls import path
from . import views

app_name = 'productos'


urlpatterns = [

    path('crear/', views.crear_producto, name='crear'),
    path('ver/', views.ver_producto, name='ver_producto'),
]
