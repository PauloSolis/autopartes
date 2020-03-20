from django.test import TestCase
from .models import Product
from .forms import Products
from django.urls import reverse


class CrearProductoTestCase(TestCase):
    def setUp(self):
        Product.objects.create(codigo='AQ7WW5Q', nombre='Guia Derecha', descripcion='2.3 cm', marca='china',
                               modelo_coche='Chevrolet', precio_minorista='50', precio_mayorista1='10',
                               precio_mayorista2='15', precio_mayorista3='26')

    def test_url_correct(self):
        response = self.client.get(reverse('productos:crear'))
        self.assertEqual(response.status_code, 200)

    def test_form_correct(self):
        data = {
            'codigo': 'codigo1',
            'nombre': 'Guia Izquierda',
            'descripcion': '2.3 cm',
            'marca': 'china',
            'modelo_coche': 'Chevrolet',
            'precio_minorista': '520',

        }
        form = Products(data)
        self.assertTrue(form.is_valid())

    def test_form_incorrect(self):
        data = {
            'codigo': '',
            'nombre': '',
            'descripcion': '',
            'marca': 'china',
            'modelo_coche': 'Chevrolet',
            'precio_minorista': '520',

        }
        form = Products(data)
        self.assertFalse(form.is_valid())

    def test_form_not_unique(self):
        data = {
            'codigo': 'AQ7WW5Q',
            'nombre': 'Guia Derecha',
            'descripcion': '2.3 cm',
            'marca': 'china',
            'modelo_coche': 'Chevrolet',
            'precio_minorista': '520',

        }
        form = Products(data)
        self.assertFalse(form.is_valid())

    def test_model_correct(self):
        self.assertEqual(Product.objects.first().nombre, 'Guia Derecha')
