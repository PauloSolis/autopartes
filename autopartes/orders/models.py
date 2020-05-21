from django.db import models
from productos.models import Product
import productos


class Order(models.Model):
    total_price = models.FloatField(null=False)
    status = models.TextField(null=False)
    products = models.ManyToManyField(Product)
    #address = models.ForeignKey(addresses)

class ProductsOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)
    price = models.FloatField(null=False)
