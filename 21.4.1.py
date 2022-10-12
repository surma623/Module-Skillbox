def ask_user(question,
             complaint='Невернный ввод. Введите сообщение еще раз',
             retries=3):

    while True:
        answer = input(question).lower()
        if answer == 'да':
            return 1
        if answer == 'нет':
            return 0
        retries -= 1
        if retries == 0:
            break

        print(complaint)
        print('Количество попыток:', retries)


ask_user('Записать файл?')
ask_user('Удалить файл?',
         'Действительно, удалить файл?')
ask_user('Вы хотите выйти?',
         retries=2)