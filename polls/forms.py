
from django import forms

class StudentLoginForm(forms.Form):
    firstname = forms.CharField(max_length=150)
    registrationNo = forms.CharField(max_length=150)
