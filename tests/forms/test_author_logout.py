from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthorLogoutTest(TestCase):
    def test_logout_using_get_method(self):
        User.objects.create_user(username='my_user', password='my_password')

        self.client.login(username='my_user', password='my_password')

        response = self.client.get(reverse('authors:logout'), follow=True)

        assert 'Invalid logout request.' in response.content.decode('utf-8')

    def test_logout_using_wrong_user(self):
        User.objects.create_user(username='my_user', password='my_password')

        self.client.login(username='my_user', password='my_password')

        response = self.client.post(
            reverse('authors:logout'),
            data={'username': 'other_user'},
            follow=True,
        )

        assert 'Invalid logout user.' in response.content.decode('utf-8')

    def test_logout_success(self):
        User.objects.create_user(username='my_user', password='my_password')

        self.client.login(username='my_user', password='my_password')

        response = self.client.post(
            reverse('authors:logout'),
            data={'username': 'my_user'},
            follow=True,
        )

        assert 'Logout success.' in response.content.decode('utf-8')
