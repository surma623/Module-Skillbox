import random

random_num_1 = random.randint(100, 200)
random_num_2 = random.randint(100, 200)


nums_1 = [29, 17, 10, 15, 13, 22, 12, 22, 7, 24, 26, 3, 11, 2, 3, 16, 19, 21, 2, 3, 8, 27, 2, 17, 2, 20, 12, 21, 3, 1]
nums_2 = [16, 21, 30, 24, 5, 7, 23, 13, 11, 5, 21, 5, 19, 9, 12, 9, 15, 16, 29, 8, 16, 1, 22, 15, 16, 9, 1, 13, 21, 21]

nums_1_set = set(nums_1)
nums_2_set = set(nums_2)

print('Результат работы программы:\n')
print('Первое множество:', nums_1_set)
print('Второе множество:', nums_2_set, '\n')

print('Минимальный элемент 1-го множества:', min(nums_1_set))
print('Минимальный элемент 2-го множества:', min(nums_1_set))
nums_1_set.discard(min(nums_1_set))
nums_2_set.discard(min(nums_2_set))

print('Случайное число для 1-го множества:', random_num_1)
print('Случайное число для 2-го множества:', random_num_2)

nums_1_set.add(random_num_1)
nums_2_set.add(random_num_2)

print('Объединение множеств:', nums_1_set.union(nums_2_set))
print('Пересечение множеств:', nums_2_set.intersection(nums_1_set))
print('Элементы, входящие в nums_2, но не входящие в nums_1:', nums_2_set.difference(nums_1_set))
