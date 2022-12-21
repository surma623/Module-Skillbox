from typing import Callable, Any
import functools
import time


def sleep(func: Callable) -> Callable:
    """Декоратор, осуществляющий задержку начала работы функции на 3 секунды."""

    @functools.wraps(func)
    def wrapped_func(*args, **kwargs) -> Any:
        time.sleep(3)
        result = func(*args, **kwargs)
        return result

    return wrapped_func


@sleep
def calculate_even_nums() -> list[int]:
    """
    Функция, возвращающая список четных чисел от 0 до 10.

    :return: список четных чисел.
    """

    return [x for x in range(11) if x % 2 == 0]


print(calculate_even_nums())
