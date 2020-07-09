from django.urls import path
from . import views

app_name = 'dashboard'


urlpatterns = [

    path('catalogo/', views.ver_catalogo, name='catalogo'),
    path('nosotros/', views.about_us, name='nosotros'),
]
