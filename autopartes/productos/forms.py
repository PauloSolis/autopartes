from django import forms
from django.forms import ModelForm
from .models import Product, Category


class Products(ModelForm):
    original_code = forms.CharField(label="Código Original")
    product_code = forms.CharField(label="Código de Producto")
    name = forms.CharField(label="Nombre")
    description = forms.CharField(label="Descripción")
    car_brand = forms.CharField(label="Marca del Coche")
    car_model = forms.CharField(label="Modelo del Coche")
    car_year = forms.IntegerField(label="Año del Coche")
    public_price = forms.FloatField(label="Precio al Público")
    card_price = forms.FloatField(label="Precio con Tarjeta")
    master_price = forms.FloatField(label="Precio Maestro")
    wholesale_price = forms.FloatField(label="Precio por Mayoreo")
    dozen_price = forms.FloatField(label="Precio por Docena")
    image1 = forms.ImageField(label="Foto de Frente")
    image2 = forms.ImageField(label="Foto de Posterior")

    class Meta:
        model = Product
        fields = ['original_code', 'product_code', 'name', 'category', 'car_brand', 'car_model', 'car_year', 'description',
                  'public_price', 'card_price', 'master_price', 'wholesale_price', 'dozen_price', 'image1', 'image2']

    def __init__(self, *args, **kwargs):
        super(Products, self).__init__(*args, **kwargs)
        self.fields['original_code'].widget.attrs['class'] = 'form-control'
        self.fields['product_code'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['car_brand'].widget.attrs['class'] = 'form-control'
        self.fields['car_model'].widget.attrs['class'] = 'form-control'
        self.fields['car_year'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['public_price'].widget.attrs['class'] = 'form-control'
        self.fields['card_price'].widget.attrs['class'] = 'form-control'
        self.fields['master_price'].widget.attrs['class'] = 'form-control'
        self.fields['wholesale_price'].widget.attrs['class'] = 'form-control'
        self.fields['dozen_price'].widget.attrs['class'] = 'form-control'
        self.fields['category'].widget.attrs['class'] = 'form-control'
        self.fields['category'].queryset = Category.objects.filter()
        self.fields['category'].label_from_instance = lambda obj: "%s " % obj.name

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'




