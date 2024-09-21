import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.functional.authors.base import AuthorsBaseTest


@pytest.mark.selenium
class AuthorsRegisterTest(AuthorsBaseTest):
    def fill_dummy_data(self, form):  # noqa: PLR6301
        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH, '/html/body/main/div[2]/form'
        )

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register/')

        form = self.get_form()

        self.fill_dummy_data(form)

        callback(form)

        return form

    def test_register_username_error_message(self):
        def callback(form):
            form.find_element(By.ID, 'id_email').send_keys('dummy@example.com')

            first_name_field = self.get_by_placeholder(
                form, 'Enter your username'
            )
            first_name_field.send_keys(' ')
            first_name_field.send_keys(Keys.ENTER)

            form = self.get_form()

            assert 'Username is required' in form.text

        self.form_field_test_with_callback(callback)

    def test_field_email_error_message(self):
        def callback(form):
            email_field = form.find_element(By.ID, 'id_email')
            email_field.send_keys('dummy@example')
            email_field.send_keys(Keys.ENTER)

            form = self.get_form()

            assert 'Introduza um endereço de e-mail válido' in form.text

        self.form_field_test_with_callback(callback)

    def test_password_do_not_match(self):
        def callback(form):
            form.find_element(By.ID, 'id_email').send_keys('dummy@example.com')

            password = self.get_by_placeholder(form, 'Enter your password')
            password.send_keys('P@ssw0rd')

            password2 = self.get_by_placeholder(form, 'Repeat your password')
            password2.send_keys('P@ssw0rd_')
            password2.send_keys(Keys.ENTER)

            form = self.get_form()

            assert 'Passwords do not match' in form.text

        self.form_field_test_with_callback(callback)

    def test_authors_register_successfully(self):
        self.browser.get(self.live_server_url + '/authors/register/')

        form = self.get_form()

        self.get_by_placeholder(form, 'Ex.: John').send_keys('First Name')
        self.get_by_placeholder(form, 'Ex.: Doe').send_keys('Last Name')
        self.get_by_placeholder(form, 'Enter your username').send_keys(
            'firstname'
        )
        self.get_by_placeholder(form, 'Enter your email').send_keys(
            'dummy@example.com'
        )
        self.get_by_placeholder(form, 'Enter your password').send_keys(
            'P@ssw0rd'
        )
        self.get_by_placeholder(form, 'Repeat your password').send_keys(
            'P@ssw0rd'
        )

        form.submit()

        assert (
            'User created successfully. Please log in.'
            in self.browser.find_element(By.TAG_NAME, 'body').text
        )
