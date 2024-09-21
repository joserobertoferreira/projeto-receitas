import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from tests.functional.authors.base import AuthorsBaseTest


@pytest.mark.selenium
class AuthorsLoginTest(AuthorsBaseTest):
    def test_login(self):
        string_password = 'password'

        user = User.objects.create_user(
            username='my_user', password=string_password
        )

        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # send form
        form.submit()

        # assert success message
        assert (
            f'Your are logged in with {user.username}'
            in self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_raise_not_found_error(self):
        self.browser.get(
            self.live_server_url + reverse('authors:login_create')
        )

        assert (
            'Not Found' in self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_form_invalid(self):
        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')

        username.send_keys(' ')
        password.send_keys(' ')

        # send form
        form.submit()

        # assert error messages
        assert (
            'Error: Invalid form'
            in self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_invalid_credentials(self):
        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')

        username.send_keys('mariana')
        password.send_keys('xwx')

        # send form
        form.submit()

        # assert error messages
        assert (
            'Invalid credentials'
            in self.browser.find_element(By.TAG_NAME, 'body').text
        )
