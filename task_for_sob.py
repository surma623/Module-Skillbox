
def sum_digit(num):

    sum_num = 0

    if num < 0:
        num = abs(num)
    else:
        while num != 0:
            sum_num += num % 10
            num //= 10

    return sum_num




number = int(input('Введите число: '))



print(sum_digit(number))
