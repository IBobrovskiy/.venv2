from django import forms
from .models import Users
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    passwordRe = forms.CharField(widget=forms.PasswordInput(), label='Повторите пароль', strip=True)

    class Meta:
        model = Users
        fields = ['username', 'surname', 'email', 'password']  # Убрали passwordRe из fields

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        passwordRe = cleaned_data.get("passwordRe")

        # Проверяем, что оба поля заполнены
        if password and passwordRe:
            if password != passwordRe:
                print("Пароли не совпадают.")
                raise forms.ValidationError(_("Пароли не совпадают."))
            if len(password) < 8:
                print("Пароль должен содержать минимум 8 символов.")
                raise forms.ValidationError(_('Пароль должен содержать минимум 8 символов.'))
            if not re.search(r'[A-Za-z]', password):
                print("Пароль должен содержать хотя бы одну букву.")
                raise forms.ValidationError(_('Пароль должен содержать хотя бы одну букву.'))
            if not re.search(r'\d', password):
                print("Пароль должен содержать хотя бы одну цифру.")
                raise forms.ValidationError(_('Пароль должен содержать хотя бы одну цифру.'))


        return cleaned_data  # Верните очищенные данные

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(), max_length=128)
