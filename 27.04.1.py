from typing import Callable


def cut_bread(func: Callable) -> Callable:
    def wrapped_func(filling):

        print('</----------\>')
        func(filling)
        print('<\______/>')

    return wrapped_func


def cut_ingredients(func: Callable) -> Callable:
    def wrapped_func(filling):

        print('#помидоры#')
        func(filling)
        print('~салат~')

    return wrapped_func


@cut_bread
@cut_ingredients
def cook_sandwich(filling: str) -> None:
    print(filling)


cook_sandwich('--Ветчина--')
