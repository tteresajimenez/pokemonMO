from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Pokemon
from .serializers import PokemonSerializer

# Create your views here.


class PokemonView(APIView):
    """Pokemon API View"""

    def get(self, request):
        """Returns the pokemon information"""
        pokemon_info = Pokemon.objects.all()
        query = self.request.query_params.get('name', None)
        if query is None:
            serializer = PokemonSerializer(pokemon_info, many=True)
        else:
            pokemon_specific_data = Pokemon.objects.get(name=query)
            serializer = PokemonSerializer(pokemon_specific_data)
        return Response(serializer.data)

