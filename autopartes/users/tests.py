from django.contrib.auth import authenticate
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from .views import view_address
from django.test import Client
from .forms import UserRegister, AddressForm
from .models import User, Address
from django.core.management import call_command


# Create your tests here.
class CreateUserTestCase(TestCase):
    def setUp(self):
        self.admin = User.objects.create(username='Anitalavalatina', first_name='Ana', last_name='Dueñas',
                                         ruc='12345678910', email='hola9713@gmail.com', password='HolaAmigos1'
                                         , birthday='2020-03-23', phone='+524616198966', mobile='+523516198966')

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
                                        birthday='2020-03-23', phone='+523516198966', mobile='+535616198966')
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
                                        birthday='2020-03-23', phone='+523516198966', mobile='+523516198966')

    def test_view(self):
        response = self.client.get(reverse('users:rol', args={self.user.id}))
        self.assertEqual(response.status_code, 302)



class CreateAddressTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='Anitalavalatina', first_name='Ana', last_name='Dueñas',
                                        ruc='12345678910', email='hola9713@gmail.com', password='HolaAmigos1',
                                        birthday='2020-03-23', phone='+523516198966', mobile='+523516198966')
        Address.objects.create(name='Alborada', state='Guayas', city='Guayaquil', postal_code='060509', user=self.user)

    def test_url_correct(self):
        response = self.client.get(reverse('users:create_address'))
        self.assertEqual(response.status_code, 200)

    def test_form_incorrect(self):
        data = {
            'name': 'Alborada',
            'state': 'sahsakjhaksjhs',
            'city': 'guia',
            'postal_code': '121212',
            'user': self.user
        }
        form = AddressForm(data)
        self.assertFalse(form.is_valid())

    def test_form_not_unique(self):
        data = {
            'name': 'Alborada',
            'state': 'sahsakjhaksjhs',
            'city': 'guia',
            'postal_code': '121212',
            'user': self.user
        }
        form = AddressForm(data)
        self.assertFalse(form.is_valid())

    def test_model_correct(self):
        self.assertEqual(Address.objects.first().name, 'Alborada')


class ViewAddresses(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='Anitalavalatina', first_name='Ana', last_name='Dueñas',
                                        ruc='12345678910', email='hola9713@gmail.com', password='HolaAmigos1',
                                        birthday='2020-03-23', phone='+523516198966', mobile='+523516198966')
        Address.objects.create(name='Alborada', state='Guayas', city='Guayaquil', postal_code='060509', user=self.user)

    def test_view_address_URL(self):
        response = self.client.get(reverse('users:view_address'))
        self.assertEqual(response.status_code, 302)


class deleteAddress(TestCase):
    def test_delete_address(self):
        self.user = User.objects.create(username='Anitalavalatina', first_name='Ana', last_name='Dueñas',
                                        ruc='12345678910', email='hola9713@gmail.com', password='HolaAmigos1',
                                        birthday='2020-03-23', phone='+523516198966', mobile='+523516198966')
        self.address = Address.objects.create(name='Alborada', state='Guayas', city='Guayaquil', postal_code='060509',
                                              user=self.user)
        self.address.delete()
        self.assertFalse(Address.objects.filter(id=self.address.id))


class EditAddress(TestCase):
    def test_edit_address(self):
        self.user = User.objects.create(username='Anitalavalatina', first_name='Ana', last_name='Dueñas',
                                        ruc='12345678910', email='hola9713@gmail.com', password='HolaAmigos1',
                                        birthday='2020-03-23', phone='+523516198966', mobile='+523516198966')
        self.address = Address.objects.create(name='Alborada', state='Guayas', city='Guayaquil', postal_code='060509', user=self.user)
        self.client.get('users:edit_address', )

class EditProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='Anitalavalatina', first_name='Ana', last_name='Dueñas',
                                        ruc='12345678910', email='hola9713@gmail.com', password='HolaAmigos1',
                                        address='Casa 123', city='Celaya', birthday='2020-03-23',
                                        phone='+523516198966', mobile='+523516198966')

    def test_view(self):
        response = self.client.get(reverse('users:edit_profile'))
        self.assertEqual(response.status_code, 302)


class AccountActivationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='Anitalavalatina', first_name='Ana', last_name='Dueñas',
                                        ruc='12345678910', email='hola9713@gmail.com', password='HolaAmigos1',
                                        address='Casa 123', city='Celaya', birthday='2020-03-23',
                                        phone='+523516198966', mobile='+523516198966')
    def test_deactivate_view(self):
        response = self.client.get(reverse('users:deactivateUser',args={self.user.id}))
        self.assertEqual(response.status_code, 302)

    def test_activate_view(self):
        response = self.client.get(reverse('users:activateUser', args={self.user.id}))
        self.assertEqual(response.status_code, 302)

