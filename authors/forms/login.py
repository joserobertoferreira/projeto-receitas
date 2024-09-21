from django import forms

from resources.utils.django_forms import add_placeholder


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_placeholder(self.fields['username'], 'Type your username')
        add_placeholder(self.fields['password'], 'Type your password')

    username = forms.CharField(max_length=100, label='Utilizador')
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
