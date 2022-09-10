first_num = int(input('Введите число А: '))
second_num = int(input('Введите число Б: '))

list_even_num = [x for x in range(first_num, second_num + 1) if x % 2 == 0]

print(list_even_num)