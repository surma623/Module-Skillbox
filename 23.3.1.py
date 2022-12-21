
file = None

try:
    string = int(input('Введите строку: '))
    file = open('text.txt', 'w')
    file.write(str(string))
except FileExistsError as exc:
    print(type(exc), ' - ошибка: файл уже существует.')
except ValueError as exc:
    print(type(exc), ' - невозможно преобразовать значение в целое число.')
except Exception as exc:
    print((type(exc), '- Случайная ошибка'))
else:
    print('Ошибок в программе не выявлено')
finally:
    if file and not file.closed:
        file.close()
