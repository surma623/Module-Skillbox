first_num = int(input('Левая граница: '))
second_num = int(input('Правая граница: '))

cube_list = [x ** 3 for x in range(first_num, second_num + 1)]
square_list = [x ** 2 for x in range(first_num, second_num + 1)]

print('Список кубов чисел в диапазоне от 5 до 10:', cube_list)
print('Список квадратов чисел в диапазоне от 5 до 10:', square_list)