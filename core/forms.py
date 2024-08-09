from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(
        label="Email",
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
