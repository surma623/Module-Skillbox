string = input('Введите строку: ')

counter = 0

symbols = set(".,;:!?")

for sym in string:
    if sym in symbols:
        counter += 1

print('Количество знаков пунктуации: ', counter)

