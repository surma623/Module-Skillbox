words_list = input('Введите три слова: ').split()
text = input('Введите текст: ').split()
count_words = [0, 0, 0]


for index, i_word in enumerate(words_list):
    if i_word in text:
        count_words[index] += 1

print('\nПодсчет слов в тексте:')

result = [
    ' = '.join([words_list[i], str(count_words[i])])
    for i in range(len(words_list))
]

result_str = ' '.join(result)

print('Результат', result_str)

