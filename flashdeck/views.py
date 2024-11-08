from django.shortcuts import render, redirect, get_object_or_404
from .models import CardSet, Card
from .forms import FlashcardForm, CardsetForm
from django.http import HttpResponse
# Create your views here.

def index(request):
    return render(request, "flashdeck/index.html")

def signIn(request):
    return render(request, "flashdeck/signIn.html")

def register(request):
    return render(request, "flashdeck/register.html")

def home(request):
    return render(request, "flashdeck/home.html")

def myDecks(request):
    return render(request, "flashdeck/myDecks.html")

# def createDeck(request):
    # return render(request, "flashdeck/create-deck.html")

def account(request):
    return render(request, "flashdeck/account.html")

def myDecks(request):
    sets = CardSet.objects.all()
    return render(request, 'flashdeck/myDecks.html', {'sets' : sets}) # replace ... with html page that lists the card sets

def createDeck(request):
    if request.method == "POST":
        form = CardsetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cardset_list')
    else:
        form = CardsetForm()
    return render(request, 'flashdeck/create-deck.html', {'form' : form}) # replace ... with html page that has form to creat cardsets

def flashcard_list(request, set_id):
    flashcard_set = get_object_or_404(CardSet, id = set_id)
    flashcards = flashcard_set.cards.all()
    return render(request, 'flashdeck/...', {'flashcard_set': flashcard_set}) # replace ... with html page that lists the cards out

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
    return render(request, 'flashdeck/...', {'form' : form, 'flashcard_set' : flashcard_set}) # replace ... with html page that has form to add cards