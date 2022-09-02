
first_message = input('Первое сообщение: ')
second_mesage = input('Второе сообщение: ')

spec_sym_first_m = first_message.count('!') + first_message.count('?')
spec_sym_second_m = second_mesage.count('!') + second_mesage.count('?')

if spec_sym_first_m > spec_sym_second_m:
    print('Третье сообщение:', first_message, second_mesage)
elif spec_sym_first_m < spec_sym_second_m:
    print('Третье сообщение:', second_mesage, first_message)
else:
    print('Ой')
