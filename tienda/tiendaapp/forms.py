from django import forms
from .models import Venta, DetalleVenta, Venta

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
        fields = ['cliente', 'pago_contra_entrega']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'pago_contra_entrega': forms.CheckboxInput(attrs={'class':'form-control'})
        }

DetalleFormSet = forms.inlineformset_factory(Venta, DetalleVenta, 
                                             fields=('producto', 'cantidad'), extra=1, can_delete=True,
                                             widgets = 
                                                {
                                                    'producto': forms.Select(attrs={'class': 'form-control'}),
                                                    'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
                                                }
                                            )
    