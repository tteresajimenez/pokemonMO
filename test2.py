import requests

url_evolution = "https://pokeapi.co/api/v2/evolution-chain/"

evolution_chain_id = input("Ingrese el ID de la cadena de evolucion que desea: ")
pokemon_evolution_url = url_evolution + evolution_chain_id
data = requests.get(pokemon_evolution_url).json()
chain = data.get("chain")


def get_pokemon_evolution(chain):
    """Returns two lists: name and the url of the pokemons in the evolution chain"""
    dictionary_chain = [chain]
    if chain.get('evolves_to') is not None:
        pokemon_name = [chain.get("species").get("name")]
        pokemon_url = [chain.get("species").get("url")]
