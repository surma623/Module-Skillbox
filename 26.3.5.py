class Primes:

    def __init__(self, max_number):
        self.max_number = max_number
        self.counter = 2

    def __iter__(self):
        self.counter = 2
        return self

    def __next__(self):

        while self.counter <= self.max_number:
            num = self.counter
            flag = True
            divisor = 2
            if num > 1:
                while divisor < num:
                    if num % divisor == 0:
                        flag = False
                        break
                    divisor += 1

            if flag:
                self.counter += 1
                return num
            else:
                self.counter += 1

        raise StopIteration


prime_nums = Primes(50)

for i_elem in prime_nums:

    print(i_elem, end=' ')
