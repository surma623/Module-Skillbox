number = int(input('Введите целое число: '))

numbers_dict = dict()

for num in range(1, number + 1):
    numbers_dict[num] = num ** 2

print('Результат:', numbers_dict)