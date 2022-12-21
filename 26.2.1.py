import random

number_numbers = int(input('Введите количество чисел: '))
numbers = [random.randint(-100, 100) for _ in range(number_numbers)]
iterator = iter(numbers)

while True:
    try:
        print(next(iterator))
    except StopIteration:
        print('Итератор пуст.')
        break
