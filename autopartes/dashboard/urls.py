from django.urls import path
from . import views

app_name = 'dashboard'


urlpatterns = [

    path('catalogo/', views.ver_catalogo, name='catalogo'),
    path('landing/', views.ver_landing, name='landing'),

]
