from abc import ABC, abstractmethod


class Figure(ABC):

    def __init__(self, pos_x, pos_y, length, width):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.length = length
        self.width = width

    @abstractmethod
    def move(self, pos_x: int, pos_y: int):
        self.pos_x = pos_x
        self.pos_y = pos_y


class ResizeMixin:

    def __init__(self):
        self.length = 0
        self.width = 0

    def resize(self, length, width):
        self.length = length
        self.width = width


class Rectangle(Figure, ResizeMixin):

    def move(self, pos_x: int, pos_y: int):
        super().move(pos_x, pos_y)


class Square(Figure, ResizeMixin):

    def __init__(self, pos_x: int, pos_y: int, size: int):
        super().__init__(pos_x, pos_y, size, size)

    def move(self, pos_x: int, pos_y: int):
        super().move(pos_x, pos_y)


k = Square(pos_x=2, pos_y=3, size=4)
p = Rectangle(pos_x=4, pos_y=5, length=7, width=4)

print(k.pos_x, k.pos_y)
k.move(4, 6)
print(k.pos_x, k.pos_y)

print(p.pos_x, p.pos_y)
p.move(9, 7)
print(p.pos_x, p.pos_y)

print(k.length, k.width)
l = k.length * 2
w = k.width * 2
k.resize(l, w)

print(k.length, k.width)

print(p.length, p.width)
l = p.length * 2
w = p.width * 2
p.resize(l, w)

print(p.length, p.width)


