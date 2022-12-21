class Point:

    def __init__(self, x=0, y=0):
        self.set_x(x)
        self.set_y(y)

    def __str__(self):
        return 'Точка имеет следующие координаты: x = {}, y = {}'.format(
            self.__x,
            self.__y
        )

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def set_x(self, x):
        if isinstance(x, int):
            self.__x = x
        elif isinstance(x, float):
            self.__x = x
        else:
            raise ValueError('Х должен быть числом.')

    def set_y(self, y):
        if isinstance(y, int):
            self.__y = y
        elif isinstance(y, float):
            self.__y = y
        else:
            raise ValueError('Y должен быть числом.')



point_1 = Point(1, 'v')

print(point_1)
