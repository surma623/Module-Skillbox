
def is_prime(obj):

    result = list()

    if isinstance(obj, dict):
        obj = obj.items()

    for index, elem in enumerate(obj):
        flag = True
        divisor = 2
        if index > 1:
            while divisor < index:
                if index % divisor == 0:
                    flag = False
                    break
                divisor += 1

            if flag:
                result.append(elem)

    return result


def crypto(iterating_object):
    return is_prime(iterating_object)


print(crypto([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
print(crypto('О Дивный Новый мир!'))
