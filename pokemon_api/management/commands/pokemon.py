from django.core.management.base import BaseCommand, CommandError
import re
import requests
import pprint
from pokemon_api.models import Pokemon

url_evolution = "https://pokeapi.co/api/v2/evolution-chain/"
url_pokemon = "https://pokeapi.co/api/v2/pokemon/"


class Command(BaseCommand):
    help = 'With this command you can insert one ID to show the details of an specific pokemon evolution chain'

    def add_arguments(self, parser):
        parser.add_argument('id_input', type=int, help='ID representing the Evolution Chain')

    def handle(self, *args, **options):
        if int(options['id_input']):
            pokemon_evolution_url = url_evolution + str(options['id_input'])
            data = requests.get(pokemon_evolution_url).json()
            chain = data.get("chain")
            pokemon_list, pokemon_url = get_pokemon_evolution(chain)
            id_pokemon = take_pokemon_id(pokemon_url)
            evolves_to = pokemon_evolves(pokemon_list)
            pokemon_height, pokemon_weight = pokemon_height_weight(id_pokemon)
            pokemon_stats = get_pokemon_stats(id_pokemon)
            poke_stats1, poke_stats2, poke_stats3 = pokemon_stats[0], pokemon_stats[1], pokemon_stats[2]
            poke_stats1 = take_list_first_item(poke_stats1), take_list_first_item(poke_stats2), take_list_first_item(
                poke_stats3)

            # Info that is show on the console
            count = 2
            while count >= 0:
                count = count - 1
                pokemon_info = {
                    'id_pokemon': id_pokemon[count],
                    'name': pokemon_list[count],
                    'weight': pokemon_weight[count],
                    'height': pokemon_height[count],
                    'stats': pokemon_stats[count],
                    'evolution': evolves_to[count]
                }
                pprint.pprint(pokemon_info)

            # Adding information into de DB
            count = 2
            while count >= 0:
                count = count - 1
                pokemon_info_db = Pokemon(
                    id_pokemon=id_pokemon[count],
                    name=pokemon_list[count],
                    weight=pokemon_weight[count],
                    height=pokemon_height[count],
                    speed=poke_stats1[count][0],
                    special_defense=poke_stats1[count][1],
                    special_attack=poke_stats1[count][2],
                    defense=poke_stats1[count][3],
                    attack=poke_stats1[count][4],
                    hp=poke_stats1[count][5],
                    evolution=evolves_to[count]
                )
                pokemon_info_db.save()
                # print('Save with success')
        else:
            raise CommandError('Please insert a number')


def get_pokemon_evolution(chain):
    """Returns two lists: name and the url of the pokemons in the evolution chain"""
    pokemon_name = [chain.get("species").get("name")]
    pokemon_url = [chain.get("species").get("url")]
    pokemon_name2 = chain.get("evolves_to")
    while len(pokemon_name2) != 0:
        pokemon_name2 = pokemon_name2[0]
        pokemon_name.append(pokemon_name2.get("species").get("name"))
        pokemon_url.append(pokemon_name2.get("species").get("url"))
        pokemon_name2 = pokemon_name2.get("evolves_to")
    return pokemon_name, pokemon_url


def take_pokemon_id(pokemon_url):
    """Returns a list with the id of the pokemon based on the url"""
    temporal_id_list = []
    id_list = []
    # find all the numbers on the url
    for item in pokemon_url:
        temporal_id_list.append(re.findall(r"\d+", item))
    # all of they have 2 numbers so we erase the first one that is the version
    for item in temporal_id_list:
        item.pop(0)
    for i in range(len(temporal_id_list)):
        id_list.extend(temporal_id_list[i])

    return id_list


def pokemon_evolves(pokemon_list):
    """It returns a list with the names of the pokemon in the order that is next on the evolution chain"""
    evolves_to = []
    for item in reversed(pokemon_list):
        evolves_to.append(item)
    evolves_to[2] = 'None'
    evolves_to[0], evolves_to[1] = evolves_to[1], evolves_to[0]
    return evolves_to


def pokemon_height_weight(id_pokemon):
    """Returns a list of heights and weights of the pokemons"""
    pokemon_height = []
    pokemon_weight = []
    for item in id_pokemon:
        pokemon_characteristics_url = url_pokemon + item
        data = requests.get(pokemon_characteristics_url).json()
        pokemon_height.append(data['height'])
        pokemon_weight.append(data['weight'])
    return pokemon_height, pokemon_weight


def get_pokemon_stats(id_pokemon):
    """Returns a list with the stats of the pokemos in the chain"""
    all_stats = []
    pokemon_stats = []
    num_stats = 5
    for item in id_pokemon:
        pokemon_characteristics_url = url_pokemon + item
        data = requests.get(pokemon_characteristics_url).json()
        all_stats.append(data.get("stats"))
        num_stats = 5
        while num_stats >= 0:
            pokemon_stats.append(data['stats'][num_stats]['base_stat'])
            pokemon_stats.append(data['stats'][num_stats]['stat']['name'])
            num_stats = num_stats - 1

    pokemon_stats = [pokemon_stats[i * len(pokemon_stats) // 18: (i + 1) * len(pokemon_stats) // 18] for i in range(18)]
    pokemon_stats = [pokemon_stats[i * len(pokemon_stats) // 3: (i + 1) * len(pokemon_stats) // 3] for i in range(3)]
    return pokemon_stats


def take_list_first_item(lista):
    """It returns the first item on a nested list """
    list2 = []
    for item in lista:
        list2.append(item[0])
    return list2
