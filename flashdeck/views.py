from django.shortcuts import render, redirect, get_object_or_404
from .models import CardSet, Card
from .forms import FlashcardForm, CardsetForm, CustomUserCreationForm, CustomUserChangeForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "flashdeck/register.html"

def index(request):
    return render(request, "flashdeck/index.html")

def signIn(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect('home')
    else:
        form = AuthenticationForm()
    return render(request, "flashdeck/signIn.html", {"form": form})

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, "flashdeck/register.html", {"form": form})

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