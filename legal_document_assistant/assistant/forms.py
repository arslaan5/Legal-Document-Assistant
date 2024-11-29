from django import forms
from .models import UserInfo
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    widgets = {
        'username': forms.TextInput(attrs={
                'class': 'w-full p-3 rounded-lg bg-white bg-opacity-20 text-[#f5f5f5] placeholder-white/0 border border-white/30 focus:ring-2 focus:ring-[#001f54] focus:outline-none transition roboto-regular',
                'placeholder': 'Enter your username',
            }),
        'password': forms.PasswordInput(attrs={
                'class': 'w-full p-3 rounded-lg bg-white bg-opacity-20 text-[#f5f5f5] placeholder-white/0 border border-white/30 focus:ring-2 focus:ring-[#001f54] focus:outline-none transition roboto-regular',
                'placeholder': 'Enter your password',
            }),
    }


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full p-3 rounded-lg bg-white bg-opacity-20 text-[#f5f5f5] placeholder-white/0 border border-white/30 focus:ring-2 focus:ring-[#001f54] focus:outline-none transition roboto-regular',
                'placeholder': 'Enter your username',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full p-3 rounded-lg bg-white bg-opacity-20 text-[#f5f5f5] placeholder-white/0 border border-white/30 focus:ring-2 focus:ring-[#001f54] focus:outline-none transition roboto-regular',
                'placeholder': 'Enter your email',
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'w-full p-3 rounded-lg bg-white bg-opacity-20 text-[#f5f5f5] placeholder-white/0 border border-white/30 focus:ring-2 focus:ring-[#001f54] focus:outline-none transition roboto-regular',
                'placeholder': 'Enter your password',
            }),
        }
