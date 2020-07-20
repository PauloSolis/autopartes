import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from productos.models import Product
from users.models import Address
from django.contrib import messages
from django.core.paginator import Paginator
from django.core import serializers


# Create your views here.
@login_required
def ver_catalogo(request):
    products = Product.objects.all().order_by('-id')
    paginator = Paginator(products, 20)

    brands = Product.objects.values('car_brand').distinct()

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    addresses = Address.objects.filter(user=request.user)

    return render(request, '../templates/shop/ver_catalogo.html',
                  {'products': page_obj, 'addresses': addresses, 'brands': brands})

@login_required
def get_models(request):
    models = Product.objects.filter(car_brand=request.GET.get('brand')).values('car_model').distinct().order_by('car_model')

    data = []

    for model in models:
        data.append(model['car_model'])

    return JsonResponse(json.dumps(data), safe=False)

@login_required
def get_years(request):
    years = Product.objects.filter(car_model=request.GET.get('model')).values('car_year').distinct()

    data = []

    for year in years:
        data.append(year['car_year'])

    return JsonResponse(json.dumps(data), safe=False)

@login_required
def get_filtered(request):

    print("hello there")
    brand = request.POST.get('brand_filter')
    model = request.POST.get('model_filter')
    year = request.POST.get('year_filter')

    products = Product.objects.filter(car_brand=brand, car_model=model, car_year=year)
    paginator = Paginator(products, 20)

    brands = Product.objects.values('car_brand').distinct()

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    addresses = Address.objects.filter(user=request.user)

    return render(request, '../templates/shop/ver_catalogo.html',
                  {'products': page_obj, 'addresses': addresses, 'brands': brands})


