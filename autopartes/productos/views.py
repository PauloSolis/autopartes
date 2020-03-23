from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Product
from .forms import Products
from django.db import DatabaseError
from django.utils import timezone
from django.views.generic.edit import UpdateView

STATUS_SAVED = 'SAVED'
STATUS_ERROR = 'ERROR'


def crear_producto(request):
    if request.method == 'POST':
        form = Products(request.POST)
        context = {
            'form': form,
        }
        if form.is_valid():
            try:
                new_product = Product(
                    codigo=form.cleaned_data.get('codigo'),
                    nombre=form.cleaned_data.get('nombre'),
                    descripcion=form.cleaned_data.get('descripcion'),
                    marca=form.cleaned_data.get('marca'),
                    modelo_coche=form.cleaned_data.get('modelo_coche'),
                    precio_minorista=form.cleaned_data.get('precio_minorista'),
                    precio_mayorista1=(form.cleaned_data.get('precio_minorista') * .97),
                    precio_mayorista2=(form.cleaned_data.get('precio_minorista') * .95),
                    precio_mayorista3=(form.cleaned_data.get('precio_minorista') * .92),
                )
                new_product.save()
                messages.success(request, 'Se guardo correctamente el nuevo producto')
                return render(request, '../templates/productos/ver_producto.html', context)
            except DatabaseError:
                messages.error(request, 'Error')
                return render(request, '../templates/productos/crear_producto.html')
    else:
        form = Products()
        context = {
            'form': form,
        }
        return render(request, '../templates/productos/crear_producto.html', context)


def ver_producto(request):
    products = Product.objects.all();
    paginator = Paginator(products, 20);
    return render(request, '../templates/productos/ver_producto.html')
