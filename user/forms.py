from django import forms
from django.contrib.auth.forms import User

class SignUpForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-indigo-400'
        }) 
    )
    confurm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-indigo-400'
        }))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-indigo-400'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-indigo-400'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-indigo-400'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-indigo-400'
            }),
            
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confurm_password = cleaned_data.get("confurm_password")

        if password and confurm_password and password != confurm_password:
            raise forms.ValidationError("Passwords do not match")

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-indigo-400',
            'placeholder': 'Enter username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-indigo-400',
            'placeholder': 'Enter password'
        })
    )