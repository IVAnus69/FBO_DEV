from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    #profilePic = forms.ImageField(label='Изображение профиля', required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2') #'profilePic',


class UserLoginForm(forms.Form):
    username = forms.CharField(label="Имя")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())


class ChangeUserProfile(forms.Form):
    username = forms.CharField(label="Имя")
    email = forms.EmailField(label="Почта")
    profilePic = forms.ImageField(label='Изображение профиля', required=False)
    password = forms.CharField(label="Новый пароль", widget=forms.PasswordInput())