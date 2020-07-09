from django import forms
from django.forms import ModelForm
from .models import Order

STATUS_CHOICES = [
    ('Pendiente', 'Pendiente'),
    ('Despachando', 'Despachando'),
    ('Enviada', 'Enviada'),
    ('Finalizada', 'Finalizada'),

]


class Status(ModelForm):
    status = forms.CharField(label='Estado', widget=forms.Select(choices=STATUS_CHOICES))

    class Meta:
        model = Order
        fields = ['status', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget.attrs['class'] = 'form-control'
