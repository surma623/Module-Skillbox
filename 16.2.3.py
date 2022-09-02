def is_movie_exist(movie, films_list):
    for i_movie in films_list:
        if movie == i_movie:
            return True
    return False

films = [
    'Крепкий орешек', 'Назад в будущее', 'Таксист',
    'Леон', 'Богемская рапсодия', 'Город грехов',
    'Мементо', 'Отступники', 'Деревня',
    'Проклятый остров', 'Начало', 'Матрица'
]

my_list = []

while True:
    print('\nВаш текущий топ фильмов:', my_list)
    new_movie = input('Название фильма: ')
    if is_movie_exist(new_movie, films):
        print('Команды: добавить, вставить, удалить')
        command = input('Введите команду: ')
        if command == 'добавить':
            if is_movie_exist(new_movie, my_list):
                print('Этот фильм уже есть в вашем списке.')
            else:
                my_list.append(new_movie)
        elif command == 'удалить':
            if is_movie_exist(new_movie, my_list):
                my_list.remove(new_movie)
            else:
                print('Такого фильма нет в вашем списке.')
        elif command == 'вставить':
            if is_movie_exist(new_movie, my_list):
                print('Этот фильм уже есть в вашем списке.')
            else:
                index = int(input('На какое место вставить? '))
                my_list.insert(index - 1, new_movie)
        else:
            print('Ошибка: команда введена неправильно')
    else:
        print('Такого фильма нет на сайте.')