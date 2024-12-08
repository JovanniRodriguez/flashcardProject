from django.shortcuts import render, redirect, get_object_or_404
from .models import CardSet, Card, CustomUser
from .forms import FlashcardForm, CardsetForm, CustomUserCreationForm, ChangePasswordForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("home")
    template_name = "flashdeck/register.html"

def index(request):
    return render(request, "flashdeck/index.html")

def signIn(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('cardset_list')  # Replace 'home' with the URL name for your dashboard or homepage
        else:
            return render(request, 'flashdeck/signIn.html', {'error': 'Invalid username or password'})
    return render(request, 'flashdeck/signIn.html')

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            login(request, user)  # Log the user in after registration
            return redirect('signIn')  # Redirect to sign-in page or another view
    else:
        form = CustomUserCreationForm()
    return render(request, "flashdeck/register.html", {"form": form})

def home(request):
    return render(request, "flashdeck/home.html")

@login_required
def edit_cardset(request, cardset_id):
    cardset = get_object_or_404(CardSet, id=cardset_id, user=request.user)
    cards = cardset.cards.all()

    if request.method == 'POST':
        cardset_form = CardsetForm(request.POST, instance=cardset)
        card_forms = [FlashcardForm(request.POST, prefix=str(card.id), instance=card) for card in cards]

        if cardset_form.is_valid() and all(form.is_valid() for form in card_forms):
            cardset_form.save()
            for form in card_forms:
                form.save()
            return redirect('cardset_detail', cardset_id=cardset.id)
    else:
        cardset_form = CardsetForm(instance=cardset)
        card_forms = [FlashcardForm(prefix=str(card.id), instance=card) for card in cards]

    context = {
        'cardset_form': cardset_form,
        'card_forms': card_forms,
    }
    return render(request, 'flashdeck/edit_cardset.html', context)

def account(request):
    return render(request, "flashdeck/account.html")

@login_required
def study(request, deck_id):
    card_set = get_object_or_404(CardSet, id=deck_id, user=request.user)
    cards = card_set.cards.all()
    
    # Add this for debugging
    print(f"Number of cards found: {cards.count()}")
    for card in cards:
        print(f"Card {card.id}: Question: {card.question}, Answer: {card.answer}")
    
    return render(request, 'flashdeck/study.html', {
        'cards': cards,
        'deck': card_set
    })

def quiz(request):
    return render(request, 'flashdeck/quiz.html')

@login_required
def myDecks(request):
    user_decks = CardSet.objects.filter(user=request.user)
    return render(request, 'flashdeck/myDecks.html', {'sets' : user_decks}) # replace ... with html page that lists the card sets

@login_required
def createDeck(request):
    if request.method == "POST":
        form = CardsetForm(request.POST)
        if form.is_valid():
            deck = form.save(commit=False)  
            deck.user = request.user       
            deck.save()             
            return redirect('cardset_list')
    else:
        form = CardsetForm()
    return render(request, 'flashdeck/create-deck.html', {'form' : form}) # replace ... with html page that has form to creat cardsets

@login_required
def flashcard_list(request, set_id):
    flashcard_set = get_object_or_404(CardSet, id=set_id, user=request.user)
    flashcards = Card.objects.filter(card_set=flashcard_set)
    return render(request, 'flashdeck/...', { 
        'flashcard_set': flashcard_set,
        'flashcards': flashcards
    }) # replace ... with html page that lists the cards out

@login_required
def add_flashcard(request, set_id):
    flashcard_set = get_object_or_404(CardSet, id=set_id, user=request.user)
    if request.method == "POST":
        form = FlashcardForm(request.POST)
        if form.is_valid():
            flashcard = form.save(commit=False)
            flashcard.set = flashcard_set
            flashcard.save()
            return redirect('flashcard_list', set_id=set_id)
    else:
        form = FlashcardForm()
    return render(request, 'flashdeck/create-card.html', {'form' : form, 'flashcard_set' : flashcard_set}) # replace ... with html page that has form to add cards

@login_required
def delete_account(request):
    if request.method == "POST" and "confirm_delete" in request.POST:
        # Delete the user if the confirmation flag is present
        request.user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect('index')  # Redirect to a safe page

    # If the request is GET or no confirmation flag, show the confirmation page
    return render(request, 'flashdeck/delete_account.html')

class ChangePasswordView(PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy('account')
    template_name = 'flashdeck/password_change.html'
