from rest_framework import serializers
from .models import Pokemon, EvolutionChain, Stats


class PokemonSerializer(serializers.ModelSerializer):
    """Transform the pokemon data (model) into a json"""
    id_evolution = serializers.ReadOnlyField(source='id_evolution_fk.id_evolution_chain', read_only=True)
    class Meta:
        model = Pokemon
        fields = ['id_pokemon', 'name', 'weight', 'height', 'id_evolution']


class StatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stats
        fields = ['special_defense','special_attack','defense','attack','hp','speed']

class EvolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = ['id_pokemon','name']