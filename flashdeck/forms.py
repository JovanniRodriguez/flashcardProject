from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, PasswordChangeForm
from .models import Card, CardSet, CustomUser

class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['question', 'answer', 'img', 'audio']

class CardsetForm(forms.ModelForm):
    class Meta:
        model = CardSet
        fields = ['name', 'description']

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ["username", "email"]
        widgets = {
            'username' : forms.TextInput(attrs={
                'class' : 'form-group mb-5 form-control',
                'placeholder' : 'Username'
            }),
            'password': forms.PasswordInput(attrs={
                'class' : 'form-group form-control',
                'placeholder' : 'Password'
            }),
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")
        widgets = {
            'username' : forms.TextInput(attrs={
                'class' : 'form-group mb-5 form-control',
                'placeholder' : 'Username'
            }),
            'password': forms.PasswordInput(attrs={
                'class' : 'form-group form-control',
                'placeholder' : 'Password'
            }),
        }

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))