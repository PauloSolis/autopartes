from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.forms import DateInput
from django.forms import ModelForm
from phonenumber_field.formfields import PhoneNumberField
from .models import User, Address
from djmoney.models.fields import MoneyField
from djmoney.forms.fields import MoneyField


class UserRegister(UserCreationForm):
    username = forms.CharField(label='Nombre Comercial')
    first_name = forms.CharField(label='Nombre')
    last_name = forms.CharField(label='Apellidos ')
    ruc = forms.IntegerField(min_value=00000000000, max_value=99999999999, label='RUC ',
                             widget=forms.TextInput(attrs={'placeholder': 'ej. 98688242308'}))
    email = forms.EmailField(label='Correo electrónico',
                             widget=forms.EmailInput(attrs={'placeholder': 'ejemplo@gmail.com'}))
    birthday = forms.DateField(label='Fecha de nacimiento', widget=forms.SelectDateWidget(years=range(1960, 2012),
                                                                                          attrs={
                                                                                              'class': 'form-control snps-inline-select'}))
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput())
    phone = PhoneNumberField(label='Teléfono', widget=forms.TextInput(attrs={'placeholder': 'ej. +524617857592'}))
    mobile = PhoneNumberField(label='Teléfono celular',
                              widget=forms.TextInput(attrs={'placeholder': 'ej. +524617857592'}))

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'ruc', 'email', 'password1', 'password2', 'birthday',
            'phone', 'mobile')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['ruc'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['class'] = 'form-control'
        self.fields['mobile'].widget.attrs['class'] = 'form-control'
        # for fieldname in ['password1', 'password2']:
        # self.fields[fieldname].help_text = None


class AuthenticationForm(AuthenticationForm):
    username = forms.CharField(label=False, widget=forms.EmailInput(attrs={'placeholder': 'Correo'}))
    password = forms.CharField(label=False, widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))

    class Meta:
        model = User
        fields = ['email', 'password']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['email'].widget.attrs['class'] = 'form-control'
            self.fields['password'].widget.attrs['class'] = 'form-control'


STATE_CHOICES = [
    ('Azuay', 'Azuay'),
    ('Bolívar', 'Bolívar'),
    ('Cañar', 'Cañar'),
    ('Carchi', 'Carchi'),
    ('Chimborazo', 'Chimborazo'),
    ('El Oro', 'El Oro'),
    ('Esmeraldas', 'Esmeraldas'),
    ('Galápagos', 'Galápagos'),
    ('Guayas', 'Guayas'),
    ('Imbabura', 'Imbabura'),
    ('Loja', 'Loja'),
    ('Los Ríos', 'Los Ríos'),
    ('Manabí', 'Manabí'),
    ('Morona Santiago', 'Morona Santiago'),
    ('Napo', 'Napo'),
    ('Orellana', 'Orellana'),
    ('Pastaza', 'Pastaza'),
    ('Pichincha', 'Pichincha'),
    ('Santa Elena', 'Santa Elena'),
    ('Santo Domingo de los Tsáchilas', 'Santo Domingo de los Tsáchilas'),
    ('Sucumbíos', 'Sucumbíos'),
    ('Tungurahua', 'Tungurahua'),
    ('Zamora Chinchipe', 'Zamora Chinchipe'),

]


class AddressForm(ModelForm):
    name = forms.CharField(label='Nombre de la Sucursal')
    state = forms.CharField(label='Provincia', widget=forms.Select(choices=STATE_CHOICES))
    city = forms.CharField(label='Ciudad')
    address = forms.CharField(label='Dirección',
                              widget=forms.TextInput(attrs={'placeholder': 'Calle, colonia y número'}))
    postal_code = forms.IntegerField(min_value=00000000000, max_value=99999999999, label='Código Postal ',
                                     widget=forms.TextInput(attrs={'placeholder': 'ej.  090503'}))

    class Meta:
        model = Address
        fields = (
            'name', 'state', 'city', 'address', 'postal_code')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['state'].widget.attrs['class'] = 'form-control'
        self.fields['city'].widget.attrs['class'] = 'form-control'
        self.fields['address'].widget.attrs['class'] = 'form-control'
        self.fields['postal_code'].widget.attrs['class'] = 'form-control'


class EditProfileForm(UserChangeForm):
    password = None
    username = forms.CharField(label='Nombre Comercial')
    first_name = forms.CharField(label='Nombre')
    last_name = forms.CharField(label='Apellidos ')
    ruc = forms.IntegerField(min_value=00000000000, max_value=99999999999, label='RUC ',
                             widget=forms.TextInput(attrs={'placeholder': 'ej. 98688242308'}))
    email = forms.EmailField(label='Correo electrónico',
                             widget=forms.EmailInput(attrs={'placeholder': 'ejemplo@gmail.com'}))
    birthday = forms.DateField(label='Fecha de nacimiento', widget=forms.SelectDateWidget(years=range(1960, 2012),
                                                                                          attrs={
                                                                                              'class': 'form-control snps-inline-select'}))
    phone = PhoneNumberField(label='Teléfono', widget=forms.TextInput(attrs={'placeholder': 'ej. +524617857592'}))
    mobile = PhoneNumberField(label='Teléfono celular',
                              widget=forms.TextInput(attrs={'placeholder': 'ej. +524617857592'}))

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'ruc', 'email',
            'birthday',
            'phone', 'mobile']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['ruc'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['class'] = 'form-control'
        self.fields['mobile'].widget.attrs['class'] = 'form-control'


class EditBalance(ModelForm):
    balance = forms.DecimalField(max_digits=10, decimal_places=2, label='')

    class Meta:
        model = User
        fields = ['balance']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['balance'].widget.attrs['class'] = 'form-control'
