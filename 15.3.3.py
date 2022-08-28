word_text = ''
word_text_list = []
user_words_list = []
count_words = [0, 0, 0]
count_words_list = 0

for i in range(3):
    word = input(f'Введите {i + 1} слово: ')
    user_words_list.append(word)


print()
while word_text != 'end':
    word_text = input('Слово из текста: ')
    count_words_list += 1
    word_text_list.append(word_text)

for i in range(count_words_list):
    if user_words_list[0] == word_text_list[i]:
        count_words[0] += 1
    elif user_words_list[1] == word_text_list[i]:
        count_words[1] += 1
    elif user_words_list[2] == word_text_list[i]:
        count_words[2] += 1

print('\nПодсчет слов в тексте:')

for i in range(3):
    print(user_words_list[i] + ':', count_words[i])



words_list = []
counts = [0, 0, 0]

for i in range(3):
    print("Введите", i+1, "слово", end=' ')
    word = input()
    words_list.append(word)

text = input("Слово из текста: ")
while text != "end":
    for index in range(3):
        if words_list[index] == text:
            counts[index] += 1
    text = input("Слово из текста: ")

print("Подсчёт слов в тексте")
for i in range(3):
    print(words_list[i], ':', counts[i])
