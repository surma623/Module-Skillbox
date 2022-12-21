import requests
import json


address_api = 'http://swapi.dev/api/planets/'
request = requests.get(address_api)
print(request.text)
data = json.loads(request.text)
number_of_planets = data['count']
lst_for_dicts_of_info_of_planets = list()
for num in range(6):
    req = requests.get('http://swapi.dev/api/planets/?page=3')
    data_of_planet_dict = json.loads(req.text)
    print(data_of_planet_dict)
    info_of_planet_dict = dict()
    info_of_planet_dict['name'] = data_of_planet_dict['name']
    info_of_planet_dict['population'] = data_of_planet_dict['population']
    lst_for_dicts_of_info_of_planets.append(info_of_planet_dict)






