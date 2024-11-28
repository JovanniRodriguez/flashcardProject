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
    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(
        attrs={
            'class': 'form-control mt-2 mb-4',
            'placeholder': 'Enter your old password'
            }))
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
        attrs={
            'class': 'form-control mt-2 mb-4',
            'placeholder': 'Enter a new password'
            }))
    new_password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
        attrs={
            'class': 'form-control mt-2 mb-4',
            'placeholder': 'Re-enter your new password'
            }))