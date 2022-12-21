import random

class MyIter:

    def __init__(self, limit):
        self.__limit = limit
        self.__counter = 0
        self.__last = random.random()

    def __iter__(self):
        self.__counter = 0
        self.__last = random.random()
        return self

    def __next__(self):
        if self.__counter < self.__limit:
            self.__last += random.random()
            self.__counter += 1
            return round(self.__last, 2)
        else:
            raise StopIteration


number_elem = int(input('Кол-во элементов: '))

my_iter = MyIter(limit=number_elem)

print('Элементы итератора:')

for i_elem in my_iter:
    print(i_elem)




