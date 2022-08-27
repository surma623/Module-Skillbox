line = input('Ввеите строку: ')
number_sym = int(input('Введите номер символа: '))
count_same_sym = -1

line_list = list(line)

for index, symbol in enumerate(line_list):
    if index == number_sym - 1:
        print('Символ слева:', line_list[index - 1])
        print('Символ справа:', line_list[index + 1])

for symbol in line_list:
    if symbol == line_list[number_sym - 1]:
        count_same_sym += 1

if count_same_sym == 0:
    print('Таких же символов нет.')

else:
    print(f'Есть такие же символы в количестве:', count_same_sym)