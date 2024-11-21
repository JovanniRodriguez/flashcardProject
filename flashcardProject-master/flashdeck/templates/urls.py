from django.urls import path
from .views import RegisterView
from . import views

urlpatterns = [
    path("", views.index, name="index"),              # Landing page, not signed in
    path("sign-in", views.signIn, name="signIn"),     # Sign-in page
    path("register", RegisterView.as_view(), name="register"),  # Register page
    path("home", views.home, name="home"),            # Home page when signed in
    path("account", views.account, name="account"),   # Account page
    path("study", views.study, name="study"),         # Study page
    path("my-decks", views.myDecks, name="cardset_list"),  # My Decks page
    path("create-deck", views.createDeck, name="add_cardset"),  # Create Deck page
    path("set/<int:set_id>/", views.flashcard_list, name="flashcard_list"),
    path("set/<int:set_id>/add/", views.add_flashcard, name="add_flashcard"),
]