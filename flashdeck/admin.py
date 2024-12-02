from django.contrib import admin
from .models import CardSet, Card, CustomUser
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username",]

admin.site.register(CardSet)
admin.site.register(Card)
admin.site.register(CustomUser, CustomUserAdmin)
