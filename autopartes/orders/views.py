from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Order
from django.db import DatabaseError
from django.contrib.auth.decorators import login_required
from users.decorators import admin_required, retailer_required, wholesaler_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.generic.edit import UpdateView
from django.shortcuts import render
import json

# Create your views here.
def crear_orden(request):
    if request.method == 'POST':
        print('-------------------------------------------------')
        print(request.POST)

