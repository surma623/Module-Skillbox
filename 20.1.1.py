import random

first_tuple = list()
second_tuple = list()

for _ in range(10):
    first_tuple.append(random.randint(0, 5))
    second_tuple.append(random.randint(-5, 0))

third_tuple = tuple(first_tuple) + tuple(second_tuple)

print('Третий кортеж:', third_tuple)
print('Количество нулей в третьем кортеже:', third_tuple.count(0))


# import random
#
# def create_random_tuple(a, b, n):
#     return tuple([random.randint(a, b) for _ in range(n)])
#
#
# first = create_random_tuple(0, 5, 10)
# second = create_random_tuple(-5, 0, 10)
# third = first + second
# nulls_count = third.count(0)
# print(third, nulls_count)
