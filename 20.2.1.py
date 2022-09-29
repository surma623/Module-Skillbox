string = input('Введите строку: ')

tilde_index_list = []

for index, sym in enumerate(string):
    if sym == '~':
        tilde_index_list.append(index)

print('Ответ:', *tilde_index_list)