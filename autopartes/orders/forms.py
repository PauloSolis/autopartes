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
    carrier = forms.CharField(label='Paquetería', required=False)
    tracking_code = forms.CharField(label='Código de rastreo', required=False)

    class Meta:
        model = Order
        fields = ['status', 'carrier', 'tracking_code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget.attrs['class'] = 'form-control'
        self.fields['carrier'].widget.attrs['class'] = 'form-control'
        self.fields['tracking_code'].widget.attrs['class'] = 'form-control'
