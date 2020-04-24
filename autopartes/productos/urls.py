from django.urls import path
from . import views

app_name = 'productos'


urlpatterns = [

    path('crear/', views.crear_producto, name='crear'),
    path('ver/', views.ver_producto, name='ver_producto'),
    path('delete/<int:id>/', views.delete_product, name="delete_product"),
    path('editar/<int:id>/', views.edit_product, name="edite_product"),
]
