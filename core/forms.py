from django import forms
from .models import Alert, Scrip
class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class RegisterForm(forms.Form):
        username = forms.CharField(
        label="Username",
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
        email = forms.CharField(
        label="Email",
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
        password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
        password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class SymbolForm(forms.Form):
        symbol = forms.CharField(
        label="Company Scrip",
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )       

class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = ['scrip', 'alert_on']
        labels = {
            'scrip': 'Company Scrip',
            'alert_on': 'Minimum Target',
        }
        widgets = {
            'scrip': forms.Select(attrs={'class': 'form-control'}),
            'alert_on': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pass user if you need it later
        super().__init__(*args, **kwargs)
        self.fields['scrip'].queryset = Scrip.objects.all()