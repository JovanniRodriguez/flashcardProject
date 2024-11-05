from django.contrib import admin
from .models import CardSet, Card # new

# Register your models here.

admin.site.register(CardSet) # new
admin.site.register(Card) # new
