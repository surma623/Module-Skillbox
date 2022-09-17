path = input('Путь к файлу: ')

disk_choice = input('На каком диске должен лежать файл: ').upper()
format_file = input('Требуемое расширение файла: ').lower()

if not path.startswith(disk_choice):
    print('Ошибка: не тот диск')
elif not path.endswith(format_file):
    print('Ошибка: не то расширение')
else:
    print('Путь корректен!')

