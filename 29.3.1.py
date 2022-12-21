from typing import Callable
import functools
from typing import Optional


def repeat_number(_func: Optional[Callable] = None, *, number_n: int = 10) -> Callable:
    def repeat(func: Callable) -> Callable:
        """Функция-декоратор, выполняет переданную функцию n раз."""

        @functools.wraps(func)
        def wrapped_func(*args, **kwargs) -> None:
            for _ in range(number_n):
                func(*args, **kwargs)

        return wrapped_func
    if _func is None:
        return repeat
    return repeat(_func)


@repeat_number
def greeting(name: str) -> None:
    print('Привет, {name}!'.format(name=name))


res = greeting('Паша')
