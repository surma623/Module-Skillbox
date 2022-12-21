class DivisionError(Exception):
    pass


with open('num.txt', 'r') as file:

    for i_line in file:
        try:
            line = i_line.split()
            if int(line[0]) < int(line[1]):
                raise DivisionError('Нельзя делить меньшее на большее')
            result = int(line[0]) / int(line[1])
            print('Результат:', result)
        except DivisionError as exc:
            print(exc)
        except ValueError:
            print('Значение должно быть числом.')






