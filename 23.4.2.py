import logging
logging.basicConfig(filename="log.txt", level = logging.INFO)

string = ''
file = 'words.txt'
line_counter = 0
palindrome_counter = 0
input_file = None

try:
    input_file = open(file, 'r')
    try:
        for i_line in input_file:
            line_counter += 1
            for index in range(len(i_line) - 2, -1, -1):
                if i_line[index].isdigit():
                    raise ValueError(' в слове \'{0}\' в строке № {1} найдено числовое значение '
                                     '- это критическая ошибка, '
                                     'работа программы прервана'.format(i_line[:len(i_line) - 1], line_counter))
                string += i_line[index]
            if string == i_line[:len(i_line) - 1]:
                palindrome_counter += 1
            string = ''
    except ValueError as exc:
        logging.error(str(exc),)
        print(type(exc), '- ошибка записана в отчет. Работа программы была прервана.')


except FileNotFoundError:
    print('Файл под именем {} не найден.'.format(file))

finally:
    if input_file and not input_file.closed:
        input_file.close()
    print('Количество палиндромов', palindrome_counter)
