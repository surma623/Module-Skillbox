from contextlib import contextmanager
from collections.abc import Iterator
import os


@contextmanager
def in_dir(path) -> Iterator:
    flag = True
    try:
        os.chdir(path)
        yield True
    except FileNotFoundError as exc:
        print(exc)
        if isinstance(exc, FileNotFoundError):
            flag = False
        yield False
    finally:
        if flag:
            cur_path = os.getcwd()
            os.chdir(cur_path)


my_path = os.path.abspath(os.path.sep)

with in_dir(my_path) as my_flag:

    if my_flag:
        print('Файлы директории: {}'.format(my_path))
        for file in os.listdir():
            print(file)



