from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.db import DatabaseError
from django.utils import timezone
from django.views.generic.edit import UpdateView
from django.contrib.auth import logout, login, get_user_model

def ver_catalogo(request):
    return render(request, '../templates/store.html')

def ver_landing(request):
    return render(request, '../templates/landing.html')