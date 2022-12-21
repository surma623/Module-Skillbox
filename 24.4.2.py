
class Point:
    counter_of_points = [0]

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.counter_of_points[0] += 1

    def display_info(self):
        print('Координаты точки {}: x = {}, y = {}\nКоличество точек: {}'.format(
            *self.counter_of_points,
            self.x,
            self.y,
            *self.counter_of_points))


point_1 = Point()
point_1.display_info()
point_2 = Point(2, 3)
point_2.display_info()
