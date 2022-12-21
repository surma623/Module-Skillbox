BRUCE_WILLIS = 42
input_data = input('Введите строку: ')

try:
    leeloo = int(input_data[4])
    result = BRUCE_WILLIS * leeloo
    print(f'- Leeloo Dallas! Multi-pass № {result}!')
except ValueError as exc:
    print(type(exc), ' - элемент невозможно преобразовать к числу')
except IndexError as exc:
    print(type(exc), ' - указанный в индекс выходит за границы соответствующего списка.')
except Exception as exc:
    print(type(exc), ' - поймано исключение')

