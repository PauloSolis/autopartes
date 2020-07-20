from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.db import DatabaseError
from django.utils import timezone
from django.views.generic.edit import UpdateView
from django.contrib.auth import logout, login, get_user_model
from productos.models import Product


def ver_catalogo(request):

    return render(request, '../templates/store.html')


def ver_landing(request):
    products = Product.objects.all().filter(is_new=True)
    return render(request, '../templates/landing.html', {'products': products})


def about_us(request):
    return render(request, '../templates/about_us.html')


def contact_us(request):
    return render(request, '../templates/contact-us.html')