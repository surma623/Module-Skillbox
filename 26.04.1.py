# def use_generation():
#
#     counter = 0
#
#     while True:
#         yield counter
#         counter += 1
#
#
# generation = use_generation()
#
# for num in generation:
#     print(num, end=' ')


def is_prime(max_numbers):

    counter = 2

    while counter <= max_numbers:
        num = counter
        flag = True
        divisor = 2
        if num > 1:
            while divisor < num:
                if num % divisor == 0:
                    flag = False
                    break
                divisor += 1

        if flag:
            counter += 1
            yield num
        else:
            counter += 1


primes = is_prime(50)

for i_elem in primes:

    print(i_elem, end=' ')