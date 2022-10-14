import os
import random


def search_file(directory, file, list_p):

    for i_elem in os.listdir(directory):
        path = os.path.join(directory, i_elem)
        if file == i_elem:
            list_p.append(path)
        elif os.path.isdir(path):
            search_file(path, file, list_p)

    return list_p


list_paths = list()
my_dir = 'Skillbox'
dir_path = os.path.abspath(os.path.join('..', '..', '..', my_dir))

print('Ищем в: ', dir_path)
file_name = input('Имя файла: ')


result = search_file(dir_path, file_name, list_paths)

if not result:
    print('Указанный файл в системе не найден.')
else:
    print('Найдены следующие пути:')
    for i_path in result:
        print(i_path)

random_file = random.choice(result)

file = open(random_file, 'r', encoding='utf-8')

print('Вывод случайного файла из найденных, его путь', random_file)
for i_line in file:
    print(i_line, end='')

