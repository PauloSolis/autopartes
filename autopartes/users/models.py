from django.contrib.auth.models import AbstractUser
from django.db import models
from djmoney.models.validators import MinMoneyValidator
from djmoney.money import Money
from phonenumber_field.modelfields import PhoneNumberField
from djmoney.models.fields import MoneyField


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=50, null=False)
    ruc = models.BigIntegerField(null=False, default=False)
    birthday = models.DateField(auto_now=False, null=True, blank=True)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    mobile = PhoneNumberField(null=False, blank=False, unique=True)
    #balance = models.DecimalField(default=0, max_digits=14, decimal_places=2)
    balance = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', default=0,
                         validators=[
                             MinMoneyValidator(0),
                             MinMoneyValidator(Money(0, 'USD')),
                         ]
                         )
    is_administrator = models.BooleanField(default=False)
    is_wholesaler = models.BooleanField(default=False)
    is_retailer = models.BooleanField(default=True)
    can_buy = models.BooleanField(default=True)

    def __str__(self):
        return self.email


class Address(models.Model):
    name = models.CharField(max_length=100, null=False, default="Sin Nombre")
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    postal_code = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
