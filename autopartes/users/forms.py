from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField

from .models import User

class UserRegister(UserCreationForm):
    username = forms.CharField(label='Usuario', widget=forms.TextInput(attrs={'placeholder': 'Juan5110'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'ejempl@gmail.com'}))
    phone = PhoneNumberField()
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1','password2', 'phone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['class'] = 'form-control'




