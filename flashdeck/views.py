from django.shortcuts import render
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

def createDeck(request):
    return render(request, "flashdeck/create-deck.html")