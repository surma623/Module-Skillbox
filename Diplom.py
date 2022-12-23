import telebot
import requests
import json
from typing import Optional, Any, List, Dict
from translate import Translator
import datetime


class User:
    all_users = dict()

    def __init__(self, user_id):
        self.city = None
        self.city_id = None
        self.hotels_count = None
        self.getting_photos = False
        self.photos_count = None
        self.user_command = None
        self.check_in = None
        self.check_out = None
        self.block_choose_date = False
        self.sort_flag = 'ASC'
        self.hotel_data = []
        self.need_to_get_ranges_flag = False
        self.p_range = None
        self.d_range = None

        User.add_user(user_id, self)

    @classmethod
    def get_user(cls, user_id):
        if User.all_users.get(user_id) is None:
            new_user = User(user_id)
            return new_user
        return User.all_users.get(user_id)

    @classmethod
    def add_user(cls, user_id, user):
        cls.all_users[user_id] = user

    @classmethod
    def del_user(cls, user_id):
        if User.all_users.get(user_id) is not None:
            del User.all_users[user_id]


class InputError(Exception):
    pass


def translate_name_city(name_city: str) -> Optional[str]:
    """Функция, которая переводит название города на английский язык .

    :param:
        name_city: название города для перевода.
    :return:
        перевод названия города.
    :exception:
        в случае невозможности перевести название города на английский язык, вызывается исключение RuntimeError.
    """
    try:

        translator = Translator(from_lang='russian', to_lang='english')
        translation = translator.translate(name_city)
        return translation

    except RuntimeError as exc:
        return exc


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
        "X-RapidAPI-Key": "fc4d8bf2b3msh9d7800fdb1f6826p1283cejsn73018965022a",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    return get_api_request(method_request=method_request, url=url, headers=headers, querystring=querystring)


def make_hotel_list_api_request(city_id: str, check_in: List[str], check_out: List[str]) -> Optional[dict]:
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
            "max": 150,
            "min": 100
        }}
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "fc4d8bf2b3msh9d7800fdb1f6826p1283cejsn73018965022a",
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
        "X-RapidAPI-Key": "fc4d8bf2b3msh9d7800fdb1f6826p1283cejsn73018965022a",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    return get_api_request(method_request=method_request, url=url, headers=headers, querystring=payload)


def search_city_id(location_data: Any) -> Optional[str]:
    """Функция, совершающая поиск id города в полученных данных из API.

    :param:
        location_data: данные городе в формате json.
    :return:
        id города и None в случае, если полученные данные не содержат id города.
    """

    city_id = None

    if isinstance(location_data, dict):
        for key, value in location_data.items():
            if key == 'gaiaId':
                city_id = value
                return city_id
            elif isinstance(value, list):
                city_id = search_city_id(value)
            elif isinstance(value, dict):
                search_city_id(value)
    elif isinstance(location_data, list):

        for elem in location_data:
            if isinstance(elem, dict):
                city_id = search_city_id(elem)
                if city_id:
                    break
        else:
            city_id = None

    return city_id


def is_date_valid(checking_date: str) -> bool:
    """Функция, проверяющая дату на корректность.

    :param:
        checking_date: проверяемая дата

    :return: True - если дата корректна, False - если нет
    :except IndexError, ValueError: эти два исключения вызываются в случае ввода
     некоторых вариантов некорректной строки даты и призваны обеспечить нормальную работу программы
    """
    valid = False
    checking_date = checking_date.split('-')
    if len(checking_date) == 3:
        current_date = datetime.date.today()
        current_date = str(current_date).split('-')
        if (int(checking_date[0]) == int(current_date[0])) and (int(checking_date[1]) == int(current_date[1])) \
                and (int(checking_date[2]) >= int(current_date[2])) or (int(checking_date[0]) == int(current_date[0])) \
                and (int(checking_date[1]) > int(current_date[1])) or (int(checking_date[0]) > int(current_date[0])):
            try:
                if int(checking_date[2]) in range(1, 32) and int(checking_date[1]) in [1, 3, 5, 7, 8, 10, 12] \
                        and int(checking_date[0]) in range(int(current_date[0]), 2100):
                    valid = True
                elif int(checking_date[2]) in range(1, 31) and int(checking_date[1]) in [4, 6, 9, 11] \
                        and int(checking_date[0]) in range(int(current_date[0]), 2100):
                    valid = True
                elif int(checking_date[2]) in range(1, 29) and int(checking_date[1]) == 2 and int(checking_date[0]) \
                        in range(int(current_date[0]), 2100):
                    valid = True
                elif (int(checking_date[2]) in range(1, 30) and int(checking_date[1]) == 2 and int(checking_date[0])
                      in range(2024, 2100, 4)):
                    valid = True

                if valid:
                    return True
                else:
                    return False
            except (IndexError, ValueError):
                pass
        else:
            return False
    else:
        return False


def is_range_date_valid(date_check_in: List[str], date_check_out: List[str]) -> bool:
    """Функция, проверяющая диапазон введенных дат на корректность.

    :param:
        date_check_in: дата начала пребывания в отеле
        date_check_out: дата окончания пребывания в отеле

    :return: True - если дата корректна, False - если нет
    """
    valid = True

    if (date_check_in[0] == date_check_out[0]) and (date_check_in[1] == date_check_out[1]) \
            and (date_check_in[2] >= date_check_out[2]) or (date_check_in[0] == date_check_out[0]) \
            and (date_check_in[1] > date_check_out[1]) or (date_check_in[0] > date_check_out[0]):
        valid = False
        return valid

    return valid


def get_hotels_list(places_city: Any, hotel_info: Dict, key_flag: bool, user: User) -> None:
    """Функция, осуществляющая сбор информации об отелях из данных от API

    :param:
        places_city: данные от API
        hotel_info: словарь для записи данных об отелях
        key_flag: флаг сигнализирующий о нахождении нужного ключа (становится True)
        user: объект класса User, содержащий данные об вводимой пользователем информации
    """

    if isinstance(places_city, dict):
        for key, value in places_city.items():
            if isinstance(value, dict):
                get_hotels_list(value, hotel_info, key_flag, user)
            elif isinstance(value, list):
                get_hotels_list(value, hotel_info, key_flag, user)
            if key == 'propertySearchListings':
                key_flag = True
                get_hotels_list(value, hotel_info, key_flag, user)
            elif value == 'Property' and key_flag:
                for nested_key, nested_value in places_city.items():
                    if nested_key == 'id':
                        hotel_info['id_hotel'] = nested_value
                        hotel_info['URL'] = f'https://www.hotels.com/h{nested_value}.Hotel-Information'
                    elif nested_key == 'name':
                        hotel_info['name_hotel'] = nested_value
                        break
            elif key == 'distanceFromDestination' and key_flag:
                for nested_key, nested_value in value.items():
                    if nested_key == 'value':
                        hotel_info['distance_from_center'] = str(nested_value)
            elif key == 'label' and key_flag:
                money = ''
                for sym in value:
                    if sym != '$':
                        money += sym
                hotel_info['cost_for_day'] = money

            elif value == 'LodgingEnrichedMessage' and key_flag:
                for nested_key, nested_value in places_city.items():
                    if nested_key == 'value':
                        total_cost = ''
                        for symbol in nested_value:
                            if symbol.isdigit():
                                total_cost += symbol
                        hotel_info['total_cost'] = total_cost
                        break
                hotel_info_copy = hotel_info.copy()
                if len(user.hotel_data) < user.hotels_count:
                    user.hotel_data.append(hotel_info_copy)
                break

    elif isinstance(places_city, list):
        for elem in places_city:
            if isinstance(elem, dict):
                get_hotels_list(elem, hotel_info, key_flag, user)


def get_hotel_details(detail_hotel, user, index):
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


def get_search_result(user: User) -> List[Dict]:
    hotel_data = dict()
    needed_key_flag = False

    places_city_dict = make_hotel_list_api_request(user.city_id, user.check_in.split('-'), user.check_out.split('-'))

    get_hotels_list(places_city_dict, hotel_data, needed_key_flag, user)

    for index_dict, hotel_dict in enumerate(user.hotel_data):

        detail_hotel_dict = make_detail_hotel_api_request(hotel_dict['id_hotel'])

        user.hotel_data[index_dict]['hotel_address'] = None
        if user.getting_photos:
            user.hotel_data[index_dict]['hotel_photos'] = list()
        get_hotel_details(detail_hotel_dict, user, index_dict)

    print(user.hotel_data)

    return user.hotel_data


bot = telebot.TeleBot('5870004764:AAHuvLUh4NuPg-sVl9K3iVm5zNgdLjV6ook')


@bot.message_handler(commands=['start'])
def to_start(message: telebot.types.Message) -> None:
    """Функция, обрабатывающая введенную пользователем команду /start

    :param:
        message: объект класса telebot
    """
    if message.chat.id not in User.all_users:
        User(message.chat.id)
    bot.send_message(message.chat.id, 'Здравствуйте, <b>{name}</b>! Вас приветствует <b>Travel_guid_bot</b>!👋\n'
                                      'Я помогу Вам выбрать отель для отдыха.☀️🏝⛱✈️\n'
                                      'У меня вы можете узнать:\n'
                                      'топ самых дешёвых отелей в городе (команда /lowprice);\n'
                                      'топ самых дорогих отелей в городе (команда /highprice);\n'
                                      'топ отелей, наиболее подходящих по цене и расположению от центра'
                                      '(самые дешёвые и находятся ближе всего к центру) (команда /bestdeal);\n'
                                      'историю поиска отелей (команда /history)'.format(
        name=message.from_user.first_name), parse_mode='HTML')


@bot.message_handler(commands=['lowprice'])
def get_low_price_message(message: telebot.types.Message) -> None:
    """Функция, обрабатывающая введенную пользователем команду /lowprice

    :param:
        message: объект класса telebot
    """
    bot.send_message(message.chat.id, 'Отлично, <b>{name}</b>!😇 Сейчас я помогу Вам найти'
                                      ' топ самых дешёвых отелей в городе.😎👌\n'
                                      ' Пожалуйста, введите город для поиска.\n'.format(
        name=message.from_user.first_name), parse_mode='HTML')
    bot.register_next_step_handler(message, get_city)


def get_city(message: telebot.types.Message) -> None:
    """Функция, регистрирующая данные из сообщения пользователя о городе, где необходимо искать отели.

    :param:
        message: объект класса telebot
    """
    try:
        user = User.get_user(message.from_user.id)
        user.city = translate_name_city(message.text.lower())
        if isinstance(user.city, RuntimeError):
            raise RuntimeError
        user.city_id = search_city_id(make_location_search_api_request(user.city))
        print(user.city_id)
        if not user.city_id:
            bot.send_message(message.from_user.id, 'Неудача, <b> {name} </b>😳! Я не смог найти информацию'
                                                   ' по вашему городу!😢😢😢'
                                                   'Попробуйте, пожалуйста, еще раз.'.format(
                name=message.from_user.first_name), parse_mode='HTML')
            bot.register_next_step_handler(message, get_city)

        else:
            bot.send_message(message.from_user.id, 'Отлично, <b>{name}</b>👍😁😁! Теперь скажите, пожалуйста,'
                                                   ' с какого по какое число Вы '
                                                   ' будете проживать в отеле? (ГГГГ-ММ-ДД,'
                                                   ' ГГГГ-ММ-ДД)'.format(name=message.from_user.first_name),
                             parse_mode='HTML')

            bot.register_next_step_handler(message, get_date)
    except RuntimeError:
        bot.send_message(message.from_user.id, 'Неудача, <b> {name} </b>😳! Для того, чтобы начать поиск отелей '
                                               ' в указанном Вами городе мне нужно совершить перевод его названия '
                                               ' на английский язык. К сожалению😢😢😢, я не могу перевести введенное'
                                               ' Вами название, возможно,'
                                               ' в нем ошибка. Попробуйте, пожалуйста, еще раз.'.format(
            name=message.from_user.first_name), parse_mode='HTML')
        bot.register_next_step_handler(message, get_city)
    except TypeError:
        bot.send_message(message.from_user.id, 'Город введен некорректно. Попробуйте еще раз.')
        bot.register_next_step_handler(message, get_city)


def get_date(message: telebot.types.Message) -> None:
    """Функция, регистрирующая данные из сообщения пользователя о диапазоне планируемого пребывания в отеле.
    :param:
        message: объект класса telebot
    """

    user = User.get_user(message.from_user.id)
    try:
        user.check_in = message.text.split(', ')[0]
        user.check_out = message.text.split(', ')[1]
        if not is_date_valid(user.check_in):
            bot.send_message(message.chat.id, 'Неудача, <b>{name}</b>😳! Вы ввели некорректную дату заезда!'
                                              ' Попробуйте, пожалуйста, еще раз. Формат ввода - (ГГГГ-ММ-ДД,'
                                              ' ГГГГ-ММ-ДД)'.format(name=message.from_user.first_name),
                             parse_mode='HTML')
            bot.register_next_step_handler(message, get_date)
        elif not is_date_valid(user.check_out):
            bot.send_message(message.chat.id, 'Неудача, <b>{name}</b>😳! Вы ввели некорректную дату отъезда!'
                                              ' Попробуйте, пожалуйста, еще раз. Формат ввода - (ГГГГ-ММ-ДД,'
                                              ' ГГГГ-ММ-ДД)'.format(name=message.from_user.first_name),
                             parse_mode='HTML')
            bot.register_next_step_handler(message, get_date)

        else:
            if not is_range_date_valid(user.check_in.split('-'), user.check_out.split('-')):
                bot.send_message(message.chat.id, 'Неудача, <b>{name}</b>😳! Вы ввели неверный диапазон '
                                                  ' времени бронирования отеля!'
                                                  ' Попробуйте, пожалуйста, еще раз.'.format(
                    name=message.from_user.first_name), parse_mode='HTML')
                bot.register_next_step_handler(message, get_date)
            else:
                bot.send_message(message.chat.id, 'Замечательно, <b>{name}</b>😇😇! Теперь назовите, пожалуйста, '
                                                  ' количество отелей для поиска.'.format(
                    name=message.from_user.first_name), parse_mode='HTML')
                bot.register_next_step_handler(message, get_number_hotels)
    except IndexError:
        bot.send_message(message.chat.id, 'Неудача, <b>{name}</b>😳! Вы ввели неверный формат даты'
                                          ' Попробуйте, пожалуйста, еще раз. Формат ввода - (ГГГГ-ММ-ДД,'
                                          ' ГГГГ-ММ-ДД)'.format(name=message.from_user.first_name), parse_mode='HTML')
        bot.register_next_step_handler(message, get_date)


def get_number_hotels(message: telebot.types.Message) -> None:
    """Функция, регистрирующая данные из сообщения пользователя о количестве отелей для поиска.

    :param:
        message: объект класса telebot
    """
    user = User.get_user(message.from_user.id)
    try:
        user.hotels_count = int(message.text)
        bot.send_message(message.chat.id, 'Хорошо, <b>{name}</b>😄😄! Теперь скажите, пожалуйста, '
                                          ' нужно ли искать фотографии отелей?🙃🙃'.format(
            name=message.from_user.first_name), parse_mode='HTML')
        bot.register_next_step_handler(message, is_search_photos)
    except ValueError:
        bot.send_message(message.chat.id, 'Неудача, <b>{name}</b>😳! Вам необходимо ввести цифровое значение '
                                          ' Попробуйте, пожалуйста, еще раз.'.format(name=message.from_user.first_name),
                         parse_mode='HTML')
        bot.register_next_step_handler(message, get_number_hotels)


def is_search_photos(message: telebot.types.Message) -> None:
    """Функция, регистрирующая данные из сообщения пользователя о необходимость поиска фотографий отелей.

    :param:
        message: объект класса telebot
    """
    user = User.get_user(message.from_user.id)
    try:
        if message.text.lower() == 'да':
            user.getting_photos = True
            bot.send_message(message.chat.id, 'Введите, пожалуйста, количество фотографий для поиска'.format(
                name=message.from_user.first_name), parse_mode='HTML')
            bot.register_next_step_handler(message, get_number_photos)
        elif message.text.lower() == 'нет':
            bot.send_message(message.chat.id, 'Отлично, <b>{name}</b>👍😁😁! Я собрал всю необходимую информацию и'
                                              ' начинаю поиск, пожалуйста, подождите!'.format(
                name=message.from_user.first_name), parse_mode='HTML')
            bot.send_message(message.chat.id, '...')

            result_search: Optional[List[Dict]] = get_search_result(user)
            if result_search:
                bot.send_message(message.chat.id, '<b>Результаты поиска:</b>',  parse_mode='HTML')
                for number in range(user.hotels_count):
                    bot.send_message(message.chat.id, 'Отель № {number}\n'
                                                      '<b>Название отеля:</b> <i>{name}</i>\n'
                                                      '<b>Веб-страница отеля на сайте Hotels.com:</b> <i>{url}</i>\n'
                                                      '<b>Адрес отеля:</b> <i>{address}</i>\n'
                                                      'Отель расположен от центра города на расстоянии в '
                                                      '<b>{distance} nm</b>\n'
                                                      '<b>Цена за сутки проживания (двое взрослых):'
                                                      '</b> <i>{day_cost} $</i>\n'
                                                      'Общая стоимость проживания  за период с <b>{check_in} по'
                                                      ' {check_out}</b>  (с учетом пошлин):'
                                                      '<i>{total_cost} $</i>'.format(

                        number=str(number + 1),
                        url=result_search[number]['URL'],
                        name=result_search[number]['name_hotel'],
                        address=result_search[number]['hotel_address'],
                        distance=result_search[number]['distance_from_center'],
                        day_cost=result_search[number]['cost_for_day'],
                        check_in=user.check_in,
                        check_out=user.check_out,
                        total_cost=result_search[number]['total_cost']), parse_mode='HTML')
                user.hotel_data = []
            else:
                bot.send_message(message.chat.id, 'К сожалению, <b>{name}</b>, я не смог найти никакой информации'
                                                  ' по вашему запросу😔😔😔. Проверьте, пожалуйста, '
                                                  'введенную информацию или попробуйте произвести поиск позже.'.format(
                    name=message.from_user.first_name), parse_mode='HTML')

        elif message.text.lower() != 'нет' and message.text.lower() != 'да':
            raise InputError('Неудача, <b>{name}</b>😳! Вам необходимо ввести либо "да", либо "нет" '
                             ' Попробуйте, пожалуйста, еще раз.'.format(name=message.from_user.first_name),
                             parse_mode='HTML')
    except InputError as exc:
        bot.send_message(message.chat.id, exc)
        bot.register_next_step_handler(message, is_search_photos)


def get_number_photos(message: telebot.types.Message) -> None:
    """Функция, регистрирующая данные из сообщения пользователя о количестве фотографий отелей для поиска.

    :param:
        message: объект класса telebot
    """
    user = User.get_user(message.from_user.id)
    try:
        user.photos_count = int(message.text)
        bot.send_message(message.chat.id, 'Отлично, <b>{name}</b>👍😁😁! Я собрал всю необходимую информацию и'
                                          ' начинаю поиск отелей, пожалуйста, подождите!'.format(
            name=message.from_user.first_name), parse_mode='HTML')
        bot.send_message(message.chat.id, '...')

        result_search: Optional[List[Dict]] = get_search_result(user)
        if result_search:
            bot.send_message(message.chat.id, '<b>Результаты поиска:</b>', parse_mode='HTML')
            for number in range(user.hotels_count):
                bot.send_message(message.chat.id, 'Отель № {number}\n'
                                                  '<b>Название отеля:</b> <i>{name}</i>\n'
                                                  '<b>Веб-страница отеля на сайте Hotels.com:</b> <i>{url}</i>\n'
                                                  '<b>Адрес отеля:</b> <i>{address}</i>\n'
                                                  'Отель расположен от центра города на расстоянии в '
                                                  '<b>{distance} nm</b>\n'
                                                  '<b>Цена за сутки проживания (двое взрослых):'
                                                  '</b> <i>{day_cost} $</i>\n'
                                                  'Общая стоимость проживания  за период с <b>{check_in} по'
                                                  ' {check_out}</b>  (с учетом пошлин):<i>{total_cost} $</i>'.format(

                    number=str(number + 1),
                    url=result_search[number]['URL'],
                    name=result_search[number]['name_hotel'],
                    address=result_search[number]['hotel_address'],
                    distance=result_search[number]['distance_from_center'],
                    day_cost=result_search[number]['cost_for_day'],
                    check_in=user.check_in,
                    check_out=user.check_out,
                    total_cost=result_search[number]['total_cost']), parse_mode='HTML')

                # if len(result_search[number]['hotel_photos']) < user.photos_count:
                #     bot.send_message(message.chat.id, 'Мне не удалось найти так много'
                #                                       ' фотографий - вот все, что есть.')
                # elif result_search[number]['hotel_photos'] is None:
                #     bot.send_message(message.chat.id, 'К сожалению, фотографии найти не удалось')
                #     continue
                for photo in result_search[number]['hotel_photos']:
                    bot.send_photo(message.chat.id, photo)
            user.hotel_data = []
        else:
            bot.send_message(message.chat.id, 'К сожалению, <b>{name}</b>, я не смог найти никакой информации'
                                              ' по вашему запросу😔😔😔. Проверьте, пожалуйста, '
                                              'введенную информацию или попробуйте произвести поиск позже.'.format(
                name=message.from_user.first_name), parse_mode='HTML')



    except ValueError:
        bot.send_message(message.chat.id, 'Неудача, <b>{name}</b>😳! Вам необходимо ввести цифровое значение '
                                          ' Попробуйте, пожалуйста, еще раз.'.format(name=message.from_user.first_name),
                         parse_mode='HTML')
        bot.register_next_step_handler(message, get_number_photos)


bot.polling()