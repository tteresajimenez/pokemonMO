from django.core.management.base import BaseCommand, CommandError
import re
import requests
import pprint
from pokemon_api.models import Pokemon, Stats, EvolutionChain

URL_EVOLUTION = "https://pokeapi.co/api/v2/evolution-chain/"
URL_POKEMON = "https://pokeapi.co/api/v2/pokemon/"


class Command(BaseCommand):
    help = 'With this command you can insert one ID to show the details of an specific pokemon evolution chain'

    def add_arguments(self, parser):
        parser.add_argument('id_input', type=int, help='ID representing the Evolution Chain')

    def handle(self, *args, **options):
        if int(options['id_input']):
            chain_id = str(options['id_input'])
            save_pokemon_info(chain_id)
        else:
            raise CommandError('Please insert a number')


def save_pokemon_info(chain_id):
    """Main funtion that shows and saves the pokemon information"""
    pokemon_evolution_url = URL_EVOLUTION + chain_id
    data = requests.get(pokemon_evolution_url).json()
    chain = data.get("chain")
    pokemon_list, pokemon_url = get_pokemon_name_and_url(chain)
    id_pokemon = take_pokemon_id(pokemon_url)
    pokemon_height, pokemon_weight = pokemon_height_weight(id_pokemon)
    id_evolution = fill_id_evolution_chain(id_pokemon,data)
    pokemon_stats = get_pokemon_stats(id_pokemon)

    value_stats = []
    for item in pokemon_stats:
        value_stats.append(take_list_first_item(item))

    pokemon_number_in_chain = len(id_pokemon)
    print(id_evolution)
    evolution_instance = EvolutionChain(
        id_evolution_chain=data['id'],
        name_poke='hello'
    )
    evolution_instance.save()
    try:
        while pokemon_number_in_chain >= 1:
            pokemon_number_in_chain -= 1

            pokemon_instance = Pokemon(
                id_pokemon=id_pokemon[pokemon_number_in_chain],
                id_evolution_fk=evolution_instance,
                name=pokemon_list[pokemon_number_in_chain],
                weight=pokemon_weight[pokemon_number_in_chain],
                height=pokemon_height[pokemon_number_in_chain]
            )
            pokemon_instance.save()

            stats_instance = Stats(
                id_pokemon_fk=pokemon_instance,
                speed=pokemon_stats[pokemon_number_in_chain][0],
                special_defense=value_stats[pokemon_number_in_chain][1],
                special_attack=value_stats[pokemon_number_in_chain][2],
                defense=value_stats[pokemon_number_in_chain][3],
                attack=value_stats[pokemon_number_in_chain][4],
                hp=value_stats[pokemon_number_in_chain][5]
            )
            stats_instance.save()
    except:
        print('ERROR that pokemon is already save on db')
    else:
        print('Success')

    while pokemon_number_in_chain >= 0:
        pokemon_number_in_chain = pokemon_number_in_chain - 1
        pokemon_info = {
            'id_pokemon': id_pokemon[pokemon_number_in_chain],
            'name': pokemon_list[pokemon_number_in_chain],
            'weight': pokemon_weight[pokemon_number_in_chain],
            'height': pokemon_height[pokemon_number_in_chain],
            'evolution_chain': data['id'],
            'stats': { 'speed': value_stats[pokemon_number_in_chain][0],
                       'special_defense': value_stats[pokemon_number_in_chain][1],
                       'special_attack': value_stats[pokemon_number_in_chain][2],
                       'defense': value_stats[pokemon_number_in_chain][3],
                       'attack': value_stats[pokemon_number_in_chain][4],
                       'hp': value_stats[pokemon_number_in_chain][5],
            }

        }
        pprint.pprint(pokemon_info)

def get_pokemon_name_and_url(chain):
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


def pokemon_height_weight(id_pokemon):
    """Returns a list of heights and weights of the pokemons"""
    pokemon_height = []
    pokemon_weight = []
    for item in id_pokemon:
        pokemon_characteristics_url = URL_POKEMON + item
        data = requests.get(pokemon_characteristics_url).json()
        pokemon_height.append(data['height'])
        pokemon_weight.append(data['weight'])
    return pokemon_height, pokemon_weight


def get_pokemon_stats(id_pokemon):
    """Returns a list with the stats of the pokemon in the chain"""
    all_stats = []
    pokemon_stats = []
    num_stats = 5
    for item in id_pokemon:
        pokemon_characteristics_url = URL_POKEMON + item
        data = requests.get(pokemon_characteristics_url).json()
        all_stats.append(data.get("stats"))
        num_stats = 5
        while num_stats >= 0:
            pokemon_stats.append(data['stats'][num_stats]['base_stat'])
            pokemon_stats.append(data['stats'][num_stats]['stat']['name'])
            num_stats = num_stats - 1

        # It creates sublist based on the stats and their value
    pokemon_stats = [pokemon_stats[
                     i * len(pokemon_stats) // (len(pokemon_stats) // 2): (i + 1) * len(pokemon_stats) // (
                                 len(pokemon_stats) // 2)] for i in range((len(pokemon_stats) // 2))]
    # It creates 3 different lists
    pokemon_stats = [
        pokemon_stats[i * len(pokemon_stats) // (len(id_pokemon)): (i + 1) * len(pokemon_stats) // (len(id_pokemon))]
        for i in range(len(id_pokemon))]
    return pokemon_stats

def take_list_first_item(any_list):
    """It returns the first item on a nested list """
    list2 = []
    for item in any_list:
        list2.append(item[0])
    return list2

def fill_id_evolution_chain(id_pokemon, data):
    id_evolution = []
    VARIABLE_TO_ITERATE = len(id_pokemon)
    while VARIABLE_TO_ITERATE >= 1:
        VARIABLE_TO_ITERATE -= 1
        id_evolution.append(data['id'])
    return id_evolution
