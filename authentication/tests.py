from django.test import TestCase
from django.test import Client
from  django.urls import reverse
from django.contrib.auth.models import User

class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        my_admin = User(username='user', is_staff=True)
        my_admin.set_password('123456')
        my_admin.save()

    def test_login(self):
        response = self.client.get(reverse("authentication:login"), follow=True)
        loginresponse = self.client.login(username='user', password='123456')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(loginresponse)

