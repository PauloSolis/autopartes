from django.db import models
from django.utils import timezone


class Product(models.Model):
    codigo = models.CharField(max_length=100, unique=True, null=False)
    nombre = models.CharField(max_length=100, null=False)
    descripcion = models.TextField(null=False)
    marca = models.CharField(max_length=100)
    modelo_coche = models.CharField(max_length=100)
    precio_minorista = models.FloatField(null=False)
    precio_mayorista1 = models.FloatField(null=True)
    precio_mayorista2 = models.FloatField(null=True)
    precio_mayorista3 = models.FloatField(null=True)

    def __str__(self):
        return self.nombre
