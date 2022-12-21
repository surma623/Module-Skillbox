class Robot:

    def __init__(self, number_model):
        self.__number_model = number_model

    def __str__(self):
        return '\n Модель робота - {}'.format(self.__number_model)

    def operate(self):
        print('Робот ездит по кругу')


class VacuumCleanerRobo(Robot):

    def __init__(self, number_model):
        super().__init__(number_model)
        self.bag_for_rubbish = 0

    def operate(self):
        self.bag_for_rubbish += 1
        print('Робот пылесосит пол. Значение заполненности мешка для мусора = {}'.format(self.bag_for_rubbish))


class WarRobo(Robot):

    def __init__(self, number_model, gun):
        super().__init__(number_model)
        self.gun = gun

    def operate(self):
        print('Робот охраняет военный объект с помощью оружия - {}'.format(self.gun))


class SubmarineRobo(Robot):
    def __init__(self, number_model, depth):
        super().__init__(number_model)
        self.depth = depth

    def operate(self):
        print('Робот охраняет военный объект на глубине - {}'.format(self.depth))


robo_1 = VacuumCleanerRobo('111')
robo_2 = WarRobo('123', 'пулемет')
robo_3 = SubmarineRobo('344', 3)

robo_1.operate()
robo_2.operate()
robo_3.operate()
