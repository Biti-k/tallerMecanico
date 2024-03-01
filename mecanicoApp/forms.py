from django import forms

class LoginForm(forms.Form):
    usuario = forms.CharField(label="Usuario", max_length=12, required=True, label_suffix='')
    password = forms.CharField(required=True, label="Contraseña", label_suffix='', widget=forms.PasswordInput)
