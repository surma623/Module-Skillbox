import telebot
import requests
import json
from typing import Optional, Any, List
from translate import Translator
import datetime


class User:
    all_users = dict()

    def __init__(self, user_id):
        self.city = None
        self.city_id = None
        self.hotels_count = None
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
        в случае невозможности перевести название города на английский язык, вызывается исключение BaseException.
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
        данные в формате json либо None при отсутствии города в данных от API
    :exception:
       requests.Timeout: вызывается в случае, если сервер не отвечает на запрос в течении установленного времени
       requests.RequestException: вызывается в случае любой другой ошибки при попытке отправки запроса и получения
       ответа с сервера
    """
    try:
        if method_request == "GET":
            response = requests.request(method_request, url, headers=headers, params=querystring, timeout=20)
        else:
            response = requests.request(method_request, url, json=querystring, headers=headers,  timeout=20)

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
        данные в формате json либо None при отсутствии города в данных от API
    """
    method_request = "GET"
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"
    querystring = {"q": name_city, "locale": "en_US", "langid": "1033", "siteid": "300000001"}
    headers = {
        "X-RapidAPI-Key": "658321e9b4msh17b5cf51d1ee298p1b8f09jsn473c3fb8945e",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    return get_api_request(method_request=method_request, url=url, headers=headers, querystring=querystring)


def make_hotel_list_api_request(city_id: str) -> Optional[dict]:
    """ Функция, которая формирует параметры запроса информации об отелях в городе к API.

    :param:
        city_id: id города.
    :return:
        данные в формате json либо None при отсутствии информации об отелях в городе в данных от API
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
            "max": 150,
            "min": 100
        }}
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "658321e9b4msh17b5cf51d1ee298p1b8f09jsn473c3fb8945e",
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
            and (date_check_in[2] > date_check_out[2]) or (date_check_in[0] == date_check_out[0]) \
            and (date_check_in[1] > date_check_out[1]) or (date_check_in[0] > date_check_out[0]):
        valid = False
        return valid

    return valid


def get_search_result(user: Optional[User]) -> str:
    print(user.city_id)
    print(make_hotel_list_api_request(user.city_id))
    return 'Есть'


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
                                                  ' Попробуйте, пожалуйста, еще раз. Формат ввода - (ГГГГ-ММ-ДД,'
                                                  ' ГГГГ-ММ-ДД)'.format(
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
            bot.send_message(message.chat.id, 'Введите, пожалуйста, количество фотографий для поиска'.format(
                name=message.from_user.first_name), parse_mode='HTML')
            bot.register_next_step_handler(message, get_number_photos)
        elif message.text.lower() == 'нет':
            bot.send_message(message.chat.id, 'Отлично, <b>{name}</b>👍😁😁! Я собрал всю необходимую информацию и'
                                              ' начинаю поиск, пожалуйста, подождите!'.format(
                                                name=message.from_user.first_name), parse_mode='HTML')
            bot.send_message(message.chat.id, get_search_result(user))
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
        bot.send_message(message.chat.id, get_search_result(user))
    except ValueError:
        bot.send_message(message.chat.id, 'Неудача, <b>{name}</b>😳! Вам необходимо ввести цифровое значение '
                                          ' Попробуйте, пожалуйста, еще раз.'.format(name=message.from_user.first_name),
                         parse_mode='HTML')
        bot.register_next_step_handler(message, get_number_photos)


bot.polling()