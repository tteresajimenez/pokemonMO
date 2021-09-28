from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Pokemon, EvolutionChain, Stats
from .serializers import PokemonSerializer, StatsSerializer,EvolutionSerializer


# Create your views here.


class PokemonView(APIView):
    """Pokemon API View"""

    def get(self, request):
        """Returns the pokemon information"""
        pokemon_info = Pokemon.objects.all()
        stat_info = Stats.objects.all()
        query = self.request.query_params.get('name', None)

        if query is None:
            serializer_pokemon = PokemonSerializer(pokemon_info, many=True)
            serializer_stats = StatsSerializer(stat_info, many=True)
        else:
            pokemon_specific_data = Pokemon.objects.get(name=query)
            stats_specific_data = Stats.objects.get(id_pokemon_fk=pokemon_specific_data.id_pokemon)
            #same_evolution_chain = Pokemon.objects.filter(id_evolution_fk=pokemon_specific_data.id_evolution_fk)
            serializer_pokemon = PokemonSerializer(pokemon_specific_data)
            serializer_stats = StatsSerializer(stats_specific_data)
            #serializer_evolution = EvolutionSerializer(same_evolution_chain)
        return Response({'pokemon': serializer_pokemon.data,
                         'stats': serializer_stats.data,
                         #'evolution':serializer_evolution
                        })

