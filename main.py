from config import POKEAPI_URL
import requests


def get_api_response(url: str):
    '''
    Gets the API information at a certain URL (endpoint)

    Parameters:
        - url: URL used to query the API

    Raises:
        - SystemExit: Prints an error and calls sys.exit based on the requests 

    Returns:
        - response.json(): Response from the API in JSON format
    '''

    try:
        response = requests.get(url)
        return response.json()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


def question_1():
    '''
    Gets the number of Pokémon that contain in their names the substring "at" and have 2 "a" (including the first "a" of the "at").
    
    Parameters:
        None

    Returns:
        - match_pattern: Number of Pokémon whose names match the pattern
    '''

    # Gets the total number of Pokémon from the json response
    json_response = get_api_response(POKEAPI_URL + 'pokemon')
    number_pokemons = json_response['count']

    # Sets a list of all Pokémon obtained from the json response
    json_response_pokemons = get_api_response(POKEAPI_URL + 'pokemon/?limit='+str(number_pokemons))
    pokemons = json_response_pokemons['results']

    # Iterates over each Pokémon in the list and validates whether the name of the Pokémon matches the pattern
    match_pattern = 0
    for pokemon in pokemons:
        pokemon_name = str(pokemon['name'])
        match_pattern += 'at' in pokemon_name and pokemon_name.count('a') == 2

    # Returns the result
    return match_pattern


def question_2(pokemon_name: str):
    '''
    Gets the number of Pokémon species that the current Pokémon can breed with.
    The default Pokémon is Raichu.
    2 Pokémon can breed if they are in the same egg group.
    
    Parameters:
        - pokemon_name: Name of the Pokémon to query
    
    Returns:
        - pokemon_species_set_length: Number of Pokémon species with which the Pokémon can breed with
    '''

    # Gets the information of the Pokémon from the json response
    json_response = get_api_response(POKEAPI_URL + 'pokemon/' + pokemon_name)
    json_response_pok_species = get_api_response(json_response['species']['url'])
    
    # Gets the egg_groups of the Pokémon and creates a set to store non-duplicate Pokémon
    pokemon_egg_groups = json_response_pok_species['egg_groups']
    pokemon_species_set = set()

    # Iterates over the egg_groups of the Pokémon and get the Pokémon species of each egg_group
    for egg_group in pokemon_egg_groups:
        json_egg_group = get_api_response(egg_group['url'])
        pokemon_species = json_egg_group['pokemon_species']

        # Adds to the set the names of each Pokémon without duplicates and without the queried Pokémon
        for pokemon in pokemon_species:
            if pokemon['name'] != pokemon_name:
                pokemon_species_set.add(pokemon['name'])

    # Gets the length of the set and returns it
    return len(pokemon_species_set)


def question_3(pokemon_type: str, id: int):
    '''
    Gets the maximum and minimum weight of Pokémon of a certain type and of a certain generation which implies that the id is less or equal than a certain value.
    By default the type is set to "fighting", the generation 1 which implies the id value to be "151".

    Parameters:
        - pokemon_type: Pokémon type
        - id: Maximum id to be included

    Returns:
        - max_min_weights: List containing the maximum and minimum weight of Pokémon that meet the conditions
    '''

    # Gets the Pokémon found in the requested type
    json_response = get_api_response(POKEAPI_URL + 'type/' + pokemon_type)
    pokemon_response_type = json_response['pokemon']

    # Sets a list where the weights of Pokémon that meet the conditions will be stored
    pokemon_weights = []

    # Iterates over each Pokémon obtained from the requested type and validates through 
    # the information of each Pokémon if it meets the id condition
    for pokemon in pokemon_response_type:
        pokemon_name = pokemon['pokemon']['name']
        pokemon_id = int(str(pokemon['pokemon']['url']).split('/')[-2])
        if pokemon_id <= id:
            pokemon_info = get_api_response(POKEAPI_URL + 'pokemon/' + pokemon_name)
            pokemon_weights.append(pokemon_info['weight'])

    
    # Sets a list with the maximum and minimum weight of the pokemon_weights list and returns it
    max_min_weights = [max(pokemon_weights), min(pokemon_weights)]
    return max_min_weights

if __name__ == '__main__':
   print(question_1())
   print(question_2('raichu'))
   print(question_3('fighting', 151))