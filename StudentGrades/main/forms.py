from django import forms
from .models import Student, Grade
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Student
        fields = ['name', 'username', 'date', 'password1', 'password2']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class LoginForm(AuthenticationForm):
    class Meta:
        model = Student
        fields = ['username']

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'grade']
        widgets = {
            'grade': forms.Select(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]),
        }