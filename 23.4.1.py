sum_symbols = 0
line_counter = 0
try:
    input_file = open('people.txt', 'r')

    for i_line in input_file:
        line_counter += 1
        length = len(i_line)
        if i_line.endswith('\n'):
            length -= 1
        if length < 3:
            raise BaseException('Работа программы завершена на {0} строке! '
                                'В строке {0} длинна имени меньше трех символов.'.format(line_counter))
        sum_symbols += length

    input_file.close()
except FileNotFoundError as exc:
    print(type(exc), '- файл не найден')
finally:
    print('Сумма символов в именах сотрудников', sum_symbols)
