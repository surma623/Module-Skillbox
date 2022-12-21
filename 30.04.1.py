from typing import List

# Задача 1. Однострочный код

numbers: List[str] = input('Введите числа: ').split()

print(list((sorted(map(int, numbers)))))


# Задача 2. Однострочный код 2

numbers: str = input('Введите числа: ')

print(list(filter(lambda x: x.isalpha() and x.islower(), numbers)))

