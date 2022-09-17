while True:
    grats_tamp = input('Введите шаблон поздравления, в шаблоне можно использовать конструкцию {name} и {age}:'
                       'С днём рождения, {name}! С {age}-летием тебя! ')
    if '{name}' and '{age}' in grats_tamp:
        break
    else:
        print('Ошибка: отсутствуют одна или две конструкции.')

names_list = input('Список людей через запятую: ').split(', ')

ages_str = input('Возраст людей через пробел: ')
ages = [int(i_number) for i_number in ages_str.split()]

for i_man in range(len(names_list)):
    print(grats_tamp.format(name=names_list[i_man], age=ages[i_man]))

people = [' '.join([names_list[i], str(ages[i])])
          for i in range(len(names_list))
          ]

people_str = ', '.join(people)

print('\nИменинники:', people_str)