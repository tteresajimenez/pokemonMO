from rest_framework import serializers
from .models import Pokemon


class PokemonSerializer(serializers.ModelSerializer):
    """Transform the pokemon data (model) into a json"""
    class Meta:
        model = Pokemon
        fields = '__all__'

