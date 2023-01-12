import os
import telebot
import requests
from dotenv import load_dotenv
import json
from typing import Optional, Any, List, Dict, Tuple
from datetime import datetime
from googletrans import Translator
import verification
import history
from user import User


def translate_name_city(name_city: str) -> str:
    """Функция, которая переводит название города на английский язык .

    :param:
        name_city: название города для перевода.
    :return:
        перевод названия города.
    """
    # Есть города, которые библиотека googletrans неправильно переводит, город Марсель один
    # из них, по мере использования бота можно отлавливать такие случаи и делать переводы отдельных городов вручную.

    if name_city == 'марсель':
        return 'Marseille'
    else:
        translator = Translator()
        translation = translator.translate(name_city, src='ru', dest='en')
        return translation.text


def get_api_request(method_request, url: str, headers: dict, querystring: dict) -> Optional[dict]:
    """
    Функция совершающая отправку запроса к API.

    :param:
        method_request: метод запроса
        url: url запроса
        headers: заголовки запроса в формате словаря
        querystring: параметр запроса в формате словаря.
    :return:
        десериализованные данные либо None при отсутствии города в данных от API
    :exception:
       requests.Timeout: вызывается в случае, если сервер не отвечает на запрос в течении установленного времени
       requests.RequestException: вызывается в случае любой другой ошибки при попытке отправки запроса и получения
       ответа с сервера
    """
    try:
        if method_request == "GET":
            response = requests.request(method_request, url, headers=headers, params=querystring, timeout=20)
        else:
            response = requests.request(method_request, url, json=querystring, headers=headers, timeout=20)

        if response.status_code == 200:
            result = json.loads(response.text)
        else:
            result = None

    except requests.Timeout:
        result = None
    except requests.RequestException:
        result = None

    return result


def make_location_search_api_request(name_city: str) -> Optional[dict]:
    """ Функция, которая формирует параметры запроса информации о городе к API.

    :param:
        name_city: название города.
    :return:
       десериализованные данные либо None при отсутствии города в данных от API
    """
    method_request = "GET"
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"
    querystring = {"q": name_city, "locale": "en_US", "langid": "1033", "siteid": "300000001"}
    headers = {
        "X-RapidAPI-Key": rapid_api_key,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    return get_api_request(method_request=method_request, url=url, headers=headers, querystring=querystring)


def make_hotel_list_api_request(city_id: str, check_in: List[str], check_out: List[str],
                                price_range: Tuple[int, int]) -> Optional[dict]:
    """ Функция, которая формирует параметры запроса информации об отелях в городе к API.

    :param:
        city_id: id города
        check_in: дата заезда
        check_out: дата отъезда.
    :return:
         десериализованные данные либо None при отсутствии информации об отелях в городе в данных от API
    """

    url = "https://hotels4.p.rapidapi.com/properties/v2/list"
    method_request = "POST"
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "destination": {"regionId": city_id},
        "checkInDate": {
            "day": int(check_in[2]),
            "month": int(check_in[1]),
            "year": int(check_in[0])
        },
        "checkOutDate": {
            "day": int(check_out[2]),
            "month": int(check_out[1]),
            "year": int(check_out[0])
        },
        "rooms": [
            {
                "adults": 2,
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 200,
        "sort": "PRICE_LOW_TO_HIGH",
        "filters": {"price": {
            "max": price_range[1],
            "min": price_range[0]
        }}
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": rapid_api_key,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    return get_api_request(method_request=method_request, url=url, headers=headers, querystring=payload)


def make_detail_hotel_api_request(id_hotel: str) -> Optional[dict]:
    """ Функция, которая формирует параметры запроса информации об конкретном отеле к API.

        :param:
            id_hotel: id отеля
        :return:
          десериализованные данные либо None при отсутствии информации о конкретном отеле в данных от API
        """

    url = "https://hotels4.p.rapidapi.com/properties/v2/detail"
    method_request = "POST"
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": id_hotel
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": rapid_api_key,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    return get_api_request(method_request=method_request, url=url, headers=headers, querystring=payload)


def search_city_id(user: User, location_data: Any) -> None:
    """Функция, совершающая поиск id города в полученных данных из API.

    :param:
        location_data: данные города в формате словаря.
    :return:
        id города и None в случае, если полученные данные не содержат id города.
    """

    if isinstance(location_data, dict):
        for key, value in location_data.items():
            if key == 'gaiaId':
                user.city_id = value
                break
            elif isinstance(value, list):
                search_city_id(user, value)

    elif isinstance(location_data, list):
        for elem in location_data:
            if isinstance(elem, dict):
                search_city_id(user, elem)
                if user.city_id:
                    break


def get_hotels(places_city: Any, hotel_info: Dict, user: User) -> None:
    """Функция, осуществляющая сбор информации об отелях в городе из данных от API

    :param:
        places_city: данные о различных местах в городе от API
        hotel_info: словарь для записи данных об отелях
        key_flag: флаг сигнализирующий о нахождении нужного ключа (становится True)
        user: объект класса User, содержащий данные об вводимой пользователем информации
    """

    if isinstance(places_city, dict):
        for key, value in places_city.items():
            if isinstance(value, dict):
                get_hotels(value, hotel_info, user)
            elif isinstance(value, list):
                get_hotels(value, hotel_info, user)
            if key == 'propertySearchListings':
                user.found_needed_flag = True
                get_hotels(value, hotel_info, user)
            elif value == 'Property' and user.found_needed_flag:
                for nested_key, nested_value in places_city.items():
                    if nested_key == 'id':
                        hotel_info['id_hotel'] = nested_value
                        hotel_info['URL'] = f'https://www.hotels.com/h{nested_value}.Hotel-Information'
                    elif nested_key == 'name':
                        hotel_info['name_hotel'] = nested_value
                        break
            elif key == 'distanceFromDestination' and user.found_needed_flag:
                for nested_key, nested_value in value.items():
                    if nested_key == 'value':
                        hotel_info['distance_from_center'] = str(nested_value)
            elif key == 'lead' and isinstance(value, dict) and user.found_needed_flag:
                for nested_key, nested_value in value.items():
                    if nested_key == 'formatted':
                        hotel_info['cost_for_day'] = nested_value
                        break
            elif value == 'LodgingEnrichedMessage' and user.found_needed_flag:
                for nested_key, nested_value in places_city.items():
                    if nested_key == 'value':
                        total_cost = ''
                        for symbol in nested_value:
                            if symbol.isdigit() or symbol == '$' or symbol == ',':
                                total_cost += symbol
                        hotel_info['total_cost'] = total_cost
                        break
                hotel_info_copy = hotel_info.copy()
                if user.user_command == '/lowprice':
                    if len(user.hotel_data) < user.hotels_count:
                        user.hotel_data.append(hotel_info_copy)
                elif user.user_command == '/highprice' or user.user_command == '/bestdeal':
                    user.hotel_data.append(hotel_info_copy)
                else:
                    print('Impossible.')
                break

    elif isinstance(places_city, list):
        for elem in places_city:
            if isinstance(elem, dict):
                get_hotels(elem, hotel_info, user)


def sort_distance(user: User) -> None:
    """Функция, сортирующая отели по дистанции от центра города.

    :param:
        user: объект класса User, содержащий данные об вводимой пользователем информации
    """

    sorted_distance_list = list()

    for hotel in user.hotel_data:
        if user.distance_range[0] <= float(hotel['distance_from_center']) <= user.distance_range[1]:
            sorted_distance_list.append(hotel)

    user.hotel_data = sorted_distance_list


def remove_unnecessary_hotels(user: User) -> None:
    """Функция, удаляющая лишние отели (словари с данными) из списка отелей города.

    :param:
        user: объект класса User, содержащий данные об вводимой пользователем информации
    """
    # В цикле удаляются отели начиная с начала списка, таким образом, в списке остаются только самые дорогие отели.
    if user.user_command == '/highprice':
        while len(user.hotel_data) > user.hotels_count:
            del user.hotel_data[0]
    # В цикле удаляются отели с конца списка, таким образом, в списке остаются только самые дешевые отели.
    elif user.user_command == '/bestdeal':
        while len(user.hotel_data) > user.hotels_count:
            user.hotel_data.pop()
    else:
        print('Impossible')


def get_hotel_details(detail_hotel, user, index) -> None:
    if isinstance(detail_hotel, dict):
        for key, value in detail_hotel.items():
            if key == 'staticImage':
                continue
            elif isinstance(value, dict):
                get_hotel_details(value, user, index)
            elif isinstance(value, list):
                get_hotel_details(value, user, index)
            elif key == 'address':
                get_hotel_details(value, user, index)
            elif key == 'addressLine':
                user.hotel_data[index]['hotel_address'] = value
            elif user.hotel_data[index]['hotel_address'] is not None and user.getting_photos:
                if key == 'image':
                    get_hotel_details(value, user, index)
                elif key == 'url':
                    if len(user.hotel_data[index]['hotel_photos']) < user.photos_count:
                        user.hotel_data[index]['hotel_photos'].append(value)

    elif isinstance(detail_hotel, list):
        for elem in detail_hotel:
            if isinstance(elem, dict):
                get_hotel_details(elem, user, index)


def get_search_result(user: User) -> None:
    """Функция, осуществляющая сбор всей необходимой информации об отелях в указанном пользователем городе.

    :param:
        user: объект класса User, содержащий данные об вводимой пользователем информации
        hotel_data Dict: словарь для хранения данных об отеле
        needed_key_flag bool: флаг сигнализирующий о нахождении нужного ключа (становится True), необходим для функции
        get_hotels_list
    """
    hotel_data = {'id_hotel': None,
                  'URL': None,
                  'name_hotel': None,
                  'distance_from_center': None,
                  'cost_for_day': None,
                  'total_cost': None,
                  'hotel_address': None
                  }
    user.found_needed_flag = False

    places_city_dict = make_hotel_list_api_request(city_id=user.city_id, check_in=user.check_in.split('-'),
                                                   check_out=user.check_out.split('-'), price_range=user.price_range)

    get_hotels(places_city=places_city_dict, hotel_info=hotel_data, user=user)

    bot.send_message(chat_id=user.chat_id, text='Осталось совсем чуть-чуть😇😇.')

    if user.user_command == '/bestdeal':
        sort_distance(user=user)

    if len(user.hotel_data) > user.hotels_count:
        remove_unnecessary_hotels(user=user)

    for index_dict, hotel_dict in enumerate(user.hotel_data):

        detail_hotel_dict = make_detail_hotel_api_request(id_hotel=hotel_dict['id_hotel'])

        if user.getting_photos:
            user.hotel_data[index_dict]['hotel_photos'] = list()
        get_hotel_details(detail_hotel=detail_hotel_dict, user=user, index=index_dict)


load_dotenv()
bot_token = os.getenv('BOT_TOKEN')
rapid_api_key = os.getenv('RAPIDAPI_KEY')
bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start'])
def to_start(message: telebot.types.Message) -> None:
    """Функция, обрабатывающая введенную пользователем команду /start

    :param:
        message: объект класса telebot
    """
    if message.chat.id not in User.all_users:
        User(message.chat.id)

    bot.send_message(message.chat.id, 'Здравствуйте, <b>{name}</b>! Вас приветствует <b>Travel_guid_bot</b>!👋'
                                      ' Я помогу Вам выбрать отель для отдыха.☀️🏝⛱✈️\n'
                                      'У меня вы можете узнать:\n'
                                      '🔹топ самых дешёвых отелей в городе (команда /lowprice);\n'
                                      '🔹топ самых дорогих отелей в городе (команда /highprice);\n'
                                      '🔹топ отелей, наиболее подходящих по цене и расположению от центра'
                                      ' (самые дешёвые и находятся ближе всего к центру) (команда /bestdeal);\n'
                                      '🔹историю поиска отелей (команда /history);\n'
                                      '🔹доступные для выполнения команды (команда /help).'.format(
                                       name=message.from_user.first_name), parse_mode='HTML')


@bot.message_handler(commands=['help'])
def get_help(message: telebot.types.Message) -> None:
    """Функция, обрабатывающая введенную пользователем команду /help

    :param:
        message: объект класса telebot
    """
    bot.send_message(message.chat.id, 'У меня вы можете узнать:\n'
                                      '🔹топ самых дешёвых отелей в городе (команда /lowprice);\n'
                                      '🔹топ самых дорогих отелей в городе (команда /highprice);\n'
                                      '🔹топ отелей, наиболее подходящих по цене и расположению от центра'
                                      '(самые дешёвые и находятся ближе всего к центру) (команда /bestdeal);\n'
                                      '🔹историю поиска отелей (команда /history);\n'
                                      '🔹доступные для выполнения команды (команда /help).', parse_mode='HTML')


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def get_prices_message(message: telebot.types.Message) -> None:
    """Функция, обрабатывающая одну из введенных пользователем команд: /lowprice, /highprice, /bestdeal.

    :param:
        message: объект класса telebot
    """
    user = User.get_user(message.from_user.id)
    user.chat_id = message.chat.id
    user.datetime_input_command = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
    if message.text == '/lowprice':
        user.price_range = (1, 100)
        user.user_command = message.text
        bot.send_message(message.chat.id, 'Отлично, <b>{name}</b>!😇 Сейчас я помогу Вам найти'
                                          ' топ самых дешёвых отелей в городе.😎👌'
                                          ' Пожалуйста, введите город для поиска.'.format(
                                           name=message.from_user.first_name), parse_mode='HTML')

    elif message.text == '/highprice':
        user.price_range = (100, 10000)
        user.user_command = message.text
        bot.send_message(message.chat.id, 'Отлично, <b>{name}</b>!😇 Сейчас я помогу Вам найти'
                                          ' топ самых дорогих отелей в городе.😎👌'
                                          ' Пожалуйста, введите город для поиска.'.format(
                                           name=message.from_user.first_name), parse_mode='HTML')

    else:
        user.user_command = message.text
        bot.send_message(message.chat.id, 'Отлично, <b>{name}</b>!😇 Сейчас я помогу Вам найти'
                                          ' топ отелей, наиболее подходящих по цене и расположению от центра '
                                          '(самые дешёвые и находятся ближе всего к центру).😎👌'
                                          ' Пожалуйста, введите город для поиска.'.format(
                                           name=message.from_user.first_name), parse_mode='HTML')

    bot.register_next_step_handler(message, get_city)


def get_city(message: telebot.types.Message) -> None:
    """Функция, регистрирующая данные из сообщения пользователя о городе, где необходимо искать отели.

    :param:
        message: объект класса telebot
    """
    try:
        user = User.get_user(message.from_user.id)
        user.city = translate_name_city(name_city=message.text.lower())
        search_city_id(user=user, location_data=make_location_search_api_request(name_city=user.city))

        if not user.city_id:
            bot.send_message(message.from_user.id, 'Неудача, <b>{name}</b>😳! Я не смог найти информацию'
                                                   ' по вашему городу!😢😢😢'
                                                   'Попробуйте, пожалуйста, еще раз.'.format(
                                                    name=message.from_user.first_name), parse_mode='HTML')
            bot.register_next_step_handler(message, get_city)

        else:
            if user.user_command == '/bestdeal':
                bot.send_message(message.from_user.id, 'Отлично, <b>{name}</b>👍😁😁! Теперь укажите, пожалуйста,'
                                                       ' ценовой диапазон поиска (от $1 до $100).\n'
                                                       'Пример ввода: <b>10</b>, <b>100</b>.'.format(
                                                        name=message.from_user.first_name),
                                 parse_mode='HTML')

                bot.register_next_step_handler(message, get_price_range)

            else:
                bot.send_message(message.from_user.id, 'Отлично, <b>{name}</b>👍😁😁! Теперь скажите, пожалуйста,'
                                                       ' с какого по какое число Вы'
                                                       ' будете проживать в отеле? Диапазон времени планируемого '
                                                       'проживания в отеле не должен превышать <b>28 дней</b>.\n'
                                                       'Формат ввода: <b>ГГГГ-ММ-ДД</b>, <b>ГГГГ-ММ-ДД</b>.'.format(
                                                        name=message.from_user.first_name),
                                 parse_mode='HTML')

                bot.register_next_step_handler(message, get_date)
    except TypeError:
        bot.send_message(message.from_user.id, 'Город введен некорректно😳. Попробуйте еще раз.')
        bot.register_next_step_handler(message, get_city)


def get_price_range(message: telebot.types.Message) -> None:
    """Функция, регистрирующая данные из сообщения пользователя о диапазоне цен как одного из критериев поиска
     нужных отелей.

    :param:
        message: объект класса telebot
    """
    user = User.get_user(message.from_user.id)

    try:
        min_price = message.text.split(', ')[0]
        max_price = message.text.split(', ')[1]

        if not verification.is_price_valid(price=float(min_price)):
            bot.send_message(message.chat.id, 'Неудача, <b>{name}</b>!😳 Вы ввели некорректный диапазон цен!'
                                              ' Попробуйте, пожалуйста, еще раз.'.format(
                                                name=message.from_user.first_name),
                             parse_mode='HTML')
            bot.register_next_step_handler(message, get_price_range)
        elif not verification.is_price_valid(price=float(max_price)):
            bot.send_message(message.chat.id, 'Неудача, <b>{name}</b>!😳 Вы ввели некорректный диапазон цен!'
                                              ' Попробуйте, пожалуйста, еще раз.'.format(
                                                name=message.from_user.first_name),
                             parse_mode='HTML')
            bot.register_next_step_handler(message, get_price_range)
        else:
            if verification.is_range_price_valid(min_p=float(min_price), max_p=float(max_price)):
                user.price_range = (float(min_price), float(max_price))
                bot.send_message(message.from_user.id, 'Замечательно, <b>{name}</b>👍😁😁! Теперь введите, пожалуйста,'
                                                       ' диапазон расстояния (в случае необходимости'
                                                       ' через десятичную точку, но не запятую),'
                                                       ' на котором отель находится от центра города (от <b>0.1</b> до'
                                                       ' <b>50</b> миль (nm)).\nПример ввода: <b>1</b>,'
                                                       ' <b>19.5</b>.'.format(name=message.from_user.first_name),
                                 parse_mode='HTML')
                bot.register_next_step_handler(message, get_distance_range)

            else:
                bot.send_message(message.chat.id, 'Неудача, <b>{name}</b>!😳 Вы ввели некорректный диапазон цен!'
                                                  ' Попробуйте, пожалуйста, еще раз.'.format(
                                                    name=message.from_user.first_name),
                                 parse_mode='HTML')
                bot.register_next_step_handler(message, get_price_range)
    except ValueError:
        bot.send_message(message.chat.id, 'Неудача, <b>{name}</b>😳! Введите числовые значения.'
                                          ' Пример ввода: <b>10</b>, <b>100</b>.'.format(
                                            name=message.from_user.first_name),
                         parse_mode='HTML')
        bot.register_next_step_handler(message, get_price_range)
    except IndexError:
        bot.send_message(message.chat.id, 'Неудача, <b>{name}</b>😳! Неверный формат ввода.'
                                          ' Пример ввода: <b>10</b>, <b>100</b>.'.format(
                                            name=message.from_user.first_name),
                         parse_mode='HTML')
        bot.register_next_step_handler(message, get_price_range)


def get_distance_range(message: telebot.types.Message) -> None:
    """Функция, регистрирующая данные из сообщения пользователя о диапазоне расстояния как одного из критериев поиска
     нужных отелей.

    :param:
        message: объект класса telebot
    """
    user = User.get_user(message.from_user.id)

    try:
        start_point_distance = message.text.split(', ')[0]
        end_point_distance = message.text.split(', ')[1]
        if not verification.is_distance_valid(distance=float(start_point_distance)):
            bot.send_message(message.chat.id, 'Неудача, <b>{name}</b>!😳 Вы ввели некорректный диапазон расстояния!'
                                              ' Попробуйте, пожалуйста, еще раз.'.format(
                                                name=message.from_user.first_name),
                             parse_mode='HTML')
            bot.register_next_step_handler(message, get_distance_range)
        elif not verification.is_distance_valid(distance=float(end_point_distance)):
            bot.send_message(message.chat.id, 'Неудача, <b>{name}</b>!😳 Вы ввели некорректный диапазон расстояния!'
                                              ' Попробуйте, пожалуйста, еще раз.'.format(
                                                name=message.from_user.first_name),
                             parse_mode='HTML')
            bot.register_next_step_handler(message, get_distance_range)
        else:
            if verification.is_range_distance_valid(start_point=float(start_point_distance),
                                                    end_point=float(end_point_distance)):
                user.distance_range = (float(start_point_distance), float(end_point_distance))
                bot.send_message(message.from_user.id, 'Великолепно, <b>{name}</b>👍😁😁! Теперь скажите, пожалуйста,'
                                                       ' с какого по какое число Вы будете проживать в отеле? '
                                                       'Диапазон времени планируемого проживания в отеле не должен'
                                                       ' превышать <b>28 дней</b>.\n'
                                                       'Формат ввода: <b>ГГГГ-ММ-ДД</b>, <b>ГГГГ-ММ-ДД</b>.'.format(
                                                         name=message.from_user.first_name),
                                 parse_mode='HTML')

                bot.register_next_step_handler(message, get_date)

            else:
                bot.send_message(message.chat.id, 'Неудача, <b>{name}</b>!😳 Вы ввели некорректный диапазон расстояния!'
                                                  ' Попробуйте, пожалуйста, еще раз.'.format(
                                                    name=message.from_user.first_name),
                                 parse_mode='HTML')
                bot.register_next_step_handler(message, get_distance_range)

    except ValueError:
        bot.send_message(message.chat.id, 'Неудача, <b>{name}</b>😳! Введите числовые значения'
                                          ' (в случае необходимости через десятичную точку, но не запятую).'
                                          ' Пример ввода: <b>1</b>, <b>19.5</b>.'.format(
                                            name=message.from_user.first_name),
                         parse_mode='HTML')
        bot.register_next_step_handler(message, get_distance_range)
    except IndexError:
        bot.send_message(message.chat.id, 'Неудача, <b>{name}</b>😳! Неверный формат ввода.'
                                          ' Пример ввода: <b>1</b>, <b>19.5</b>.'.format(
                                            name=message.from_user.first_name),
                         parse_mode='HTML')
        bot.register_next_step_handler(message, get_distance_range)


def get_date(message: telebot.types.Message) -> None:
    """Функция, регистрирующая данные из сообщения пользователя о диапазоне планируемого пребывания в отеле.
    :param:
        message: объект класса telebot
    """

    user = User.get_user(message.from_user.id)
    try:
        user.check_in = message.text.split(', ')[0]
        user.check_out = message.text.split(', ')[1]
        if not verification.is_date_valid(date=user.check_in):
            bot.send_message(message.chat.id, 'Неудача, <b>{name}</b>!😳 Вы ввели некорректную дату заезда!'
                                              ' Попробуйте, пожалуйста, еще раз. Формат ввода: <b>ГГГГ-ММ-ДД</b>,'
                                              ' <b>ГГГГ-ММ-ДД</b>.'.format(name=message.from_user.first_name),
                             parse_mode='HTML')
            bot.register_next_step_handler(message, get_date)
        elif not verification.is_date_valid(date=user.check_out):
            bot.send_message(message.chat.id, 'Неудача, <b>{name}</b>!😳 Вы ввели некорректную дату отъезда!'
                                              ' Попробуйте, пожалуйста, еще раз. Формат ввода: <b>ГГГГ-ММ-ДД</b>,'
                                              ' <b>ГГГГ-ММ-ДД</b>.'.format(name=message.from_user.first_name),
                             parse_mode='HTML')
            bot.register_next_step_handler(message, get_date)

        else:
            valid_range_date = verification.is_range_date_valid(date_check_in=user.check_in.split('-'),
                                                                date_check_out=user.check_out.split('-'),
                                                                user=user)
            if not user.block_choose_date and not valid_range_date:
                bot.send_message(message.chat.id, 'Неудача, <b>{name}</b>!😳 Вы ввели неверный диапазон '
                                                  ' времени бронирования отеля!'
                                                  ' Попробуйте, пожалуйста, еще раз.'.format(
                                                    name=message.from_user.first_name), parse_mode='HTML')
                bot.register_next_step_handler(message, get_date)
            elif user.block_choose_date and not valid_range_date:
                bot.send_message(message.chat.id, 'Неудача, <b>{name}</b>!😳 Диапазон '
                                                  ' времени бронирования отеля не должен превышать <b>28 дней</b>!'
                                                  ' Попробуйте, пожалуйста, еще раз.'.format(
                                                    name=message.from_user.first_name), parse_mode='HTML')
                bot.register_next_step_handler(message, get_date)
            elif not user.block_choose_date and valid_range_date:
                bot.send_message(message.chat.id, 'Замечательно!😇😇 Теперь назовите, пожалуйста, '  # type: ignore
                                                  ' количество отелей для поиска (не более 5).'.format(
                                                    name=message.from_user.first_name), parse_mode='HTML')
                bot.register_next_step_handler(message, get_number_hotels)
    except IndexError:
        bot.send_message(message.chat.id, 'Неудача, <b>{name}</b>😳! Вы ввели неверный формат даты'
                                          ' Попробуйте, пожалуйста, еще раз. Формат ввода: <b>ГГГГ-ММ-ДД</b>,'
                                          ' <b>ГГГГ-ММ-ДД</b>.'.format(name=message.from_user.first_name),
                         parse_mode='HTML')
        bot.register_next_step_handler(message, get_date)


def get_number_hotels(message: telebot.types.Message) -> None:
    """Функция, регистрирующая данные из сообщения пользователя о количестве отелей для поиска.

    :param:
        message: объект класса telebot
    """
    user = User.get_user(message.from_user.id)
    try:
        if int(message.text) > 0 and int(message.text) <= 5:
            user.hotels_count = int(message.text)
            bot.send_message(message.chat.id, 'Хорошо, <b>{name}</b>😄😄! Теперь скажите, пожалуйста, '
                                              ' нужно ли искать фотографии отелей?🙃🙃'.format(
                                                name=message.from_user.first_name), parse_mode='HTML')
            bot.register_next_step_handler(message, is_search_photos)
        else:
            bot.send_message(message.chat.id, '<b>{name}</b>, количество отелей должно составлять'
                                              ' не менее <b>1</b> и не более <b>5</b> позиций.'
                                              ' Повторите, пожалуйста, ввод.'.format(
                                                name=message.from_user.first_name), parse_mode='HTML')
            bot.register_next_step_handler(message, get_number_hotels)
    except ValueError:
        bot.send_message(message.chat.id,
                         'Неудача😳! Вам необходимо ввести  значение в виде целого числа.'  # type: ignore
                         ' Попробуйте, пожалуйста, еще раз.'.format(name=message.from_user.first_name),
                         parse_mode='HTML')
        bot.register_next_step_handler(message, get_number_hotels)


def is_search_photos(message: telebot.types.Message) -> None:
    """Функция, регистрирующая данные из сообщения пользователя о необходимость поиска фотографий отелей.

    :param:
        message: объект класса telebot
    """
    user = User.get_user(message.from_user.id)

    if message.text.lower() == 'да':
        user.getting_photos = True
        bot.send_message(message.chat.id, 'Введите, пожалуйста, количество фотографий для поиска'  # type: ignore
                                          ' (не более 5)🙃🙃.'.format(name=message.from_user.first_name),
                         parse_mode='HTML')
        bot.register_next_step_handler(message, get_number_photos)
    elif message.text.lower() == 'нет':
        bot.send_message(message.chat.id, 'Отлично, <b>{name}</b>👍😁😁! Я собрал всю необходимую информацию и'
                                          ' начинаю поиск🔍.'.format(name=message.from_user.first_name),
                         parse_mode='HTML')
        bot.send_message(message.chat.id, 'Пожалуйста, подождите🕑🕑🕑.')

        get_search_result(user=user)
        if user.hotel_data:
            bot.send_message(message.chat.id, '<b>Результаты поиска:</b>', parse_mode='HTML')
            if len(user.hotel_data) < user.hotels_count:
                bot.send_message(message.chat.id, 'Мне не удалось найти так много'
                                                  ' отелей в городе - вот все, что есть.🙃🙃')
            for number, hotel in enumerate(user.hotel_data):
                bot.send_message(message.chat.id, 'Отель № {number}\n'
                                                  '<b>Название отеля:</b> <i>{name}</i>\n'
                                                  '<b>Веб-страница отеля на сайте Hotels.com:</b> '
                                                  '<i>{url}</i>\n'
                                                  '<b>Адрес отеля:</b> <i>{address}</i>\n'
                                                  'Отель расположен от центра города на расстоянии в '
                                                  '<b>{distance} nm</b>\n'
                                                  '<b>Цена за сутки проживания (двое взрослых):'
                                                  '</b> <i>{day_cost}</i>\n'
                                                  'Общая стоимость проживания  за период с <b>{check_in} по'
                                                  ' {check_out}</b>  (с учетом пошлин): <i>{total_cost}</i>'.format(

                                                    number=str(number + 1),
                                                    url=hotel['URL'],
                                                    name=hotel['name_hotel'],
                                                    address=hotel['hotel_address'],
                                                    distance=hotel['distance_from_center'],
                                                    day_cost=hotel['cost_for_day'],
                                                    check_in=user.check_in,
                                                    check_out=user.check_out,
                                                    total_cost=hotel['total_cost']), parse_mode='HTML')
            history.write_data_into_database(user=user)
            user.hotel_data = []
        else:
            bot.send_message(message.chat.id, 'К сожалению, <b>{name}</b>, я не смог найти никакой информации'
                                              ' по вашему запросу😔😔😔. Проверьте, пожалуйста, '
                                              'введенную информацию или попробуйте произвести поиск позже.'.format(
                                                name=message.from_user.first_name), parse_mode='HTML')

    elif message.text.lower() != 'нет' and message.text.lower() != 'да':
        bot.send_message(message.chat.id, 'Неудача, <b>{name}</b>😳! Вам необходимо ввести либо <b>"да"</b>, либо'
                                          ' <b>"нет"</b> Попробуйте, пожалуйста, '
                                          'еще раз.'.format(name=message.from_user.first_name), parse_mode='HTML')
        bot.register_next_step_handler(message, is_search_photos)


def get_number_photos(message: telebot.types.Message) -> None:
    """Функция, регистрирующая данные из сообщения пользователя о количестве фотографий отелей для поиска.

    :param:
        message: объект класса telebot
    """
    user = User.get_user(message.from_user.id)
    try:
        if int(message.text) > 0 and int(message.text) <= 5:
            user.photos_count = int(message.text)
            bot.send_message(message.chat.id, 'Отлично, <b>{name}</b>👍😁😁! Я собрал всю необходимую информацию и'
                                              ' начинаю поиск отелей🔍.'.format(
                                                name=message.from_user.first_name), parse_mode='HTML')
            bot.send_message(message.chat.id, 'Пожалуйста, подождите🕑🕑🕑.')

            get_search_result(user=user)
            if user.hotel_data:
                bot.send_message(message.chat.id, '<b>Результаты поиска:</b>', parse_mode='HTML')
                if len(user.hotel_data) < user.hotels_count:
                    bot.send_message(message.chat.id, 'Мне не удалось найти так много'
                                                      ' отелей в городе - вот все, что есть.')

                for number, hotel in enumerate(user.hotel_data):

                    if hotel['hotel_photos'] is not None \
                            and len(hotel['hotel_photos']) < user.photos_count:
                        bot.send_message(message.chat.id, 'Мне не удалось найти так много'
                                                          ' фотографий данного отеля - вот все, что есть.🙃🙃')
                    if hotel['hotel_photos'] is None:
                        bot.send_message(message.chat.id, 'К сожалению, фотографии отеля найти не удалось.😔😔'
                                                          'Отель № {number}\n'
                                                          '<b>Название отеля:</b> <i>{name}</i>\n'
                                                          '<b>Веб-страница отеля на сайте Hotels.com:</b> '
                                                          '<i>{url}</i>\n'
                                                          '<b>Адрес отеля:</b> <i>{address}</i>\n'
                                                          'Отель расположен от центра города на расстоянии в '
                                                          '<b>{distance} nm</b>\n'
                                                          '<b>Цена за сутки проживания (двое взрослых):'
                                                          '</b> <i>{day_cost}</i>\n'
                                                          'Общая стоимость проживания  за период с <b>{check_in} по'
                                                          ' {check_out}</b>  (с учетом пошлин): '
                                                          '<i>{total_cost}</i>'.format(
                                                            number=str(number + 1),
                                                            url=hotel['URL'],
                                                            name=hotel['name_hotel'],
                                                            address=hotel['hotel_address'],
                                                            distance=hotel['distance_from_center'],
                                                            day_cost=hotel['cost_for_day'],
                                                            check_in=user.check_in,
                                                            check_out=user.check_out,
                                                            total_cost=hotel['total_cost']), parse_mode='HTML')

                    else:
                        bot.send_media_group(message.chat.id,
                                             [telebot.types.InputMediaPhoto(photo,
                                              caption='Отель № {number}\n<b>Название отеля:</b> <i>{name}</i>\n'
                                              '<b>Веб-страница отеля на сайте Hotels.com:</b> <i>{url}</i>\n<b>Адрес '
                                              'отеля:</b> <i>{address}</i>\n'
                                              'Отель расположен от центра города на расстоянии в '
                                              '<b>{distance} nm</b>\n'
                                              '<b>Цена за сутки проживания (двое взрослых):'
                                              '</b> <i>{day_cost}</i>\n'
                                              'Общая стоимость проживания  за период с <b>{check_in} по'
                                              ' {check_out}</b>  (с учетом пошлин):'
                                              ' <i>{total_cost}</i>'.format(
                                                number=str(number + 1),
                                                url=hotel['URL'],
                                                name=hotel['name_hotel'],
                                                address=hotel['hotel_address'],
                                                distance=hotel['distance_from_center'],
                                                day_cost=hotel['cost_for_day'],
                                                check_in=user.check_in,
                                                check_out=user.check_out,
                                                total_cost=hotel['total_cost']) if index == 0 else '',
                                                parse_mode='HTML')
                                              for index, photo in enumerate(hotel['hotel_photos'])])

                history.write_data_into_database(user=user)
                user.hotel_data = []
            else:
                bot.send_message(message.chat.id, 'К сожалению, <b>{name}</b>, я не смог найти никакой информации'
                                                  ' по вашему запросу😔😔😔. Проверьте, пожалуйста, '
                                                  'введенную информацию или попробуйте произвести поиск позже.'.format(
                                                    name=message.from_user.first_name), parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, '<b>{name}</b>, количество фотографий должно '
                                              'составлять не менее 1 и не более <b>5</b> позиций.'
                                              ' Повторите, пожалуйста,ввод.'.format(
                                                name=message.from_user.first_name), parse_mode='HTML')
            bot.register_next_step_handler(message, get_number_photos)
    except ValueError:
        bot.send_message(message.chat.id, 'Неудача, <b>{name}</b>😳! Вам необходимо ввести цифровое значение '
                                          ' Попробуйте, пожалуйста, еще раз.'.format(name=message.from_user.first_name),
                         parse_mode='HTML')
        bot.register_next_step_handler(message, get_number_photos)


@bot.message_handler(commands=['history'])
def get_message_about_history_search(message: telebot.types.Message) -> None:
    """Функция, обрабатывающая введенную пользователем команду /history.

    :param:
        message: объект класса telebot
    """

    user = User.get_user(message.from_user.id)

    if user.chat_id is None:
        user.chat_id = message.chat.id

    history_search_list = history.get_history_search(user=user)

    if not history_search_list:
        bot.send_message(message.chat.id, 'История поиска пуста🙃🙃🙃.'.format(  # type: ignore
            name=message.from_user.first_name), parse_mode='HTML')

    else:
        bot.send_message(message.chat.id, '<b>История поиска отелей:</b>'.format(  # type: ignore
            name=message.from_user.first_name), parse_mode='HTML')

        for number, history_elem in enumerate(history_search_list):
            bot.send_message(message.chat.id, 'Запись № {number}\nВведенная команда: <b>{command}</b>\n'
                                              'Дата и время введенной команды: <b>{date_and_time}</b>\n'
                                              'Город, в котором проводился поиск отелей: <b>{city}</b>\n'
                                              'Найденные отели: <b>{hotels}</b>.'.format(number=(number + 1),
                                                                                         command=history_elem[0],
                                                                                         date_and_time=history_elem[1],
                                                                                         city=history_elem[2],
                                                                                         hotels=history_elem[3]),
                             parse_mode='HTML')


@bot.message_handler(content_types=['text'])
def get_message_for_incorrect_input(message: telebot.types.Message) -> None:
    """Функция, обрабатывающие введенные пользователем несуществующие команды и текстовые сообщения вне
     выполнения конкретных команд.

    :param:
        message: объект класса telebot
    """
    if message.text.startswith('/'):
        bot.send_message(message.chat.id, 'Я не знаю такой команды🤯🤯🤯. Для получения справки о доступных командах'
                                          ' введите /help.')
    else:
        bot.send_message(message.chat.id, 'Для начала работы введите, пожалуйста, соответствующую команду.😎😎 '
                                          'Для получения справки о доступных командах наберите /help.')


if __name__ == '__main__':
    bot.polling()
