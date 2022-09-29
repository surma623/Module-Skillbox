
def get_list_elem(obj):

    result_list = list()

    if isinstance(obj, tuple):
        obj = list(obj)
    elif isinstance(obj, dict):
        obj = obj.items()

    for index, elem in enumerate(obj):
        if index % 2 == 0:
            result_list.append(elem)

    return result_list


my_string = 'О Дивный Новый мир!'
my_list = [100, 200, 300, 'буква', 0, 2, 'а']
my_tuple = (1, 2, 4, 7, 'd', 'df')
my_dict = {0: 'е', 1: 'о', 2: 'ч', 3: 'ы', 4: 'в', 5: 'н', 6: 'д', 7: 'а', 8: 'ш', 9: 'ц'}
choice = int(input('Выберите тип данных для обработки (1-строка, 2-список, 3-кортеж, 4-словарь): '))

if choice == 1:
    print('Допустим, есть такая строка:', my_string)
    print('Результат:', get_list_elem(my_string))
elif choice == 2:
    print('Допустим, есть такой список:', my_list)
    print('Результат:', get_list_elem(my_list))
elif choice == 3:
    print('Допустим, есть такой кортеж:', my_tuple)
    print('Результат:', get_list_elem(my_tuple))
else:
    print('Допустим, есть такой кортеж:', my_dict)
    print('Результат:', get_list_elem(my_dict))



