from typing import Callable, Any
import functools
from datetime import datetime


def do_logging(meth: Callable) -> Callable:
    """Декоратор, совершающий логирование метода экземпляра класса,
     а также выводящий на экран название метода и его документацию.
     """
    @functools.wraps(meth)
    def wrapped_func(*args, **kwargs) -> Any:
        print('Название метода: {name}.\nЕго документация: {doc}'.format(
            name=meth.__name__,
            doc=meth.__doc__
        ))
        print(meth(*args, **kwargs))
        with open('method.log', 'a', encoding='UTF-8') as file_log:
            file_log.write(meth.__name__ + ' аргумент ' + repr(args[1]) + ' ' + meth.__doc__ + str(datetime.now()) + '\n')
        return 'Данные о методе записаны в файл method.log.'

    return wrapped_func


def for_all_method(decorator: Callable) -> Callable:

    @functools.wraps(decorator)
    def decorate(cls):
        for i_method_name in dir(cls):
            if not i_method_name.startswith('__'):
                cur_method = getattr(cls, i_method_name)
                decorated_method = decorator(cur_method)
                setattr(cls, i_method_name, decorated_method)
        return cls
    return decorate


@for_all_method(do_logging)
class MyClass:

    def __init__(self, number=1):
        self.number = number

    def method_1(self, number):
        """Документация к методу 1"""
        return self.number + number

    def method_2(self, number):
        """Документация к методу 2"""
        return self.number + number

    def method_3(self, number):
        """Документация к методу 3"""
        return self.number + number



test_1 = MyClass()

print(test_1.method_1(1))

print(test_1.method_2(1))

print(test_1.method_3(1))