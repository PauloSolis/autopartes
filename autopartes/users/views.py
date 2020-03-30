from django.contrib.auth.password_validation import validate_password
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.views import View
from .models import User
from .forms import UserRegister


# Create your views here.
class RegisterView(SuccessMessageMixin, View):
    form_class = UserRegister
    template_name = '../templates/crear_cuenta.html'
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
            return redirect('../')

        return render(request, self.template_name, {'form': form})


def displayUsers(request):
    users = User.objects.all().order_by('id')
    context = {
        'users': users,
    }
    return render(request, '../templates/ver_usuarios.html', context)
