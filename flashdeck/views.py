from django.shortcuts import render, redirect, get_object_or_404
from .models import CardSet, Card, CustomUser
from .forms import FlashcardForm, CardsetForm, CustomUserCreationForm, ChangePasswordForm
from django.http import JsonResponse
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
def edit_cardset_details(request, cardset_id):
    cardset = get_object_or_404(CardSet, id=cardset_id, user=request.user)
    sets = CardSet.objects.filter(user=request.user)

    if request.method == 'POST':
        cardset_form = CardsetForm(request.POST, instance=cardset)
        if cardset_form.is_valid():
            cardset_form.save()
            return redirect('cardset_list') 
        else:
            # If form isn't valid, log or print to see the errors
            print(cardset_form.errors)  # Check for validation errors
    else:
        cardset_form = CardsetForm(instance=cardset)

    context = {
        'cardset_form': cardset_form,
        'sets': sets,
    }
    return render(request, 'flashdeck/myDecks.html', context)


@login_required
def edit_flashcards(request, set_id):
    flashcard_set = get_object_or_404(CardSet, id=set_id, user=request.user)
    if request.method == 'POST' and request.POST.get('action') == 'edit':
        card_id = request.POST.get('card_id')
        card = get_object_or_404(Card, id=card_id, card_setNumber=flashcard_set)
        card.question = request.POST.get('question')
        card.answer = request.POST.get('answer')
        card.save()
        return JsonResponse({'status': 'success'})  # Return success response
    return render(request, 'flashdeck/edit_flashcards.html', {'flashcard_set': flashcard_set})


def account(request):
    if request.method == "POST" and "confirm_delete" in request.POST:
        # Delete the user if the confirmation flag is present
        request.user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect('index')  # Redirect to a safe page
    else:
        return render(request, "flashdeck/account.html")

def study(request, deck):
    deck_instance = get_object_or_404(CardSet, id=deck)

    return render(request, 'flashdeck/study.html', {'deck': deck_instance})

def quiz(request, deck):
    deck_instance = get_object_or_404(CardSet, id=deck)

    return render(request, 'flashdeck/quiz.html', {'deck': deck_instance})

@login_required
def my_decks(request):
    decks = CardSet.objects.filter(user=request.user)  # Or filter for specific decks
    return render(request, 'flashdeck/myDecks.html', {'sets': decks})

def delete_deck(request, deck_id):
    deck = get_object_or_404(CardSet, id=deck_id)
    if request.method == 'POST':
        deck.delete()
        return redirect('cardset_list')  # Redirect to the list of decks after deletion
    return render(request, 'confirm_delete.html', {'deck': deck})

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
    flashcards = Card.objects.filter(card_setNumber=flashcard_set)
    return render(request, 'flashdeck/myDecks.html', { 
        'flashcard_set': flashcard_set,
        'flashcards': flashcards
    }) # replace ... with html page that lists the cards out

@login_required
def add_flashcard(request, set_id):
    flashcard_set = get_object_or_404(CardSet, id=set_id, user=request.user)
    if request.method == "POST" and request.POST.get('action') == 'add':
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        #image = request.FILES.get('image')
        #audio = request.FILES.get('audio')

        # Create and save the new Card instance
        Card.objects.create(
            card_setNumber=flashcard_set,
            question=question,
            answer=answer,
            #img=image if image else None,
            #audio=audio if audio else None
        )
        return JsonResponse({'status': 'success'});

    return render(request, 'flashdeck/create-card.html', {'flashcard_set': flashcard_set})

@login_required
def delete_account(request):
    if request.method == "POST" and "confirm_delete" in request.POST:
        # Delete the user if the confirmation flag is present
        request.user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect('sign-in')  # Redirect to a safe page

    # If the request is GET or no confirmation flag, show the confirmation page
    return render(request, 'flashdeck/delete_account.html')

class ChangePasswordView(PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy('account')
    template_name = 'flashdeck/password_change.html'
