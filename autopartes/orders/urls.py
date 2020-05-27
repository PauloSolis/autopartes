from django.urls import path
from . import views

app_name = 'orders'


urlpatterns = [

    path('ver_ordenes/', views.ver_ordenes, name='ver_ordenes'),
    path('ver_desgloce/<int:id>/', views.ver_desgloce, name='ver_desgloce'),
    path('store_order/', views.crear_orden, name="crear_orden"),
]
