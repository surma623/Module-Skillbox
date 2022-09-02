
num_competitors = int(input('Кол-во участников: '))
num_members_team = int(input('Кол-во человек в команде: '))

if num_competitors % num_members_team != 0:
    print(f'Ошибка! {num_competitors} участников невозможно поделить на команды по {num_members_team} человек.')

else:
    num = 1

    competitors_list = []

    for _ in range(num_competitors // num_members_team):
        competitors_list.append(list(range(num, num + (num_competitors // num_members_team))))
        num += (num_competitors // num_members_team)

    print(competitors_list)
