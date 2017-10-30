from django.test import TestCase
from django.test import Client
from django.urls import reverse
from myhome.models import UserProfile
from myhome.forms import forms

"""
    Test when arduino connected

    """
# class GetSensorTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#
#     def test_data_acquire(self):
"""
    Tests for the data read from arduino and stored in database

    """
#         response = self.client.get(reverse("myhome:connection"), follow=True)
#         self.assertEqual(response.status_code, 200)
#         self.assertGreaterEqual(response.context['data'].Uvalue, 0)
#         self.assertGreaterEqual(response.context['data'].Hvalue, 0)
#         self.assertLessEqual(response.context['data'].Uvalue, 100)
#         self.assertGreaterEqual(response.context['data'].Tvalue, -4)
#         self.assertLessEqual(response.context['data'].Uvalue, 125)

class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        my_admin = UserProfile(username='user', is_staff=True)
        my_admin.set_password('123456')
        my_admin.save()

    def test_login(self):
        """
            Tests for the user login

            """
        response = self.client.get(reverse("myhome:login"), follow=True)
        loginresponse = self.client.login(username='user', password='123456')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(loginresponse)

class ModifyProfile(TestCase):
    def setUp(self):
        self.first_user = UserProfile.objects.create(username='user', password='1234')

        self.test_user = UserProfile.objects.create(username='bob', password='swordfish')

        self.test_user.save()

    def test_registration_profile_created(self):
        """
        Test that a ``RegistrationProfile`` is created for a new user.

        """
        self.assertEqual(UserProfile.objects.count(), 2)

    class RegistrationFormTests(TestCase):
        """
        Tests for the forms and custom validation logic included in
        django-registration.

        """

        def test_registration_form(self):
            """
            Test that ``RegistrationForm`` enforces username constraints
            and matching passwords.

            """
            invalid_data_dicts = [
                # Non-alphanumeric username.
                {
                    'data':
                        {'username': 'foo/bar',
                         'email': 'foo@example.com',
                         'password1': 'foo',
                         'password2': 'foo'},
                    'error':
                        ('username', [u"Enter a valid value."])
                },
                # Already-existing username.
                {
                    'data':
                        {'username': 'alice',
                         'email': 'alice@example.com',
                         'password1': 'secret',
                         'password2': 'secret'},
                    'error':
                        ('username', [u"This username is already taken. Please choose another."])
                },
                # Mismatched passwords.
                {
                    'data':
                        {'username': 'foo',
                         'email': 'foo@example.com',
                         'password1': 'foo',
                         'password2': 'bar'},
                    'error':
                        ('__all__', [u"You must type the same password each time"])
                },
            ]

            for invalid_dict in invalid_data_dicts:
                form = forms.RegisterForm(data=invalid_dict['data'])
                self.failIf(form.is_valid())
                self.assertEqual(form.errors[invalid_dict['error'][0]], invalid_dict['error'][1])

            form = forms.RegisterForm(data={'username': 'foo',
                                                'email': 'foo@example.com',
                                                'password1': 'foo',
                                                'password2': 'foo'})
            self.failUnless(form.is_valid())

