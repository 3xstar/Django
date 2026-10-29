from django import forms
from django.core.validators import (
    EmailValidator,
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
    RegexValidator,
)
from django.forms import (CharField, EmailField, PasswordInput, IntegerField, ChoiceField, ComboField,
                          DateTimeField, TimeField, FileField, BooleanField)


class LoginForm(forms.Form):
    email_field = forms.EmailField(
        label='Email',
        required=True,
        validators=[EmailValidator(message='Не корректный email адрес')],
        widget=forms.EmailInput(attrs={'placeholder': 'Введите email'})
    )
    password_field = forms.CharField(
        label='Пароль',
        required=True,
        validators=[MinLengthValidator(8, message='Пароль должен быть не менее 8 символов')],
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'})
    )
    remember_me = forms.BooleanField(
        label='Запомнить меня',
        widget=forms.CheckboxInput()
    )


class Note(forms.Form):
    name = CharField(max_length=100, required=True, label="Name")
    text = CharField(required=True, label="Text")