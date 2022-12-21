from typing import Optional, Callable, Any
import functools
import time


def sleep_timer(_func: Optional[Callable] = None, *, seconds: int = 1) -> Callable:
    def sleep(func: Callable) -> Callable:
        """Декоратор, осуществляющий задержку начала работы функции на 3 секунды."""

        @functools.wraps(func)
        def wrapped_func(*args, **kwargs) -> Any:
            time.sleep(seconds)
            result = func(*args, **kwargs)
            return result

        return wrapped_func
    if _func is None:
        return sleep
    return sleep(_func)


@sleep_timer(seconds=5)
def calculate_even_nums() -> list[int]:
    """
    Функция, возвращающая список четных чисел от 0 до 10.

    :return: список четных чисел.
    """

    return [num for num in range(11) if num % 2 == 0]


print(calculate_even_nums())