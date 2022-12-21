import random

while True:
    try:
        max_num = int(input('Введите максимальное число: '))
    except ValueError:
        print('Введите числовые значения!')
    else:
        guess_number = random.randint(1, max_num)
        max_range_number = {num for num in range(1, max_num + 1)}

        while True:

            guessed_num_flag = False
            try:
                answer = input('Нужное число есть среди вот этих чисел: ').split()

                if ''.join(answer) == 'Помогите!':
                    print('Артём мог загадать следующие числа:', *max_range_number)
                    break

                answer_set = {int(elem) for elem in answer}

            except ValueError:
                print('Нужно ввести либо числовые значения либо слово "Помогите"')
            else:
                if guess_number in answer_set:
                    print('Ответ Артёма: Да\n')
                    max_range_number = max_range_number.intersection(answer_set)
                    guessed_num_flag = True
                else:
                    print('Ответ Артёма: Нет\n')
                    max_range_number.difference_update(answer_set)

                if (len(max_range_number) == 1) and guessed_num_flag:
                    print('Артём загадал следующее число:', *max_range_number)
                    break
        break
