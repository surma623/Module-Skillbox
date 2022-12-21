from collections.abc import Iterable


# Вариант класс-итератор.
class SquaringIteration:
    """ Класс-итератор создает объект-итератор, возвращающий квадрат числа из последовательности от 1 до N.

    Arguments:
        num_n (int): число N

    Attributes:
        self.__num_n (int): число N
        self.__counter (int): счетчик N

    """

    def __init__(self, num_n: int) -> None:
        self.__num_n = num_n
        self.__counter = 1

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if self.__counter <= self.__num_n:
            self.__counter += 1
            return (self.__counter - 1) ** 2
        raise StopIteration


number_n = int(input('Введите натуральное число N: '))
squaring = SquaringIteration(number_n)

for num in squaring:
    print(num, end=' ')

print()


# Вариант функция-генератор.
def squaring_generation(num_n: int) -> Iterable[int]:
    """
    Возвращает квадрат числа для каждого значения из последовательности от 1 до числа N.

    :param num_n: крайнее число в последовательности.
    :return: элемент итерируемого объекта
    """

    counter = 1

    while counter <= num_n:
        yield counter ** 2
        counter += 1


squaring_2 = squaring_generation(number_n)

for num in squaring_2:
    print(num, end=' ')

print()

# Вариант генераторное выражение.
squaring_3 = (i_num ** 2 for i_num in range(1, number_n + 1))

for num in squaring_3:
    print(num, end=' ')


