from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path(
        '',
        TemplateView.as_view(template_name='/base.html'),
        name='home'
    ),
    path('', views.flashcard_list, name='flashcard_list'),
    path('set/<int:set_id>/add/', views.add_flashcard, name='add_flashcard'),
    path('set/<int:set_id>/', views.cardset_list, name='cardset_list'),
    path('add/set/', views.add_cardset, name='add_cardset'),
]