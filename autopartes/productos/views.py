from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import DatabaseError
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from users.decorators import admin_required
from .forms import Products
from .models import Product

STATUS_SAVED = 'SAVED'
STATUS_ERROR = 'ERROR'



@login_required
@admin_required
def crear_producto(request):
    if request.method == 'POST':
        form = Products(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se guardo correctamente el nuevo producto')
            return HttpResponseRedirect("/productos/ver/")
        else:

            return redirect("productos:ver_producto")
    else:
        form = Products()
        context = {
            'form': form,
        }
        return render(request, '../templates/productos/crear_producto.html', context)



@login_required
@admin_required
def ver_producto(request):
    products = Product.objects.all().order_by('-id')
    paginator = Paginator(products, 20)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, '../templates/productos/ver_producto.html', {'products': page_obj})


@login_required
@admin_required
def delete_product(request, id):
    Product.objects.get(id=id).delete()
    messages.success(request, 'Se ha eliminado correctamente el producto')
    return redirect('productos:ver_producto')
