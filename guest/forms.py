from django import forms
from django.contrib.auth import password_validation

from .models import User


ROLES = (
    ('client', 'Cliente'),
    ('owner', 'Proprietário')
)

class RegisterForm(forms.Form):
    user_role = forms.ChoiceField(required=True, choices=ROLES)
    name = forms.CharField(required=True, max_length=100)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_password(self):
        password = self.cleaned_data.get('password')

        try:
            password_validation.validate_password(password)
        except:
            raise forms.ValidationError('Senha inválida')

        return password

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('As senhas não correspondem')

        user_email = cleaned_data.get('email')
        email_already_exists = User.objects.filter(email=user_email).exists()

        if email_already_exists:
            raise forms.ValidationError('Email já cadastrado.')

        return cleaned_data

