from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from .views import RegisterView
from . import views

urlpatterns = [
    path("", views.index, name="index"),              #landing page, not signed in
    path("sign-in", views.signIn, name="signIn"),     #sign in page
    path("register", RegisterView.as_view(template_name="flashdeck/register.html"), name="register"),#register page
    path("home", views.home, name="home"),            #landing page when signed in (home page)
    #path("my-decks", views.myDecks, name="my-decks"), #myDecks page (redirect to sign in if not already)
    #path("create-deck", views.createDeck, name="create-deck"), #createDeck page
    path('account', views.account, name="account"),   #account page
    path(
        '',
        TemplateView.as_view(template_name='/base.html'),
        name='home'
    ),
    path('set/<int:set_id>/', views.flashcard_list, name='flashcard_list'),
    path('set/<int:set_id>/add/', views.add_flashcard, name='add_flashcard'),
    path('my-decks', views.myDecks, name='cardset_list'),
    path('create-deck', views.createDeck, name='add_cardset'),
    path('login/', LoginView.as_view(template_name='flashdeck/home.html'), name='login'),

]