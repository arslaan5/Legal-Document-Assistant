from django import forms
from .models import UserInfo
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 rounded-lg bg-opacity-10 backdrop-blur-md text-[#F5F5F5] placeholder-gray-300 border border-white/20 focus:ring-1 focus:ring-[#FFD700] focus:outline-none transition duration-300 shadow-md hover:bg-opacity-20 roboto-regular',
            'placeholder': 'Enter your username',
            'autocomplete': 'off'
        })
        )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 rounded-lg bg-opacity-10 backdrop-blur-md text-[#F5F5F5] placeholder-gray-300 border border-white/20 focus:ring-1 focus:ring-[#FFD700] focus:outline-none transition duration-300 shadow-md hover:bg-opacity-20 roboto-regular',
            'placeholder': 'Enter your password',
        })
        )
    

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-opacity-10 backdrop-blur-md text-[#F5F5F5] placeholder-gray-300 border border-white/20 focus:ring-1 focus:ring-[#FFD700] focus:outline-none transition duration-300 shadow-md hover:bg-opacity-20 roboto-regular',
                'placeholder': 'Enter your username',
                'autocomplete': 'off'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-opacity-10 backdrop-blur-md text-[#F5F5F5] placeholder-gray-300 border border-white/20 focus:ring-1 focus:ring-[#FFD700] focus:outline-none transition duration-300 shadow-md hover:bg-opacity-20 roboto-regular',
                'placeholder': 'Enter your email',
                'autocomplete': 'off'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-opacity-10 backdrop-blur-md text-[#F5F5F5] placeholder-gray-300 border border-white/20 focus:ring-1 focus:ring-[#FFD700] focus:outline-none transition duration-300 shadow-md hover:bg-opacity-20 roboto-regular',
                'placeholder': 'Enter your password',
            }),
        }
