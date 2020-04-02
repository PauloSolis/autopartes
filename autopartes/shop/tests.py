from django.test import TestCase
from productos.models import Product
from django.urls import reverse
from django.core.management import call_command

class VerProductosTestCase(TestCase):
    def setUp(self):
        Product.objects.create(original_code='qwerewetret', product_code='sahsakjhaksjh', name='capot',
                               description='blanco', car_brand='honda', car_model='civic',
                               car_year='2020', public_price='200', card_price='250', master_price='100',
                               wholesale_price='150', dozen_price='190')

    def test_url_correct(self):
        response = self.client.get(reverse('shop:ver_catalogo'))
        self.assertEqual(response.status_code, 200)

    def test_view(self):
        response = self.client.get(reverse('shop:ver_catalogo'))
        self.assertContains(response, 'capot')


