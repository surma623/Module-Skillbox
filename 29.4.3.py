from functools import wraps
from datetime import datetime
import time


def clock_create_time(cls):
    """Декоратор, вычисляющий время инициализации экземпляров класса."""

    @wraps(cls)
    def wrapper(*args, **kwargs):
        instance = cls(*args, **kwargs)
        print('Время создания инстанса класса: {0}\n'
              'Список методов экземпляра класса: {1}'.format(
                datetime.now(),
                dir(cls)
              ))
        return instance
    return wrapper


@clock_create_time
class Tasks:

    def __init__(self, number: int) -> None:
        self.number = number

    def calculate_even_num(self) -> list[int]:
        return [x for x in range(self.number + 1) if x % 2 == 0]

    def calculate_odd_num(self) -> list[int]:
        return [x for x in range(self.number + 1) if x % 2 != 0]


example_1 = Tasks(number=10)
time.sleep(2)
example_2 = Tasks(number=10)



print(example_1.calculate_even_num())
print(example_1.calculate_odd_num())



