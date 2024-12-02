from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, PasswordChangeDoneView, PasswordChangeView
from .views import ChangePasswordView, RegisterView
from . import views

urlpatterns = [
    path("", views.index, name="index"),              #landing page, not signed in
    path("sign-in", views.signIn, name="signIn"),     #sign in page
    path("register", RegisterView.as_view(template_name="flashdeck/register.html"), name="register"),#register page
    path("home", views.home, name="home"),            #landing page when signed in (home page)
    path('account', views.account, name="account"),   #account page
    path(
        '',
        TemplateView.as_view(template_name='/base.html'),
        name='home'
    ),
    path('set/<int:set_id>/', views.flashcard_list, name='flashcard_list'),
    path('set/<int:set_id>/add/', views.add_flashcard, name='add_flashcard'),
    path('my-decks', views.my_decks, name='cardset_list'),
    path('create-deck', views.createDeck, name='add_cardset'),
    path('login/', LoginView.as_view(template_name='flashdeck/home.html'), name='login'),
    path('study/<int:deck>', views.study, name="study"),
    path('quiz', views.quiz, name="quiz"),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('cardset/<int:cardset_id>/edit/', views.edit_cardset_details, name='edit_cardset_details'),
    path('cardset/<int:cardset_id>/edit/cards/', views.edit_flashcards, name='edit_flashcards'),
    path('cardset/<int:deck_id>/delete/', views.delete_deck, name='delete_deck'),

]