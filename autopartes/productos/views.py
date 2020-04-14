from django.contrib import messages
from django.core.paginator import Paginator
from django.db import DatabaseError
from django.shortcuts import render, redirect
from django.http import HttpResponse

from users.decorators import admin_required
from .forms import Products
from .models import Product

STATUS_SAVED = 'SAVED'
STATUS_ERROR = 'ERROR'


@admin_required
def crear_producto(request):
    if request.method == 'POST':
        form = Products(request.POST, request.FILES)

        if form.is_valid():
            print("entre al is valid")
            form.save()
            messages.success(request, 'Se guardo correctamente el nuevo producto')
            return HttpResponse("/productos/ver/")
        else:
            form.save()
            return redirect("productos:ver_producto")
    else:
        form = Products()
        context = {
            'form': form,
        }
        return render(request, '../templates/productos/crear_producto.html', context)




@admin_required
def ver_producto(request):
    products = Product.objects.all().order_by('-id')
    paginator = Paginator(products, 20)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, '../templates/productos/ver_producto.html', {'products': page_obj})


@admin_required
def delete_product(request, id):
    Product.objects.get(id=id).delete()
    messages.success(request, 'Se ha eliminado correctamente el producto')
    return redirect('productos:ver_producto')
