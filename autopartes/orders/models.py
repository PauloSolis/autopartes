from django.db import models
import productos

# Create your models here.
class Order(models.Model):
    total_price = models.FloatField(null=False)
    status = models.TextField(null=False)
    products = models.ManyToManyField(productos)
    #address = models.ForeignKey(addresses)
