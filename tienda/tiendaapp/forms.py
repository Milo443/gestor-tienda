from django import forms
from .models import Venta, DetalleVenta, Producto, Cliente, Venta

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=10, required=True)
    email = forms.EmailField()
 
class LoginForm(forms.Form):
    email = forms.EmailField()

class TokenForm(forms.Form):
    token = forms.CharField(max_length=6, required=True)

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente']

DetalleFormSet = forms.inlineformset_factory(Venta, DetalleVenta, fields=('producto', 'cantidad'), extra=1, can_delete=True)
    