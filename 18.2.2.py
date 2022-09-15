name = input('Введите имя: ')
debt = int(input('Введите долг: '))

output = '{0}! {0}, привет! Как дела, {0}? Где мои {1} рублей? {0}! {1} рублей!'.format(
    name,
    debt
)

print(output)