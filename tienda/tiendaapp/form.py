from django import forms

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=10, required=True)
    email = forms.EmailField()
 
class LoginForm(forms.Form):
    email = forms.EmailField()

class TokenForm(forms.Form):
    token = forms.CharField(max_length=6, required=True)
    