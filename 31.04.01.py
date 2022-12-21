import requests
import json

my_req = requests.get('https://swapi.dev/api/people/3/')

data = json.loads(my_req.text)

data['name'] = 'Alexey'

with open('my_file.json', 'w') as file:
    json.dump(data, file, indent=4)

with open('my_file.json', 'r') as file:
    data = json.load(file)

print(data)
my_req_2 = requests.get(data['homeworld'])

print(my_req_2.text)

