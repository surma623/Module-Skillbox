import os


def search_file(directory, file, list_p):

    for i_elem in os.listdir(directory):
        path = os.path.join(directory, i_elem)
        if file == i_elem:
            list_p.append(path)
            # print(path)
        elif os.path.isdir(path):
            # result = search_file(path, file, list_p)
            search_file(path, file, list_p)
            # if result:
            #     break
    # else:
    #     result = None

    # return result
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
