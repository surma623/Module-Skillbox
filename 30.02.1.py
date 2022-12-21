from functools import wraps
from typing import Callable
import builtins


def count_func(func: Callable, count: int = 0) -> Callable:

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal count
        count += 1
        print('Функция была вызвана {} раз.'.format(count))
        result = func(*args, **kwargs)

        return result
    return wrapper


@count_func
def calculate_even_num(num: int) -> list[int]:

    return [x for x in range(num + 1) if x % 2 == 0]


@count_func
def calculate_odd_num(num: int) -> list[int]:

    return [x for x in range(num + 1) if x % 2 != 0]


for _ in range(5):
    print(calculate_even_num(10))

print()
for _ in range(5):
    print(calculate_odd_num(10))


for name in dir(builtins):
    print(name)