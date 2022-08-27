text = input('Введите строку: ')
count = 0
text_list = list(text)

for index, symbol in enumerate(text_list):
    if symbol == ':':
        text_list[index] = ';'
        count += 1

for sym in text_list:
    print(sym, end='')
print('\nКоличество исправлений', count)








