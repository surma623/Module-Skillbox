print(ord("а"), ord("я"), ord("ё"), chr(97))

text = input("Введите текст: ")
delta = int(input("Введите сдвиг: "))
alphabet = [chr(index) for index in range(ord("а"), ord("я") + 1)]  # заполняем список буквами алфавита
# Думаем над структурой алгоритма: [вариант_1 если условие_1 иначе вариант_2 for буква in текст]
new_text = [alphabet[(alphabet.index(letter) + delta) % len(alphabet)] if letter in alphabet else letter
            for letter in text.lower()
            ]

print(''.join(new_text))