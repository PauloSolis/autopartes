from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class User(AbstractUser):

    ruc = models.BigIntegerField(null=False, default=False)
    address = models.CharField(null=False, default=False, max_length=128)
    city = models.CharField(null=False, max_length=50)
    birthday = models.DateField(auto_now=False, null=True, blank=True)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    mobile = PhoneNumberField(null=False, blank=False, unique=True)
    is_administrator = models.BooleanField(default=False)
    is_wholesaler = models.BooleanField(default=False)
    is_retailer = models.BooleanField(default=False)

    def __str__(self):
        return self.email