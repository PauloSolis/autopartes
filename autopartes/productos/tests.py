from django.test import TestCase
from .models import Product
from .forms import Products
from django.urls import reverse
from django.core.management import call_command


class CrearProductoTestCase(TestCase):
    def setUp(self):
        Product.objects.create(original_code='qwerewetret', product_code='sahsakjhaksjh', name='capot',
                               description='blanco', car_brand='honda', car_model='civic',
                               car_year='2020', public_price='200', card_price='250', master_price='100',
                               wholesale_price='150', dozen_price='190')

    def test_url_correct(self):
        response = self.client.get(reverse('productos:crear'))
        self.assertEqual(response.status_code, 200)

    def test_form_correct(self):
        data = {
            'original_code': 'qwerewetrets',
            'product_code': 'sahsakjhaksjhs',
            'name': 'guia',
            'description': 'derecha',
            'car_brand': 'honda',
            'car_model': 'civic',
            'car_year': '2020',
            'public_price': '200.00',
            'card_price': '250.00',
            'master_price': '100.00',
            'wholesale_price': '150.00',
            'dozen_price': '190.00',
        }
        form = Products(data)
        self.assertTrue(form.is_valid())

    def test_form_incorrect(self):
        data = {
            'original_code': '',
            'product_code': '',
            'name': '',
            'description': '',
            'car_brand': 'honda',
            'car_model': 'civic',
            'car_year': '2020',
            'public_price': '200',
            'card_price': '250',
            'master_price': '100',
            'wholesale_price': '150',
            'dozen_price': '190',

        }
        form = Products(data)
        self.assertFalse(form.is_valid())

    def test_form_not_unique(self):
        data = {
            'original_code': 'qwerewetret',
            'product_code': 'sahsakjhaksjh',
            'name': 'capot',
            'description': 'blanco',
            'car_brand': 'honda',
            'car_model': 'civic',
            'car_year': '2020',
            'public_price': '200',
            'card_price': '250',
            'master_price': '100',
            'wholesale_price': '150',
            'dozen_price': '190',

        }
        form = Products(data)
        self.assertFalse(form.is_valid())

    def test_model_correct(self):
        self.assertEqual(Product.objects.first().name, 'capot')


class VerProductosTestCase(TestCase):
    def test_view2(self):
        call_command('flush', '--noinput')
        response = self.client.get(reverse('productos:ver_producto'))
        self.assertContains(response, '<h1 id="msg">No hay productos registrados</h1>', status_code=200)
        self.assertTemplateUsed(response, '../templates/productos/ver_producto.html')

    def setUp(self):
        Product.objects.create(original_code='qwerewetret', product_code='sahsakjhaksjh', name='capot',
                               description='blanco', car_brand='honda', car_model='civic',
                               car_year='2020', public_price='200', card_price='250', master_price='100',
                               wholesale_price='150', dozen_price='190')

    def test_url_correct(self):
        response = self.client.get(reverse('productos:ver_producto'))
        self.assertEqual(response.status_code, 200)

    def test_view(self):
        response = self.client.get(reverse('productos:ver_producto'))
        self.assertContains(response, 'capot')


class EliminarProductosTestCase(TestCase):
    product = Product.objects.create(original_code='qwerewetret', product_code='sahsakjhaksjh', name='capot',
                                     description='blanco', car_brand='honda', car_model='civic',
                                     car_year='2020', public_price='200', card_price='250', master_price='100',
                                     wholesale_price='150', dozen_price='190')

    def eliminarProducto(self):
        response = self.client.get('/inventario/delete/' + str(self.product.id) + '/')
        self.assertEqual(response.status_code, 302)


class EditProductsTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(original_code='qwerewetret', product_code='sahsakjhaksjh', name='capot',
                                              description='blanco', car_brand='honda', car_model='civic',
                                              car_year='2020', public_price='200', card_price='250', master_price='100',
                                              wholesale_price='150', dozen_price='190')

    def test_view(self):
        response = self.client.get(reverse('productos:edit_product', args={self.product.id}))
        self.assertContains(response.status_code,302)
