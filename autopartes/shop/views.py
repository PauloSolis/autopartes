from django.shortcuts import render
from productos.models import Product
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.

def ver_catalogo(request):
    products = Product.objects.all().order_by('-id')
    paginator = Paginator(products, 20)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, '../templates/shop/ver_catalogo.html', {'products': page_obj})