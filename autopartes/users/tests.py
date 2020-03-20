from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from .views import RegisterView
from .forms import UserRegister
from .models import User


# Create your tests here.
class CrearUsuarioTestCase(TestCase):
    def setUp(self):
        self.admin = User.objects.create(username='Anitalavalatina', first_name='Ana', last_name='Dueñas',
                            email='hola9713@gmail.com', password='HolaAmigos1', phone='+524616198966')

    def test_url(self):
        response = self.client.get(reverse('users:crear'))
        self.assertEqual(response.status_code, 200)

    def test_form(self):
        data = {
            'username': 'Paulo3',
            'first_name': 'Paulo',
            'last_name': 'Solis',
            'email': 'prueba@gmail.com',
            'password1': 'PauloSolis1',
            'password2': 'PauloSolis1',
            'phone': '+524616133966',
        }

        form = UserRegister(data)
        self.assertTrue(form.is_valid())
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = User.objects.create(username=username, password=password, phone='+524616133966')
        q = User.objects.all().order_by('-id')
        self.assertEqual(q[0].username, username)

    def test_db(self):
        self.assertTrue(User.objects.filter(username="Anitalavalatina"))

    def test_model(self):
        rol = self.admin.is_wholesaler
        self.admin.is_wholesaler = True
        self.admin.save()

        new_role = self.admin.is_wholesaler
        self.assertNotEqual(rol, new_role)
