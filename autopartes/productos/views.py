from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Product
from .forms import Products
from django.db import DatabaseError
from django.contrib.auth.decorators import login_required
from users.decorators import admin_required, retailer_required, wholesaler_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.generic.edit import UpdateView

STATUS_SAVED = 'SAVED'
STATUS_ERROR = 'ERROR'

@admin_required
def crear_producto(request):
    if request.method == 'POST':
        form = Products(request.POST)
        context = {
            'form': form,
        }
        if form.is_valid():
            try:
                new_product = Product(
                    original_code=form.cleaned_data.get('original_code'),
                    product_code=form.cleaned_data.get('product_code'),
                    name=form.cleaned_data.get('name'),
                    description=form.cleaned_data.get('description'),
                    car_brand=form.cleaned_data.get('car_brand'),
                    car_model=form.cleaned_data.get('car_model'),
                    car_year=form.cleaned_data.get('car_year'),
                    public_price=form.cleaned_data.get('public_price'),
                    card_price=form.cleaned_data.get('card_price'),
                    master_price=form.cleaned_data.get('master_price'),
                    wholesale_price=form.cleaned_data.get('wholesale_price'),
                    dozen_price=form.cleaned_data.get('dozen_price'),
                )
                new_product.save()
                messages.success(request, 'Se guardo correctamente el nuevo producto')
                return redirect('productos:ver_producto')
            except DatabaseError:
                messages.error(request, 'Error')
                return render(request, '../templates/productos/crear_producto.html')
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
