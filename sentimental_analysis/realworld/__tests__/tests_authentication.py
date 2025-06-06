import os
import sys

# Set up Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sentimental_analysis.settings')

# Now import Django modules
import unittest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail
from django.contrib.auth import get_user_model
from django.conf import settings

class AuthenticationTests(TestCase):

    def test_register_page_status_code(self):
        """Test if the register page is accessible."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_status_code(self):
        """Test if the login page is accessible."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_register_page_template(self):
        """Test if the register page uses the correct template."""
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'authapp/register.html')

    def test_login_page_template(self):
        """Test if the login page uses the correct template."""
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'authapp/login.html')

    def test_register_success(self):
        """Test if user can successfully register."""
        response = self.client.post(reverse('register'), {
            'username': 'TestUser',
            'password1': 'ANicePassword123',
            'password2': 'ANicePassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='TestUser').exists())

    def test_register_short_password(self):
        """Test if registration fails with short password."""
        response = self.client.post(reverse('register'), {
            'username': 'TestUser',
            'password1': '123',
            'password2': '123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password2',
                             "This password is too short. It must contain at least 8 characters.")

    def test_register_username_too_similar(self):
        """Test if registration fails with a password similar to username."""
        response = self.client.post(reverse('register'), {
            'username': 'TestUser',
            'password1': 'TestUser123',
            'password2': 'TestUser123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password2', "The password is too similar to the username.")

    def test_register_existing_username(self):
        """Test if registration fails with an existing username."""
        User.objects.create_user(username='existinguser', password='Password123')
        response = self.client.post(reverse('register'), {
            'username': 'existinguser',
            'password1': 'GoodPassword123',
            'password2': 'GoodPassword123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username', "A user with that username already exists.")

    def test_register_empty_username(self):
        """Test if registration fails with an empty username."""
        response = self.client.post(reverse('register'), {
            'username': '',
            'password1': 'Password123',
            'password2': 'Password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username', "This field is required.")

    def test_register_empty_password(self):
        """Test if registration fails with an empty password."""
        response = self.client.post(reverse('register'), {
            'username': 'TestUser',
            'password1': '',
            'password2': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password1', "This field is required.")

    def test_login_success(self):
        """Test if a user can log in with valid credentials."""
        User.objects.create_user(username='testuser', password='Password123')
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'Password123'
        })
        self.assertEqual(response.status_code, 302)

    def test_login_wrong_password(self):
        """Test if login fails with an incorrect password."""
        User.objects.create_user(username='TestUser', password='Password123')
        response = self.client.post(reverse('login'), {
            'username': 'TestUser',
            'password': 'WrongPassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password.")

    def test_login_wrong_username(self):
        """Test if login fails with an incorrect username."""
        User.objects.create_user(username='TestUser', password='Password123')
        response = self.client.post(reverse('login'), {
            'username': 'WrongUser',
            'password': 'Password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password.")

    def test_login_empty_username(self):
        """Test if login fails with an empty username."""
        response = self.client.post(reverse('login'), {
            'username': '',
            'password': 'Password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username', "This field is required.")

    def test_login_empty_password(self):
        """Test if login fails with an empty password."""
        response = self.client.post(reverse('login'), {
            'username': 'TestUser',
            'password': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password', "This field is required.")

    def test_logout(self):
        """Test if a logged-in user can log out."""
        user = User.objects.create_user(username='TestUser', password='Password123')
        self.client.login(username='TestUser', password='Password123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_username_case_insensitive_login(self):
        """Test if login is case-sensitive for username."""
        User.objects.create_user(username='TestUser', password='Password123')
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'Password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password.")

    def test_logout_redirect(self):
        """Test if a logged-out user is redirected to the login page."""
        user = User.objects.create_user(username='TestUser', password='Password123')
        self.client.login(username='TestUser', password='Password123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

    def test_register_username_too_long(self):
        """Test if registration fails with a username that is too long."""
        long_username = 'a' * 151  # Assuming username max_length is 150
        response = self.client.post(reverse('register'), {
            'username': long_username,
            'password1': 'Password123',
            'password2': 'Password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username', "Ensure this value has at most 150 characters (it has 151).")

    def test_register_invalid_username(self):
        """Test if registration fails with a username containing invalid characters."""
        response = self.client.post(reverse('register'), {
            'username': 'Invalid*User',
            'password1': 'Password123',
            'password2': 'Password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username',
                             "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.")

    def test_login_inactive_user(self):
        """Test if login fails for an inactive user."""
        user = User.objects.create_user(username='testuser', password='Password123', is_active=False)
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'Password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password.")

    def test_login_csrf(self):
        """Test if CSRF token is present on the login page."""
        response = self.client.get(reverse('login'))
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_register_csrf(self):
        """Test if CSRF token is present on the register page."""
        response = self.client.get(reverse('register'))
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_login_empty_username_and_password(self):
        """Test if login fails when both username and password are empty."""
        response = self.client.post(reverse('login'), {
            'username': '',
            'password': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username', "This field is required.")
        self.assertFormError(response, 'form', 'password', "This field is required.")


    def test_register_common_password(self):
        """Test if registration fails when password is too common."""
        response = self.client.post(reverse('register'), {
            'username': 'TestUser',
            'password1': 'password123',
            'password2': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password2', "This password is too common.")

    def test_login_form_error_message(self):
        """Test if login page shows correct error message when form validation fails."""
        response = self.client.post(reverse('login'), {
            'username': '',
            'password': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username', "This field is required.")
        self.assertFormError(response, 'form', 'password', "This field is required.")

    def test_register_form_error_message(self):
        """Test if register page shows correct error message when form validation fails."""
        response = self.client.post(reverse('register'), {
            'username': '',
            'password1': '',
            'password2': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username', "This field is required.")
        self.assertFormError(response, 'form', 'password1', "This field is required.")

    def test_user_can_login_and_logout_multiple_times(self):
        """Test that a user can log in and out multiple times."""
        user = User.objects.create_user(username='TestUser', password='Password123')
        for _ in range(3):
            login = self.client.login(username='TestUser', password='Password123')
            self.assertTrue(login)
            self.client.logout()

    def test_login_view_contains_form(self):
        """Test that the login view contains the login form."""
        response = self.client.get(reverse('login'))
        self.assertContains(response, '<form')

    def test_register_view_contains_form(self):
        """Test that the register view contains the registration form."""
        response = self.client.get(reverse('register'))
        self.assertContains(response, '<form')

    def test_logout_without_login(self):
        """Test that logout view works even if the user is not logged in."""
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

if __name__ == "__main__":
    unittest.main()