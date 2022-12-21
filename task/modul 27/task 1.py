from typing import Callable, Any
import functools


def worry(func: Callable) -> Callable:
    """Декоратор, выводящий две строки перед выводом результата работы функции."""

    @functools.wraps(func)
    def wrapped_func(*args, **kwargs) -> Any:
        print('Как дела? Хорошо.')
        print('А у меня не очень! Ладно, держи свою функцию.')
        result = func(*args, **kwargs)
        return result

    return wrapped_func


@worry
def test_1() -> None:
    """Функция, выводящая строку текста."""

    print('<Тут что-то происходит...>\n')


@worry
def test_2(number: int) -> int:
    """
    Функция возвращающая квадрат переданного в нее числа.

    :param number: переданное число.
    :return: переданное число, возведенное в квадрат
    """

    return number ** 2


@worry
def test_3() -> list[int]:
    """
    Функция, возвращающая список четных чисел от 0 до 10.

    :return: список четных чисел.
    """

    return [x for x in range(11) if x % 2 == 0]


test_1()
print(test_2(2), '\n')
print(test_3())

