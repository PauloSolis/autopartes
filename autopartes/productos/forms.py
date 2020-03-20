from django import forms
from django.forms import ModelForm
from .models import Product


class Products(ModelForm):
    codigo = forms.CharField(label='Código')
    nombre = forms.CharField(label='Nombre')
    descripcion = forms.CharField(label='Descripcion')
    marca = forms.CharField(label='Marca')
    modelo_coche = forms.CharField(label='Modelo del Coche')
    precio_minorista = forms.FloatField(label='Precio Minorista')

    #precio_mayorista1 = forms.FloatField(widget=forms.HiddenInput)
    #precio_mayorista2 = forms.FloatField(widget=forms.HiddenInput)
    #precio_mayorista3 = forms.FloatField(widget=forms.HiddenInput)


    class Meta:
        model = Product
        fields = ['codigo', 'nombre', 'descripcion', 'marca', 'modelo_coche', 'precio_minorista']

    def __init__(self, *args, **kwargs):
        super(Products, self).__init__(*args, **kwargs)
        self.fields['codigo'].widget.attrs['class'] = 'form-control'
        self.fields['nombre'].widget.attrs['class'] = 'form-control'
        self.fields['descripcion'].widget.attrs['class'] = 'form-control'
        self.fields['marca'].widget.attrs['class'] = 'form-control'
        self.fields['modelo_coche'].widget.attrs['class'] = 'form-control'
        self.fields['precio_minorista'].widget.attrs['class'] = 'form-control'
        #self.fields['precio_mayorista1'].widget.attrs['class'] = 'form-control'
        #self.fields['precio_mayorista2'].widget.attrs['class'] = 'form-control'
        #self.fields['precio_mayorista3'].widget.attrs['class'] = 'form-control'


