

def func_2(f, number):
    result = f(number) + f(number)

    return result


def func_1(x):
    return x + 10


f_1 = func_1


print(func_2(func_1, 10))
