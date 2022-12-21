from typing import Callable
import time


def timer(func: Callable) -> Callable:
    def wrapped_func():
        start = time.time()
        result = func()
        end = time.time()
        run_time = end - start
        print('Время работы: {}'.format(run_time))
        return result

    return wrapped_func


@timer
def hard_func() -> int:
    number = 100
    result = 0
    for _ in range(number + 1):
        result = sum([x ** 2 for x in range(10000)])
    return result


my = hard_func()
print(my)



