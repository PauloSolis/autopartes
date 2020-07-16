from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import DatabaseError
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from users.decorators import admin_required
from .forms import Products, CategoryForm, SubcategoryForm
from .models import Product
from django.db.models import Q

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


@login_required
@admin_required
def edit_product(request, id):
    product = Product.objects.get(id=id)
    form = Products(request.POST or None, instance=product)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('productos:ver_producto')
    context = {
        'form': form,
    }
    return render(request, '../templates/productos/editar_producto.html', context)


@login_required
@admin_required
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se guardó correctamente la categoría')
            return HttpResponseRedirect("/productos/ver/")
        else:

            return redirect("productos:ver_producto")
    else:
        form = CategoryForm
        context = {
            'form': form,
        }
        return render(request, '../templates/productos/crear_categoria.html', context)


@login_required
@admin_required
def create_subcategory(request):
    if request.method == 'POST':
        form = SubcategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se guardó correctamente la Subcategoría')
            return redirect("productos:ver_producto")
        else:

            return redirect("productos:ver_producto")
    else:
        form = SubcategoryForm
        context = {
            'form': form,
        }
        return render(request, '../templates/productos/create_subcategory.html', context)


@login_required
@admin_required
def search_product(request):
    query = request.GET.get('q', '')
    template = '../templates/productos/buscar_producto.html'
    if query:
        queryset = (Q(product_code__icontains=query)) | (Q(name__icontains=query)) | (
            Q(original_code__icontains=query)) | (Q(description__icontains=query))
        results = Product.objects.filter(queryset).distinct()
    else:
        results = []

    context = {
        'products': results,
        'query': query,
    }

    return render(request, template, context)
