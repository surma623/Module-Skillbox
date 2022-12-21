class CanFly:

    def __init__(self, height=0, speed=0):
        self.height = height
        self.speed = speed

    def take_off(self):
        pass

    def fly(self):
        pass

    def land(self):
        self.height = 0
        self.speed = 0

    def __str__(self):
        return '{} высота {} скорость {}'.format(
            self.__class__.__name__, self.height, self.speed,
        )


class Butterfly(CanFly):

    def __init__(self, height=0, speed=0):
        super().__init__(height, speed)

    def take_off(self):
        self.height = 1
        self.speed = 0.5
        print('Бабочка взлетела: высота - {}, скорость - {}'.format(self.height, self.speed))

    def fly(self):
        self.speed = 0.5
        print('Бабочка летит, скорость - {}'.format(self.speed))


class Rocket(CanFly):

    def __init__(self, height=0, speed=0):
        super().__init__(height, speed)

    def take_off(self):
        height_rocket = 500
        speed_rocket = 1000
        print('Ракета взлетела: высота - {}, скорость - {}'.format(height_rocket, speed_rocket))

    def land(self):
        height_rocket = 0
        print('Ракета приземлилась: высота - {}, ракета взорвалась'.format(height_rocket))

    def blow_up(self):
        print('Буууууууммммм!!!!')


butterfly = Butterfly()
rocket = Rocket()

butterfly.take_off()
butterfly.fly()



