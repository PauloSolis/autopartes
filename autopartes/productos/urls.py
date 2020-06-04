from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'productos'


urlpatterns = [

    path('crear/', views.crear_producto, name='crear'),
    path('ver/', views.ver_producto, name='ver_producto'),
    path('delete/<int:id>/', views.delete_product, name="delete_product"),
    path('editar/<int:id>/', views.edit_product, name="edit_product"),
    path('crear/categoria/', views.crear_categoria, name='crear_categoria'),
    path('crear/subcategoria/', views.create_subcategory, name='create_subcategory'),
]


