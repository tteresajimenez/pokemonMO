from django.urls import path
from pokemon_api import views

urlpatterns = [
    path('pokemon/', views.PokemonView.as_view()),
]