import datetime
from typing import List
from bestdeal import User


def is_date_valid(date: str) -> bool:
    """Функция, проверяющая дату на корректность.

    :param:
        checking_date: проверяемая дата
        valid (bool): значение корректности проверяемой даты

    :return: True - если дата корректна, False - если нет
    :except IndexError, ValueError: эти два исключения вызываются в случае ввода
     некоторых вариантов некорректной строки даты и призваны обеспечить нормальную работу программы
    """
    valid = False
    checking_date = date.split('-')
    if len(checking_date) == 3 and len(checking_date[0]) == 4 and len(checking_date[1]) == 2 \
            and len(checking_date[2]) == 2:
        today_date = datetime.date.today()
        current_date = str(today_date).split('-')
        try:
            if (int(checking_date[0]) == int(current_date[0])) and (int(checking_date[1]) == int(current_date[1])) \
                    and (int(checking_date[2]) >= int(current_date[2])) or (
                    int(checking_date[0]) == int(current_date[0])) \
                    and (int(checking_date[1]) > int(current_date[1])) or (
                    int(checking_date[0]) > int(current_date[0])):

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
            else:
                return False
        except (IndexError, ValueError):
            pass
    else:
        return False

    return valid


def is_range_date_valid(date_check_in: List[str], date_check_out: List[str], user: User) -> bool:
    """Функция, проверяющая диапазон введенных дат на корректность.

    :param:
        date_check_in: дата начала пребывания в отеле
        date_check_out: дата окончания пребывания в отеле
        valid (bool): значение корректности проверяемого диапазона времени
        user: объект класса User, содержащий данные об вводимой пользователем информации

    :return: True, если диапазон даты корректна, False, если нет
    """
    user.block_choose_date = False
    valid = True

    if (date_check_in[0] == date_check_out[0]) and (date_check_in[1] == date_check_out[1]) \
            and (date_check_in[2] >= date_check_out[2]) or (date_check_in[0] == date_check_out[0]) \
            and (date_check_in[1] > date_check_out[1]) or (date_check_in[0] > date_check_out[0]):
        valid = False
        return valid

    # Данный блок кода необходим для проверки длины диапазона времени (для корректного отображения общей суммы
    # проживания в отеле диапазон бронирования номера не должен превышать 28 дней)

    if date_check_in[1][0] == '0':
        date_check_in[1] = date_check_in[1][1]
    elif date_check_in[2][0] == '0':
        date_check_in[2] = date_check_in[2][1]
    if date_check_out[1][0] == '0':
        date_check_out[1] = date_check_out[1][1]
    elif date_check_out[2][0] == '0':
        date_check_out[2] = date_check_out[2][1]

    if (int(date_check_out[0]) - int(date_check_in[0])) > 1:
        valid = False
        user.block_choose_date = True
        return valid
    elif (int(date_check_out[0]) - int(date_check_in[0])) == 1 and int(date_check_in[1]) == 12 \
            and int(date_check_out[1]) == 1:
        if ((31 - int(date_check_in[2])) + int(date_check_out[2])) > 28:
            valid = False
            user.block_choose_date = True
            return valid
    elif (int(date_check_out[0]) - int(date_check_in[0])) == 1 and int(date_check_in[1]) == 12:
        if ((12 - int(date_check_in[1])) + int(date_check_out[1])) > 1:
            valid = False
            user.block_choose_date = True
            return valid
    elif (date_check_in[0] == date_check_out[0]) and (int(date_check_out[1]) - int(date_check_in[1])) > 1:
        valid = False
        user.block_choose_date = True
        return valid
    elif (date_check_in[0] == date_check_out[0]) and (int(date_check_out[1]) - int(date_check_in[1])) == 1:
        if int(date_check_in[1]) in [1, 3, 5, 7, 8, 10, 12]:
            if ((31 - int(date_check_in[2])) + int(date_check_out[2])) > 28:
                valid = False
                user.block_choose_date = True
                return valid
        elif int(date_check_in[1]) in [4, 6, 9, 11]:
            if ((30 - int(date_check_in[2])) + int(date_check_out[2])) > 28:
                valid = False
                user.block_choose_date = True
                return valid
        elif int(date_check_in[1]) == 2:
            if ((28 - int(date_check_in[2])) + int(date_check_out[2])) > 28:
                valid = False
                user.block_choose_date = True
                return valid
        elif int(date_check_in[1]) == 2 and int(date_check_in[0]) in range(2024, 2100, 4):
            if ((29 - int(date_check_in[2])) + int(date_check_out[2])) > 28:
                valid = False
                user.block_choose_date = True
                return valid
    elif date_check_in[0] == date_check_out[0] and date_check_out[1] == date_check_in[1]:
        if (int(date_check_out[2]) - int(date_check_in[2])) > 28:
            valid = False
            user.block_choose_date = True
            return valid

    return valid


def is_price_valid(price: float) -> bool:
    """Функция, проверяющая введенную цену на корректность.

    :param:
        price: цена

    :return: True, если цена корректна, False, если нет
    """

    if price >= 1 and price <= 100:
        return True
    else:
        return False


def is_range_price_valid(min_p: float, max_p: float) -> bool:
    """Функция, проверяющая диапазон введенных цен на корректность.

    :param:
        min_p: минимальная цена
        max_p: максимальная цена

    :return: True, если диапазон цен корректен, False, если нет
    """

    if min_p > max_p or min_p == max_p:
        return False
    else:
        return True


def is_distance_valid(distance: float) -> bool:
    """Функция, проверяющая введенное расстояние на корректность.

    :param:
        distance: расстояние

    :return: True, если расстояние корректна, False, если нет
    """

    if distance >= 0.1 and distance <= 50:
        return True
    else:
        return False


def is_range_distance_valid(start_point: float, end_point: float) -> bool:
    """Функция, проверяющая диапазон введенных точек расстояния на корректность.

    :param:
        start_point: стартовая точка расстояния
        end_point: конечная точка расстояния

    :return: True, если диапазон точек расстояния корректен, False, если нет
    """
    if start_point > end_point or start_point == end_point:
        return False
    else:
        return True