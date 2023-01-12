import sqlite3
from typing import List, Optional, Tuple
from user import User


def write_data_into_database(user: User) -> None:
    """Функция, осуществляющая запись информации о поиске отелей в базу данных.

    :param:
        user: объект класса User, содержащий данные о вводимой пользователем информации
    """
    database = sqlite3.connect('history_search.db')

    cursor = database.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS history_search(
        chat_id  TEXT,
        command TEXT,
        date_time TEXT,
        name_city TEXT,
        name_hotels TEXT
    ) """)

    database.commit()

    hotels = '; '.join([hotel['name_hotel'] for hotel in user.hotel_data])

    cursor.execute("INSERT INTO history_search VALUES (?, ?, ?, ?, ?)", (user.chat_id, user.user_command,
                                                                         user.datetime_input_command, user.city,
                                                                         hotels))
    database.commit()
    database.close()


def get_history_search(user: User) -> Optional[List[Tuple]]:
    """Функция, осуществляющая вывод информации об истории поиска отелей из базы данных.

        :param:
            user: объект класса User, содержащий данные о вводимой пользователем информации
    """

    database = sqlite3.connect('history_search.db')

    cursor = database.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS history_search(
        chat_id  TEXT,
        command TEXT,
        date_time TEXT,
        name_city TEXT,
        name_hotels TEXT
    ) """)

    database.commit()

    cursor.execute(f"""SELECT command, date_time, name_city, name_hotels FROM
     history_search WHERE {user.chat_id} = chat_id""")
    history_search = cursor.fetchall()

    database.close()

    return history_search

