from django import forms
from .models import Card, CardSet

class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['question', 'answer', 'img', 'audio']

class CardsetForm(forms.ModelForm):
    class Meta:
        model = CardSet
        fields = ['name', 'description']