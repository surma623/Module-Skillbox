
def get_surname_name(info_passport):

    series_pass = input('Ведите серию паспорта: ').split(', ')
    series_tuple = tuple([int(i_num) for i_num in series_pass])
    number_pass = None

    for i_series, i_number in info_passport.items():
        if series_tuple == i_series:
            number_pass = ', '.join([i_number[0], i_number[1]])
            return series_pass, number_pass

    return None


data = {
    (5000, 123456): ('Иванов', 'Василий'),
    (6000, 111111): ('Иванов', 'Петр'),
    (7000, 222222): ('Медведев', 'Алексей'),
    (8000, 333333): ('Алексеев', 'Георгий'),
    (9000, 444444): ('Георгиева', 'Мария')
}

result = get_surname_name(data)

if result is None:
    print('Такого человека нет.')
else:
    print('Фамилия и имя по номеру и серии паспорта - {0}: {1}'.format(' '.join(result[0]), result[1]))