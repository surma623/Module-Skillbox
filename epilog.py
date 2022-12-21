import requests
import json
from typing import List, Dict, Tuple, Any


def get_planets_data_from_api() -> List[Dict[str, str]]:
    """Функция, создающая список словарей, которые содержат данные о планетах (название планеты и количество ее
     население) вселенной "Звездных воин".

    :return: Список словарей с данными о планетах
    """
    flag = True
    planets_data = list()
    response_from_api = requests.get('http://swapi.dev/api/planets/?page=').json()

    while True:

        for index in range(len(response_from_api['results'])):
            data_planet_dict = dict()
            data_planet_dict['name'] = response_from_api['results'][index]['name']
            data_planet_dict['population'] = response_from_api['results'][index]['population']
            planets_data.append(data_planet_dict)

        if not response_from_api['next']:
            flag = False

        if not flag:
            break

        response_from_api = requests.get(response_from_api['next']).json()

    return planets_data


def get_planet_by_max_population(planets: List[Dict[str, str]]) -> Tuple[str, int]:
    """Функция, возвращающая словарь с данными о самой заселенной планете вселенной "Звездных воин".

    :param:
        planets_info: список словарей с данными о планетах

    :return: кортеж с именем планеты и количеством ее населения
    """
    population_planet = 0
    planet_name = ''
    for planet in planets:
        if planet['population'] == 'unknown':
            continue
        elif population_planet < int(planet['population']):
            population_planet = int(planet['population'])
            planet_name = planet['name']

    return planet_name, population_planet


def save_planet_to_json(planet: Dict[str, Any], output_filename: str) -> None:
    """Функция, стерилизующая данные о самой заселенной планете вселенной "Звездных воин" в json-файл.

      :param:
          planet_name: название планеты
          data_planets_seq: список словарей с данными о планетах
      """

    with open(output_filename, 'w') as file:
        json.dump(planet, file)


def represent_planet(planet: Dict[str, Any]) -> None:
    """Функция, выводящая на экран самую густонаселенную планету вселенной "Звездных войн"."""

    print('Самая густонаселенная планета определена.\n'
          'Название планеты: {0}, количество населения: {1}'.format(
           planet['name'],
           planet['population']
          ))


max_populated_planet = dict()
filename = 'the_most_populated_planet.json'

if __name__ == "__main__":
    planets_data_seq = get_planets_data_from_api()
    max_populated_planet['name'], max_populated_planet['population'] = get_planet_by_max_population(planets_data_seq)
    save_planet_to_json(max_populated_planet, filename)
    represent_planet(max_populated_planet)

