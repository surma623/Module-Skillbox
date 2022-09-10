line = input('Введите строку: ')
symbol = input('Введите дополнительный символ: ')

first_list = [sym * 2 for sym in line]
square_list = [i_elem + symbol for i_elem in first_list]

print('Список удвоенных символов:', first_list)
print('Склейка с дополнительным символом:', square_list)