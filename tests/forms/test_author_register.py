from http import HTTPStatus
from unittest import TestCase

from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized

from authors.forms.register import RegisterForm


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('first_name', 'Ex.: John'),
        ('last_name', 'Ex.: Doe'),
        ('username', 'Enter your username'),
        ('email', 'Enter your email'),
        ('password', 'Enter your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_fields_placeholder(self, field, value):  # noqa: PLR6301
        form = RegisterForm()

        placeholder = form[field].field.widget.attrs['placeholder']

        assert placeholder == value

    @parameterized.expand([
        (
            'username',
            (
                'Required. At least 5 characters. '
                'Only letters, digits and @.-_ are allowed'
            ),
        ),
        (
            'password',
            (
                'Password must have at least one uppercase letter,'
                ' and at least one lowercase letter'
            ),
        ),
    ])
    def test_fields_help_text(self, field, value):  # noqa: PLR6301
        form = RegisterForm()

        help_text = form[field].field.help_text

        assert help_text == value

    @parameterized.expand([
        ('first_name', 'Primeiro nome'),
        ('last_name', 'Último nome'),
        ('username', 'Utilizador'),
        ('email', 'Email'),
        ('password', 'Password'),
        ('password2', 'Repeat Password'),
    ])
    def test_fields_labels(self, field, value):  # noqa: PLR6301
        form = RegisterForm()

        label = form[field].field.label

        assert label == value


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'username',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email@example.com',
            'password': 'Str0ngPassword1',
            'password2': 'Str0ngPassword1',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'Username is required'),
        ('email', 'Email is required'),
        ('password', 'Password must be informed'),
        ('password2', 'Repeat your password'),
    ])
    def test_required_fields(self, field, error_message):
        self.form_data[field] = ''
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        # self.assertIn(error_message, response.content.decode('utf-8'))
        assert error_message in response.content.decode('utf-8')
        assert error_message in response.context['form'].errors.get(field)

    def test_username_field_min_length(self):
        self.form_data['username'] = 'JRF'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        message = 'Username must be at least 5 characters'

        assert message in response.content.decode('utf-8')
        assert message in response.context['form'].errors.get('username')

    def test_username_field_max_length(self):
        self.form_data['username'] = 'a' * 151
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        message = 'Username must not exceed 150 characters'

        assert message in response.content.decode('utf-8')
        assert message in response.context['form'].errors.get('username')

    def test_password_field_is_not_strong(self):
        self.form_data['password'] = 'weak'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        error_message = 'Password is not strong enough'

        assert error_message in response.context['form'].errors.get('password')

    def test_password_field_is_strong(self):
        # self.form_data['password'] = 'Str0ngPassword1'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        error_message = 'Password is not strong enough'

        assert error_message not in response.content.decode('utf-8')

    def test_if_password_and_password_confirmation_are_equal(self):
        self.form_data['password2'] = 'Teste'

        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        error_message = 'Passwords do not match'

        assert error_message in response.context['form'].errors.get('password')
        assert error_message in response.content.decode('utf-8')

    def test_send_request_to_register_view_using_get(self):
        url = reverse('authors:register_create')
        response = self.client.get(url)

        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_if_email_already_exist(self):
        url = reverse('authors:register_create')

        self.client.post(url, data=self.form_data, follow=True)

        response = self.client.post(url, data=self.form_data, follow=True)

        error_message = 'Email already registered'

        assert error_message in response.content.decode('utf-8')
        assert error_message in response.context['form'].errors.get('email')

    def test_if_author_created_can_login(self):
        url = reverse('authors:register_create')

        self.form_data.update({
            'username': 'testuser',
            'password': '@Bc12346',
            'password2': '@Bc12346',
        })

        self.client.post(url, data=self.form_data, follow=True)

        is_authenticated = self.client.login(
            username='testuser', password='@Bc12346'
        )

        assert is_authenticated
