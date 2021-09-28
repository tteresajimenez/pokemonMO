

import requests


URL_EVOLUTION = "https://pokeapi.co/api/v2/evolution-chain/"
URL_POKEMON = "https://pokeapi.co/api/v2/pokemon/"


def get_pokemon_stats(id_pokemon):
    """Returns a list with the stats of the pokemon in the chain"""
    all_stats = []
    pokemon_stats = []
    num_stats = 5
    for item in id_pokemon:
        pokemon_characteristics_url = URL_POKEMON + str(item)
        data = requests.get(pokemon_characteristics_url).json()
        all_stats.append(data.get("stats"))
        num_stats = 5
        while num_stats >= 0:
            pokemon_stats.append(data['stats'][num_stats]['base_stat'])
            pokemon_stats.append(data['stats'][num_stats]['stat']['name'])
            num_stats = num_stats - 1

    # It creates sublist based on the stats and their value
    pokemon_stats = [pokemon_stats[i * len(pokemon_stats) // (len(pokemon_stats)//2): (i + 1) * len(pokemon_stats) // (len(pokemon_stats)//2)] for i in range((len(pokemon_stats)//2))]
    # It creates 3 different lists
    pokemon_stats = [pokemon_stats[i * len(pokemon_stats) // (len(id_pokemon)): (i + 1) * len(pokemon_stats) // (len(id_pokemon))] for i in range(len(id_pokemon))]
    print(pokemon_stats)

get_pokemon_stats([6,4,5])