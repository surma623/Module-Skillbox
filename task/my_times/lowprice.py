import json
import requests
from translate import Translator
from typing import List


def get_lowprice_hotel(search_info: List[str]):
    lst_hotels = list()

    name_city_eng = get_translate_text(search_info[0])
    print(name_city_eng)

    url = "https://hotels4.p.rapidapi.com/locations/v3/search"

    querystring = {"q": name_city_eng, "locale": "en_US", "langid": "1033", "siteid": "300000001"}

    headers = {
        "X-RapidAPI-Key": "658321e9b4msh17b5cf51d1ee298p1b8f09jsn473c3fb8945e",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response_location = requests.request("GET", url, headers=headers, params=querystring)

    response_location_dict = json.loads(response_location.text)

    location_id = get_location_id(response_location_dict)
    print(location_id)

    url = "https://hotels4.p.rapidapi.com/properties/v2/list"

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "destination": {"regionId": location_id},
        "checkInDate": {
            "day": 10,
            "month": 10,
            "year": 2022
        },
        "checkOutDate": {
            "day": 15,
            "month": 10,
            "year": 2022
        },
        "rooms": [
            {
                "adults": 2,
                "children": [{"age": 5}, {"age": 7}]
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 200,
        "sort": "PRICE_LOW_TO_HIGH",
        "filters": {"price": {
            "max": 300,
            "min": 100
        }}
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "658321e9b4msh17b5cf51d1ee298p1b8f09jsn473c3fb8945e",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    flag = False
    my_dict = {'id_hotel': None,
               'name_hotel': None,
               'distance_from_center': None,
               'cost_for_night': None}

    response_hotels_lst = requests.request("POST", url, json=payload, headers=headers)

    response_hotels_json = json.loads(response_hotels_lst.text)

    with open('file.json', 'w') as f:
        json.dump(response_hotels_json, f, indent=2)

    hotels_lst = find_lowprice_hotels(response_hotels_json, lst_hotels, flag, my_dict)
    print(hotels_lst)

    return name_city_eng


def get_translate_text(search_data: str) -> str:
    translator = Translator(from_lang='russian', to_lang='english')
    translation = translator.translate(search_data)
    print(translation)
    return translation


def get_location_id(location_dict) -> str:
    result = None

    if isinstance(location_dict, dict):
        for key, value in location_dict.items():
            if key == 'gaiaId':
                result = value
                return result
            elif isinstance(value, list):
                result = get_location_id(value)
            elif isinstance(value, dict):
                get_location_id(value)
    elif isinstance(location_dict, list):

        for elem in location_dict:
            if isinstance(elem, dict):
                result = get_location_id(elem)
                if result:
                    break
        else:
            result = None

    return result


def find_lowprice_hotels(hotels_json, lst_h, flag, my_dict):
    if isinstance(hotels_json, dict):
        for key, value in hotels_json.items():

            if key == 'propertySearchListings':
                flag = True
                find_lowprice_hotels(value, lst_h, flag, my_dict)
            elif isinstance(value, dict):
                find_lowprice_hotels(value, lst_h, flag, my_dict)
            elif value == 'Property' and flag:
                for key1, value1 in hotels_json.items():
                    if key1 == 'id':
                        my_dict['id_hotel'] = value1
                    elif key1 == 'name':
                        my_dict['name_hotel'] = value1
                        break
            elif key == "distanceFromMessaging":
                my_dict['distance_from_center'] = value

            elif key == "label":
                my_dict['cost_for_night'] = value
                my_dict_copy = my_dict.copy()
                lst_h.append(my_dict_copy)
                break

    elif isinstance(hotels_json, list):
        for elem in hotels_json:
            if isinstance(elem, dict):
                find_lowprice_hotels(elem, lst_h, flag, my_dict)

    print(lst_h)


get_lowprice_hotel(['Минск', '4', 'нет'])