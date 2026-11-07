from django import forms
from .models import Student, Grade

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'date', 'login', 'password']
        widgets = {
            'password': forms.PasswordInput(),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class LoginForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['login', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'grade']
        widgets = {
            'grade': forms.Select(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]),
        }