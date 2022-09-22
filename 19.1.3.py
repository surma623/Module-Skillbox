phone_book = dict()

while True:     # для выхода из цикла введите "exit"
    print('Текущие контакты на телефоне:')
    if phone_book:
        for i_key in phone_book:
            print(i_key, phone_book[i_key], '\n')

    else:
        print('<Пусто>')

    name = input('Введите имя (для выхода из программы наберите "exit): ')
    if name in phone_book:
        print('Ошибка: такое имя уже существует.\n')
    elif name == 'exit':
        print('Заполнение книги контактов окончено.')
        break
    else:
        phone_number = int(input('Введите номер телефона: '))
        phone_book[name] = phone_number

