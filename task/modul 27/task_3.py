from typing import Callable, Any
import datetime

import functools


def do_logging(func: Callable) -> Callable:

    @functools.wraps(func)
    def wrapped_func(*args, **kwargs) -> Any:
        print('Название функции: {name}.\nЕе документация: {doc}'.format(
            name=func.__name__,
            doc=func.__doc__
        ))
        result = func(*args, **kwargs)
        if isinstance(result, Exception):
            with open('function_errors.log', 'a') as file_log:
                file_log.write(func.__name__ + ': Error: ' + str(type(result))
                               + ' ' + str(datetime.datetime.now()) + '\n')
            return 'Во время работы функции произошла ошибка. Она записана в файл function_errors.log.'
        else:
            return result

    return wrapped_func


@do_logging
def calculate_squares(number: int) -> int:
    """
    Функция возвращающая квадрат переданного в нее числа.

    :param number: переданное число.
    :return: переданное число, возведенное в квадрат
    """

    return number ** 2


@do_logging
def divide_number(number: int) -> float:
    """
    Функция возвращающая частное от деления переданного числа на делитель.

    :param number: переданное число
    :return: частное.
    :except ZeroDivisionError: В случае если происходит деление числа на ноль, то вызывается исключение.
    """
    try:
        result = number / 0

        return result
    except ZeroDivisionError as exc:
        return exc


@do_logging
def calculate_even_nums() -> list[int]:
    """
    Функция, возвращающая список четных чисел от 0 до 10.

    :return: список четных чисел.
    """

    return [x for x in range(11) if x % 2 == 0]


@do_logging
def add_numbers(number: int) -> int:
    """
    Функция, возвращающая сумму переданного числа и числа "4".

    :param number: переданное число
    :return: сумма чисел.
    :except TypeError: В случае если происходит сложение разных типов данных, вызывается исключение.
    """

    try:
        result = number + '4'

        return result
    except TypeError as exc:
        return exc


print('Результат работы функции: {} \n'.format(calculate_squares(2)))
print('Результат работы функции: {} \n'.format(divide_number(3)))
print('Результат работы функции: {} \n'.format(calculate_even_nums()))
print('Результат работы функции: {} \n'.format(add_numbers(4)))