from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, login, get_user_model
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserChangeForm
from .models import User
from .forms import UserRegister, EditProfileForm
from .decorators import admin_required, wholesaler_required, retailer_required
from .forms import AuthenticationForm


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
def displayUsers(request):
    users = User.objects.all().order_by('id')
    context = {
        'users': users,
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


def deactivate_profile(request, id):
    user = User.objects.get(id=id)
    user.is_active = False
    user.save()
    return HttpResponseRedirect('/ver/')

def activate_profile(request, id):
    user = User.objects.get(id=id)
    user.is_active = True
    user.save()
    return HttpResponseRedirect('/ver/')



class CustomLoginView(LoginView):
    authentication_form = AuthenticationForm


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
