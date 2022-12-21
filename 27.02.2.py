import time


def timer(func, *args, **kwargs):

    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    run_time = end - start
    print('Время работы: {}'.format(run_time))

    return result


def hard_func():
    res = sum([x ** 2 ** x for x in range(14)])
    return res


my = timer(hard_func)

print(my)



