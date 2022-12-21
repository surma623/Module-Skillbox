import random


class Toyota:
    color_of_car = 'red'
    price = 10 ** 6
    max_speed = 200
    current_speed = 0

    def display_info(self):
        print('Color of the car: {0}\nPrice of the car: {1}\nMaximum speed of the car: {2}\nCurrent'
              ' speed of the car: {3}'.format(self.color_of_car, self.price, self.max_speed, self.current_speed))

    def define_current_speed_a_car(self, cur_speed):
        self.current_speed = cur_speed
        print('\nCurrent speed of the car: {}'.format(self.current_speed))


first_car = Toyota()
first_car.display_info()
first_car.define_current_speed_a_car(random.randint(0, 200))
