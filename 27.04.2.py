from typing import Callable, Dict

plugins: Dict[str, Callable] = dict()


def register_plugins(func: Callable) -> Callable:
    """Декоратор. Регистрирует функцию как плагин."""
    plugins[func.__name__] = func
    return func


@register_plugins
def greet(name: str) -> str:

    return 'Привет, {}!'.format(name)


@register_plugins
def say_goodbye(name: str) -> str:

    return 'Пока, {}!'.format(name)


greet('Марк')
say_goodbye('Том')

print(plugins)




