from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import ClearableFileInput

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class MyClearableFileInput(ClearableFileInput):
    initial_text = 'currently'
    input_text = 'change'
    clear_checkbox_label = 'clear'


class UserForm(UserCreationForm):
    #profilePic = forms.ImageField(label='Изображение профиля', required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2') #'profilePic',


class UserLoginForm(forms.Form):
    username = forms.CharField(label="Имя")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())


class ChangeUserProfile(forms.Form):
    username = forms.CharField(label="Имя", widget=forms.TextInput(attrs={'class':'nick_change', 'placeholder':'Сменить ник'}))
    email = forms.EmailField(label="Почта", widget=forms.TextInput(attrs={'class':'mail_change', 'placeholder':'Сменить почту'}))
    profilePic = forms.ImageField(label='Изображение профиля', required=False, widget=MyClearableFileInput)
    password = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class':'password_change', 'placeholder':'Сменить пароль'}), required=False)
