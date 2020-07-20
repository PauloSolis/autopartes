from django.urls import path
from . import views

app_name = 'shop'


urlpatterns = [

    path('ver_catalogo/', views.ver_catalogo, name='ver_catalogo'),
    path('get_models/', views.get_models, name='get_models'),
    path('get_years/', views.get_years, name='get_years'),
    path('get_filtered/', views.get_filtered, name='get_filtered'),

]
