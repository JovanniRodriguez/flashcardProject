from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),              #landing page, not signed in
    path("sign-in", views.signIn, name="signIn"),     #sign in page
    path("register", views.register, name="register"),#register page
    path("home", views.home, name="home"),            #landing page when signed in (home page)
    path("my-decks", views.myDecks, name="my-decks"), #myDecks page (redirect to sign in if not already)
    
]