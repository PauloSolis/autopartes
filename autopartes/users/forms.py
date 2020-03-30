from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import DateInput
from phonenumber_field.formfields import PhoneNumberField
from .models import User


class UserRegister(UserCreationForm):
    username = forms.CharField(label='Nombre Comercial')
    first_name = forms.CharField(label='Nombre')
    last_name = forms.CharField(label='Apellidos ')
    ruc = forms.IntegerField(min_value=00000000000, max_value=99999999999, label='RUC ',
                             widget=forms.TextInput(attrs={'placeholder': 'ej. 98688242308'}))
    email = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(attrs={'placeholder': 'ejemplo@gmail.com'}))
    birthday = forms.DateField(label='Fecha de nacimiento', widget=forms.SelectDateWidget(years=range(1960, 2012), attrs={'class': 'form-control snps-inline-select'}))
    phone = PhoneNumberField(label='Teléfono', widget=forms.TextInput(attrs={'placeholder': 'ej. +524617857592'}))
    mobile = PhoneNumberField(label='Teléfono celular', widget=forms.TextInput(attrs={'placeholder': 'ej. +524617857592'}))
    address = forms.CharField(label='Dirección', widget=forms.TextInput(attrs={'placeholder': 'Calle, colonia y número'}))
    city = forms.CharField(label='Ciudad')

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'ruc', 'email', 'password1', 'password2', 'address', 'city',
            'birthday',
            'phone', 'mobile')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['ruc'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['address'].widget.attrs['class'] = 'form-control'
        self.fields['city'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['class'] = 'form-control'
        self.fields['mobile'].widget.attrs['class'] = 'form-control'
