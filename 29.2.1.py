from contextlib import contextmanager
from collections.abc import Iterator
import time


@contextmanager
def clock_timer() -> Iterator:
    start = time.time()
    try:
        yield

    except TypeError as exc:
        print(exc)

    finally:
        print(time.time() - start)


with clock_timer() as t_1:
    print('Первая программа')
    x_lst = [x for x in range(10000000) if x % 2 == 0]
    x = 1 + 'a'