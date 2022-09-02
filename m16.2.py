zoo = ['lion', 'kangaroo', 'elephant', 'monkey']

i_zoo =zoo.index('lion')

zoo.insert(i_zoo + 1, 'bear')

zoo_without_eliph = zoo.remove('elephant')

print('Результат работы программы:')
print('Зоопарк:', zoo)
print('Лев сидит в клетке номер', i_zoo + 1)
print('Обезьяна сидит в клетке номер', (zoo.index('monkey') + 1) )

