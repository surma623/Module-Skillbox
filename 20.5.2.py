
phonebook = dict()

while True:

    surname_name_contacts = input('\nВведите фамилию и имя (через пробел): ')
    if surname_name_contacts == 'Выйти':
        print('Редактирование книги контактов окончено.')
        break
    else:
        surname_name_contacts = surname_name_contacts.split()
        number = int(input('Введите номер контакта: '))

        surname_name_con_tuple = tuple([i_elem for i_elem in surname_name_contacts])

        if surname_name_con_tuple in phonebook:
            print('Такие фамилия и имя уже есть в словаре. Введите имя контакта по новому.')
            continue
        else:
            phonebook[surname_name_con_tuple] = number

            print('Текущий список контактов:')
            for name, number in phonebook.items():
                print(' '.join([name[0], name[1]]), ':', number)





