def pow(a, n):
    if n == 0:
        return 1
    return pow(a, n - 1) * a


float_num = float(input('Введите вещественное число: '))

int_num = int(input('Введите степень числа: '))

print(float_num, '**', int_num, '=', pow(float_num, int_num))