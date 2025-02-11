from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.views.generic import CreateView


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(label="Логин", disabled=True,
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(disabled=True,
                            widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(max_length=100, label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'email')
        labels = {
            'email': 'E-mail',
        }
