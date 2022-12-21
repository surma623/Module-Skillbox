import random


class Toyota:
    color_of_car = 'red'
    price = 1000000
    max_speed = 200
    current_speed = 0


random_speed_1 = Toyota()
random_speed_1.current_speed = random.randint(0, 200)
random_speed_2 = Toyota()
random_speed_2.current_speed = random.randint(0, 200)
random_speed_3 = Toyota()
random_speed_3.current_speed = random.randint(0, 200)


print(random_speed_1.current_speed)
print(random_speed_2.current_speed)
print(random_speed_3.current_speed)