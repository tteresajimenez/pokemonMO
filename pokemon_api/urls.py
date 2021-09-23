from django.urls import path
from pokemon_api import views
from rest_framework import routers

urlpatterns = [
    path('pokemon/', views.PokemonView.as_view()),
]