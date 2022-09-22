path = input('Путь к файлу: ')

disk_choice = input('На каком диске должен лежать файл: ').upper()
format_file = input('Требуемое расширение файла: ').lower()

if path.startswith(disk_choice) and path.endswith(format_file):
    print('Путь корректен!')
else:
    print('Путь некорректен!')


