from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class User(AbstractUser):


    is_administrator = models.BooleanField(default=False)
    is_wholesaler = models.BooleanField(default=False)
    is_retailer = models.BooleanField(default=False)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
