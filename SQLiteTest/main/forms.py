from django import forms


class TaskForm(forms.Form):
    title = forms.CharField(max_length=200, label="Title")
    status = forms.BooleanField(required=False, label="status")