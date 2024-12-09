
import json
from django.shortcuts import render, redirect, get_object_or_404
from .models import CardSet, Card
from .forms import FlashcardForm, CardsetForm, CustomUserCreationForm, ChangePasswordForm
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
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
            return redirect('cardset_list') 
        else:
            return render(request, 'flashdeck/signIn.html', {'error': 'Invalid username or password'})
    return render(request, 'flashdeck/signIn.html')

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()  
            login(request, user) 
            return redirect('signIn') 
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
            print(cardset_form.errors)  
    else:
        cardset_form = CardsetForm(instance=cardset)

    context = {
        'cardset_form': cardset_form,
        'sets': sets,
    }
    return render(request, 'flashdeck/myDecks.html', context)

@login_required
@require_POST
def edit_card(request, card_id):
    card = get_object_or_404(Card, id=card_id)

    data = json.loads(request.body)

    card.question = data.get('question', card.question)
    card.answer = data.get('answer', card.answer)

    card.save()

    return JsonResponse({'status': 'success'})

@login_required
def fetch_edit_cards(request, deck_id):
    flashcard_set = get_object_or_404(CardSet, id=deck_id, user=request.user)
    cards = Card.objects.filter(card_setNumber=flashcard_set).values('card_setNumber', 'question', 'answer', 'id')
    return JsonResponse({'cards': list(cards)})

@login_required
def get_study_cards(request, deck_id):
    flashcard_set = get_object_or_404(CardSet, id=deck_id, user=request.user)
    cards = Card.objects.filter(card_setNumber=flashcard_set).values('question', 'answer')
    return JsonResponse({'cards': list(cards)})

def delete_card(request, card_id):
    if request.method == 'DELETE':
        try:
            card = Card.objects.get(id=card_id)
            card.delete()
            return JsonResponse({'status': 'success', 'message': 'Card deleted successfully.'})
        except Card.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Card not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

@require_POST
def update_card_order(request):
    try:
        data = json.loads(request.body)
        card_updates = data.get('card_updates', [])
        
        for update in card_updates:
            card = Card.objects.get(id=update['id'])
            card.order = update['order']
            card.save()

        return JsonResponse({'status': 'success', 'message': 'Card order updated successfully'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
def edit_flashcards(request, cardset_id):
    cardset = get_object_or_404(CardSet, id=cardset_id, user=request.user)
    cards = cardset.cards.all()

    if request.method == 'POST':
        for card in cards:
            question = request.POST.get(f'question_{card.id}')
            answer = request.POST.get(f'answer_{card.id}')
            
            if question is not None and answer is not None:
                card.question = question
                card.answer = answer
                card.save()
        return redirect('cardset_detail', cardset_id=cardset.id)

    context = {
        'flashcards': cards,
    }
    return render(request, 'flashdeck/myDecks.html', context)


def account(request):
    if request.method == "POST" and "confirm_delete" in request.POST:
        request.user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect('index') 
    else:
        return render(request, "flashdeck/account.html")

def study(request, deck):
    deck_instance = get_object_or_404(CardSet, id=deck)

    return render(request, 'flashdeck/study.html', {'deck': deck_instance})

def quiz(request, deck):
    deck_instance = get_object_or_404(CardSet, id=deck)

    return render(request, 'flashdeck/quiz.html', {'deck': deck_instance})

def get_quiz_cards(request, deck):
    flashcard_set = get_object_or_404(CardSet, id=deck, user=request.user)
    cards = Card.objects.filter(card_setNumber=flashcard_set).values('question', 'answer')
    return JsonResponse({'cards': list(cards)})

@login_required
def my_decks(request):
    decks = CardSet.objects.filter(user=request.user)  
    return render(request, 'flashdeck/myDecks.html', {'sets': decks})

def delete_deck(request, deck_id):
    deck = get_object_or_404(CardSet, id=deck_id)
    if request.method == 'POST':
        deck.delete()
        return redirect('cardset_list')
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
    return render(request, 'flashdeck/create-deck.html', {'form' : form}) 

@login_required
def flashcard_list(request, set_id):
    flashcard_set = get_object_or_404(CardSet, id=set_id, user=request.user)
    flashcards = Card.objects.filter(card_setNumber=flashcard_set)
    return render(request, 'flashdeck/myDecks.html', { 
        'flashcard_set': flashcard_set,
        'flashcards': flashcards
    })

@login_required
def add_flashcard(request, set_id):
    flashcard_set = get_object_or_404(CardSet, id=set_id, user=request.user)
    if request.method == "POST":
        question = request.POST.get('question')
        answer = request.POST.get('answer')

        card = Card.objects.create(
            card_setNumber=flashcard_set,
            question=question,
            answer=answer,
        )
        return JsonResponse({'message': 'Card added successfully!', 'card_id': card.id})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def delete_account(request):
    if request.method == "POST" and "confirm_delete" in request.POST:

        request.user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect('sign-in')  

    return render(request, 'flashdeck/delete_account.html')

class ChangePasswordView(PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy('account')
    template_name = 'flashdeck/password_change.html'
