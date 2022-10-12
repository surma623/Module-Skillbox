
def calculate_factorial(num):

    if num == 1:
        return 1
    return num * calculate_factorial(num - 1)

number = int(input('Введите число: '))

factorial_num = calculate_factorial(number)

print(factorial_num)
