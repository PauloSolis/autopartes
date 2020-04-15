from django.contrib.auth import authenticate
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from .views import RegisterView
from django.test import Client
from .forms import UserRegister
from .models import User


# Create your tests here.
class CreateUserTestCase(TestCase):
    def setUp(self):
        self.admin = User.objects.create(username='Anitalavalatina', first_name='Ana', last_name='Dueñas',
                                         ruc='12345678910', email='hola9713@gmail.com', password='HolaAmigos1',
                                         address='Casa 123', city='Celaya', birthday='2020-03-23',
                                         phone='+524616198966', mobile='+523516198966')

    def test_url(self):
        response = self.client.get(reverse('users:signup'))
        self.assertEqual(response.status_code, 200)

    def test_form(self):
        data = {
            'first_name': 'Paulo',
            'last_name': 'Solis',
            'username': 'Paulo3',
            'ruc': '14567895214',
            'email': 'prueba@gmail.com',
            'password1': 'PauloSolis1',
            'password2': 'PauloSolis1',
            'address': 'Micasa123',
            'city': 'Celaya',
            'birthday': '2020-03-23',
            'phone': '+524616133966',
            'mobile': '+524616133966',
        }

        form = UserRegister(data)
        self.assertTrue(form.is_valid())
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = User.objects.create(username=username, password=password, phone='+523516133966')
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


class DisplayUserTestCase(TestCase):
    def test_view(self):
        response = self.client.get(reverse('users:ver'))
        self.assertEqual(response.status_code, 302)


class LoginTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='Anitalavalatina', first_name='Ana', last_name='Dueñas',
                                        ruc='12345678910', email='hola9713@gmail.com', password='HolaAmigos1',
                                        address='Casa 123', city='Celaya', birthday='2020-03-23',
                                        phone='+523516198966', mobile='+535616198966')
        self.credentials = {
            'username': 'Anitalavalatina',
            'password': 'HolaAmigos1'
        }
        self.client = Client()

    def test_correct(self):
        response = self.client.post('/login/', **self.credentials)
        self.assertTrue(response)


class ChangeRoleTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='Anitalavalatina', first_name='Ana', last_name='Dueñas',
                                        ruc='12345678910', email='hola9713@gmail.com', password='HolaAmigos1',
                                        address='Casa 123', city='Celaya', birthday='2020-03-23',
                                        phone='+523516198966', mobile='+523516198966')

    def test_view(self):
        response = self.client.get(reverse('users:rol', args={self.user.id}))
        self.assertEqual(response.status_code, 302)

