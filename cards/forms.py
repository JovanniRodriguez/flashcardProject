from django import forms
from .models import Card, CardSet

class FlashcardForm(forms.ModelsForm):
    class Meta:
        model = Card
        fields = ['question', 'answer', 'img', 'audio']

class CardsetForm(forms.ModelsForm):
    class Meta:
        model = CardSet
        fields = ['name', 'description']