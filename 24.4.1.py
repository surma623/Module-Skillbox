import random


class Toyota:

    def __init__(self, color, price, max_speed, current_speed):
        self.color_of_car = color
        self.price = price
        self.max_speed = max_speed
        self.current_speed = current_speed

    def display_info(self):
        print('Color of the car: {0}\nPrice of the car: {1}\nMaximum speed of the car: {2}\nCurrent'
              ' speed of the car: {3}'.format(self.color_of_car, self.price, self.max_speed, self.current_speed))

    def define_current_speed_a_car(self, cur_speed):
        self.current_speed = cur_speed
        print('\nCurrent speed of the car: {}'.format(self.current_speed))


first_car = Toyota('red', 10 ** 6, 200, 0)

first_car.display_info()
first_car.define_current_speed_a_car(random.randint(0, 200))

