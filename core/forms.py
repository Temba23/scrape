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
