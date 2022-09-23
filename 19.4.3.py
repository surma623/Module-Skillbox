string = set(input('Введите строку: '))

unique_nums = list()
result = ''

for sym in string:
    if '0' <= sym <= '9':
        unique_nums.append(int(sym))

unique_set = set(unique_nums)

for sym in unique_set:
    result += str(sym)

print('Различные цифры строки:', result)

# text_unique = set(string)
# result = text_unique & set("0123456789")
# # При помощи множества выделим из строки только общие элементы (цифры) и посчитаем длину множества
# print(result)