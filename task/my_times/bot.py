import telebot
import lowprice

class InputError(Exception):
    pass


bot = telebot.TeleBot('5870004764:AAHuvLUh4NuPg-sVl9K3iVm5zNgdLjV6ook')
checking_input_command_message = {'input_command_message': False}


@bot.message_handler(commands=['start'])
def get_start_message(message: telebot.types.Message) -> None:
    bot.send_message(message.chat.id, 'Здравствуйте, <b>{name}</b>! Вас приветствует <b>Travel_guid_bot</b>!👋\n'
                                      'Я помогу Вам выбрать отель для отдыха.☀️🏝⛱✈️\n'
                                      'У меня вы можете узнать:\n'
                                      'топ самых дешёвых отелей в городе (команда /lowprice);\n'
                                      'топ самых дорогих отелей в городе (команда /highprice);\n'
                                      'топ отелей, наиболее подходящих по цене и расположению от центра'
                                      '(самые дешёвые и находятся ближе всего к центру) (команда /bestdeal);\n'
                                      'историю поиска отелей (команда /history)'.format(
                                       name=message.from_user.first_name),
                                      parse_mode='HTML')


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal', 'history'])
def get_command_message(message: telebot.types.Message) -> None:

    checking_input_command_message['input_command_message'] = True
    if message.text == '/lowprice':
        bot.send_message(message.chat.id, 'Отлично, <b>{name}</b>!😇 Сейчас я помогу Вам найти'
                                          ' топ самых дешёвых отелей в городе.😎👌\n'
                                          'Последовательно через запятую введите следующую информацию:\n'
                                          '🔹 название города для поиска;\n'
                                          '🔸количество отелей для отображения в чате;\n'
                                          '🔹необходимость загрузки и вывода фотографий для каждого отеля'
                                          ' (“да/нет”, если "да",'
                                          ' то введите количество фотографий для вывода).\n'
                                          'Примеры формата ввода:\n'
                                          '✔️<i>Лондон, 4, нет</i>\n'
                                          '✔️<i>Лондон, 4, да, 1</i>\n'.format(
                                           name=message.from_user.first_name),
                                          parse_mode='HTML')


@bot.message_handler(content_types=['text'])
def get_command_message(message: telebot.types.Message) -> None:

    if not checking_input_command_message['input_command_message']:
        bot.send_message(message.chat.id, 'Я Вас не понимаю, <b>{name}</b>😳.\n'
                                          'Для начала работы введите одну из следующих команд:\n'
                                          'команда /lowprice (узнать топ самых дешёвых отелей в городе)\n'
                                          'команда /highprice (узнать самых дорогих отелей в городе)\n'
                                          'команда /bestdeal (узнать топ отелей, наиболее подходящих по цене'
                                          'и расположению от центра (узнать самые дешёвые и находятся ближе'
                                          'всего к центру))\n'
                                          'команда /history (узнать историю поиска отелей)'.format(
                                           name=message.from_user.first_name),
                                          parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, 'Думаю')
        data_for_search_hotels = message.text.split(', ')

        try:
            if data_for_search_hotels[2].lower() == 'нет':
                bot.send_message(message.chat.id, lowprice.get_lowprice_hotel(data_for_search_hotels))
            elif data_for_search_hotels[2].lower() == 'да':
                bot.send_message(message.chat.id, lowprice.get_lowprice_hotel(data_for_search_hotels))
                bot.send_photo(message.chat.id, r'https://stiralnihremont.ru/wp-content/uploads/2017/11/%D0%97%D0%BD%D0%B0%D0%BA%D0%B8-%D0%B8-%D1%81%D0%B8%D0%BC%D0%B2%D0%BE%D0%BB%D1%8B-%D0%B4%D0%BB%D1%8F-%D1%81%D1%82%D0%B8%D1%80%D0%BA%D0%B8-%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BA%D1%86%D0%B8%D1%8F-%D1%81%D1%82%D0%B8%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B9.jpg')
            elif data_for_search_hotels[2].lower() != 'да' and data_for_search_hotels[2].lower() != 'нет':
                raise InputError('Ошибка ввода: запрос на вывод фотографий отелей должен должен быть "да или нет".')
        except InputError as exc:
            bot.send_message(message.chat.id, exc)






bot.polling()