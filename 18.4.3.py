text = input('Введите строку: ')

text_list = [symbol for symbol in text]

count_upper = 0
count_lower = 0

for sym in text_list:
    if sym.isupper():
        count_upper += 1
    elif sym.islower():
        count_lower += 1

if count_upper > count_lower:
    print(text.upper())
elif count_upper < count_lower:
    print(text.lower())
else:    # Если ==
    print(text)

# text = input("Введите текст: ")
# lowers = len([letter for letter in text if letter.islower()])
# uppers = len([letter for letter in text if letter.isupper()])
#
# if lowers > uppers:
#     print("Результат:", text.lower())
# else:
#     print("Результат:", text.upper())

