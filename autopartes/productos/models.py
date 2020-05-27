from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=250, unique=True, null=False)


class Product(models.Model):
    original_code = models.CharField(max_length=100, unique=True, null=False)
    product_code = models.CharField(max_length=100, unique=True, null=False)
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    car_brand = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    car_year = models.IntegerField(null=False)
    public_price = models.FloatField(null=False)
    card_price = models.FloatField(null=True)
    master_price = models.FloatField(null=True)
    wholesale_price = models.FloatField(null=True)
    dozen_price = models.FloatField(null=True)
    image1 = models.ImageField(upload_to='images/%Y/%m/%d', blank=True)
    image2 = models.ImageField(upload_to='images/%Y/%m/%d', blank=True)

    def __str__(self):
        return self.name



