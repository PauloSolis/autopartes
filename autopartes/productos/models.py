from django.db import models
from django.utils import timezone


class Product(models.Model):
    original_code = models.CharField(max_length=100, unique=True, null=False)
    product_code = models.CharField(max_length=100, unique=True, null=False)
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(null=False)
    car_brand = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    car_year = models.IntegerField(null=False)
    public_price = models.FloatField(null=False)
    card_price = models.FloatField(null=True)
    master_price = models.FloatField(null=True)
    wholesale_price = models.FloatField(null=True)
    dozen_price = models.FloatField(null=True)

    def __str__(self):
        return self.name
