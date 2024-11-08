from django.shortcuts import render, redirect, get_object_or_404
from .models import CardSet, Card
from .forms import FlashcardForm
from .forms import CardsetForm

def cardset_list(request):
    sets = CardSet.objects.all()
    return render(request, 'cards/...', {'sets' : sets}) # replace ... with html page that lists the card sets

def add_cardset(request):
    if request.method == "POST":
        form = CardsetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cardset_list')
    else:
        form = CardsetForm()
    return render(request, 'cards/...', {'form' : form}) # replace ... with html page that has form to creat cardsets

def flashcard_list(request, set_id):
    flashcard_set = get_object_or_404(CardSet, id = set_id)
    flashcards = flashcard_set.cards.all()
    return render(request, 'cards/...', {'flashcard_set': flashcard_set}) # replace ... with html page that lists the cards out

def add_flashcard(request, set_id):
    flashcard_set = get_object_or_404(CardSet, id=set_id)
    if request.method == "POST":
        form = FlashcardForm(request.POST)
        if form.is_valid():
            flashcard = form.save(commit=False)
            flashcard.set = flashcard_set
            flashcard.save()
            return redirect('flashcard_list', set_id=set_id)
    else:
        form = FlashcardForm()
    return render(request, 'cards/...', {'form' : form, 'flashcard_set' : flashcard_set}) # replace ... with html page that has form to add cards

# Create your views here.
