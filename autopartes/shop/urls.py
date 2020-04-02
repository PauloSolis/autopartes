from django.urls import path
from . import views

app_name = 'shop'


urlpatterns = [

    path('ver_catalogo/', views.ver_catalogo, name='ver_catalogo'),

]
