from django.db import models
from productos.models import Product
from users.models import Address, User
import datetime


class Order(models.Model):
    total_price = models.FloatField(null=False)
    status = models.TextField(null=False)
    status_update = models.DateField(default=datetime.date.today)
    carrier= models.TextField(default='', max_length=10)
    tracking_code = models.TextField(default='', max_length=22)
    products = models.ManyToManyField(Product)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)




class ProductsOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)
    price = models.FloatField(null=False)

    @property
    def total(self):
        return self.quantity * self.price