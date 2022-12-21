from typing import Callable


def do_twice(func: Callable) -> Callable:
    """Функция-декоратор, дважды выполняет переданную функцию."""

    def wrapped_func(*args, **kwargs) -> None:
        func(*args, **kwargs)
        func(*args, **kwargs)

    return wrapped_func


@do_twice
def greeting(name: str) -> None:
    print('Привет, {name}!'.format(name=name))


res = greeting('Паша')

