import string
import random
string.ascii_letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


first_list = [random.choice(string.ascii_letters) for _ in range(10)]
second_list = [random.choice(string.ascii_letters) for _ in range(10)]

first_dict = dict()
second_dict = dict()

for index, values in enumerate(first_list):
    first_dict[index] = values

for index, values in enumerate(second_list):
    second_dict[index] = values

print('Первый список:', first_list)
print('Второй список:', second_list)
print('\nПервый словарь:', first_dict)
print('Второй словарь:', second_dict)



