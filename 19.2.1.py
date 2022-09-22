small_storage = {
    'гвозди': 5000,
    'шурупы': 3040,
    'саморезы': 2000
}

big_storage = {
    'доски': 1000,
    'балки': 150,
    'рейки': 600
}

big_storage.update(small_storage)

name_item = input('Введите название товара: ')

if name_item in big_storage:
    print('Количество товара {0} : {1}.'.format(name_item, big_storage.get(name_item)))
else:
    print('Ошибка: такого товара на складе нет.')