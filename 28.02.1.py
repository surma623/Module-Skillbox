class Robot:

    def __init__(self, model: str):
        self.model = model

    def operate(self):
        print('Я робот')


class CanFly:

    __height = 0
    __speed = 0
    __straight = 0

    def get_height(self):
        return self.__height

    def get_speed(self):
        return self.__speed

    def get_straight(self):
        return self.__straight

    def fly_up(self):
        print('Робот взлетел')
        self.__height = 5
        self.__speed = 15
        print('Его текущая высота теперь равна {}, а скорость {}'.format(
            self.__height,
            self.__speed))

    def fly(self):
        self.__straight += 10
        print('Робот летит, он пролетел {} метров'.format(self.__straight))

    def land(self):
        self.__height -= 0
        self.__speed -= 0
        print('Робот приземлился, его высота = {}, скорость = {}'.format(
            self.__height,
            self.__speed
        ))


class IntelligenceDrone(Robot, CanFly):

    def operate(self):
        super().operate()
        print('Веду разведку с воздуха.')
        self.fly()


class MilitaryRobo(Robot, CanFly):

    def operate(self):
        super().operate()
        print('Охраняю военный объект с помощью оружия.')


robo_war = MilitaryRobo('sd2')
robo_intel = IntelligenceDrone('WW1')

print(robo_war.model)
robo_war.fly_up()
robo_war.fly()

print(robo_war.get_height())












