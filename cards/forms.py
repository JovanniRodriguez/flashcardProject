from django import forms
from .models import Flashcard

class FlashcardForm(forms.ModelsForm):
    class Meta:
        model = Card
        fields = ['question', 'answer', 'img', 'audio']

class CardsetForm(forms.ModelsForm):
    class Meta:
        model = CardsetForm
        fields = ['name', 'description']