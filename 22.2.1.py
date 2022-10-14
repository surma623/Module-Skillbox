import os

file = 'tasks'

file_path = os.path.abspath(os.path.join('..', file))

print(file_path)
if not os.path.exists(file_path):
    print('Такого файла не существует')
else:
    if os.path.isdir(file_path):
        print('Это директория')
    elif os.path.islink(file_path):
        print('Это ссылка')
    elif os.path.isfile(file_path):
        print('Это файл')
        print('Размер файла: {} байт'.format(os.path.getsize(file_path)))

