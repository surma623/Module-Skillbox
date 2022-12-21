
def give_names_to_ages(file, dict_ages_names):

    input_file = open(file, 'r')

    for i_line in input_file:
        name = input('Введите имя человека: ')
        dict_ages_names[name] = i_line

    input_file.close()


def write_file(dict_ages_names):

    output_file = open('result.txt', 'x', encoding='utf-8')

    for key, value in dict_ages_names.items():
        output_file.write(key + ' - ' + value)

    output_file.close()


file_name = 'ages.txt'
dict_names_ages = dict()

try:
    give_names_to_ages(file_name, dict_names_ages)
    write_file(dict_names_ages)
except FileExistsError as exc:
    print(type(exc), ' - попытка создания файла, который уже существует.')
except PermissionError as exc:
    print(type(exc), ' - на чтение ожидался файл, но это оказалась директория.')
except (TypeError, ValueError) as exc:
    print(type(exc), ' - неверный тип данных и некорректное значение.')

