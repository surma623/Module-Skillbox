name = input('Введите имя: ')
number_order = int(input('Номер заказа: '))

output = 'Здравствуйте, {name}! Ваш номер заказа: {order}. Приятного дня!'.format(
    name=name,
    order=number_order
)
print(output)