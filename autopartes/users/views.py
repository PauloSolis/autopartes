from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, login, get_user_model
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import DatabaseError
from djmoney.money import Money
from .models import User, Address
from .forms import UserRegister, AddressForm, EditProfileForm, EditBalance
from django.contrib.auth.forms import UserChangeForm
from .decorators import admin_required, wholesaler_required, retailer_required
from .forms import AuthenticationForm
from django.db.models import Q


# Create your views here.
class RegisterView(SuccessMessageMixin, View):
    form_class = UserRegister
    template_name = '../templates/registration/signup.html'
    success_message = "Tu cuenta ha sido creada!"

    # Display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            try:
                validate_password(password, username)
            except ValidationError as e:
                form.add_error('password', e)
                return render(request, self.template_name, {'form': form})

            user.set_password(password)
            user.save()
            if user is not None:
                login(request, user)
            return redirect('/index/')

        return render(request, self.template_name, {'form': form})


@login_required
@admin_required
def displayUsers(request, help=None):
    users = User.objects.all().order_by('id')
    addresses = Address.objects.all()

    if request.method == 'POST':
        id = request.POST.get('id')
        previous = User.objects.get(id=id)
        token = previous.balance
        form = EditBalance(request.POST or None, instance=previous)
        if form.is_valid():
            paid = form.cleaned_data.get('balance')
            maximun = form.cleaned_data.get('max')
            zero = Money(0, 'USD')
            if paid:
                X = Money(paid, 'USD')
                new = token - X
                if new > zero:
                    User.objects.filter(id=id).update(balance=(new))

            if maximun:
                User.objects.filter(id=id).update(max=maximun)
            if help:
                return 1
        return HttpResponseRedirect('/ver/')
    else:
        form = EditBalance()
    context = {
        'users': users,
        'form': form,
        'addresses': addresses,
    }
    return render(request, '../templates/users/ver_usuarios.html', context)


@login_required
@admin_required
def changeRole(request, id):
    try:
        User = get_user_model()
        usuario = User.objects.get(id=id)

        if request.method == 'POST':

            if request.POST.get('rol') != "0":
                if request.POST.get('rol') == "1":
                    usuario.is_retailer = True
                    usuario.is_wholesaler = False
                    usuario.is_administrator = False
                if request.POST.get('rol') == "2":
                    usuario.is_retailer = False
                    usuario.is_wholesaler = True
                    usuario.is_administrator = False
                if request.POST.get('rol') == "3":
                    usuario.is_retailer = False
                    usuario.is_wholesaler = False
                    usuario.is_administrator = True

            usuario.save()
            return HttpResponseRedirect('/ver/')

        context = {'usuario': usuario}
        return render(request, '../templates/users/changeRole.html', context)
    except:
        return render(request, '')  # cambiar esto a pantalla de error


class EditView(LoginRequiredMixin, View):
    form_class = EditProfileForm
    template_name = '../templates/registration/edit_profile.html'
    success_message = "Tus datos han sido modificados! "

    def get(self, request):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/index')
        return render(request, self.template_name, {'form': form})


@login_required
@admin_required
def deactivate_profile(request, id):
    user = User.objects.get(id=id)
    user.is_active = False
    user.save()
    return HttpResponseRedirect('/ver/')


@login_required
@admin_required
def activate_profile(request, id):
    user = User.objects.get(id=id)
    user.is_active = True
    user.save()
    return HttpResponseRedirect('/ver/')


@login_required
@admin_required
def cant_purchase(request, id):
    user = User.objects.get(id=id)
    user.can_buy = False
    user.save()
    return HttpResponseRedirect('/ver/')


@login_required
@admin_required
def can_purchase(request, id):
    user = User.objects.get(id=id)
    user.can_buy = True
    user.save()
    return HttpResponseRedirect('/ver/')


class CustomLoginView(LoginView):
    authentication_form = AuthenticationForm


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'


def create_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        context = {
            'form': form,
        }
        if form.is_valid():
            try:
                new_product = Address(
                    name=form.cleaned_data.get('name'),
                    state=form.cleaned_data.get('state'),
                    city=form.cleaned_data.get('city'),
                    address=form.cleaned_data.get('address'),
                    postal_code=form.cleaned_data.get('postal_code'),
                    user=request.user
                )
                new_product.save()
                messages.success(request, 'Se guardo correctamente la nueva direción!')
                return redirect('users:view_address')
            except DatabaseError:
                messages.error(request, 'Error')
                return render(request, '../templates/users/create_address.html', context)
    else:
        form = AddressForm
        context = {
            'form': form,
        }
        return render(request, '../templates/users/create_address.html', context)


def view_address(request):
    user = User.objects.get(id=request.user.id)
    addresses = Address.objects.filter(user=user).order_by('-id')

    context = {
        'addresses': addresses,
        'form': AddressForm,
    }

    return render(request, '../templates/users/view_address.html', context)


def delete_address(request, pk):
    Address.objects.get(id=pk).delete()
    messages.success(request, 'Se ha eliminado correctamente la dirección!')
    return redirect('users:view_address')


def edit_address(request, pk):
    address = Address.objects.get(id=pk)
    form = AddressForm(request.POST or None, instance=address)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Se ha editado correctamente la dirección!')
        return redirect('users:view_address')
    context = {
        'form': form,
    }
    return render(request, '../templates/users/edit_address.html', context)


@login_required
@admin_required
def search(request):
    query = request.GET.get('q', '')
    addresses = Address.objects.all()
    form = EditBalance()
    template = '../templates/users/search.html'
    if query:
        queryset = (Q(first_name__icontains=query)) | (Q(username__icontains=query)) | (
            Q(last_name__icontains=query)) | (Q(ruc__icontains=query))
        results = User.objects.filter(queryset).distinct()
    else:
        results = []
    displayUsers(request, 1)
    context = {
        'users': results,
        'query': query,
        'form': form,
        'addresses': addresses,
    }

    return render(request, template, context)
