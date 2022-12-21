class Unit:
    def __init__(self, health_point, basic_damage=0):
        self.__health_point = health_point
        self.__basic_damage = basic_damage

    def get_health_point(self):
        return self.__health_point

    def get_basic_damage(self):
        return self.__basic_damage



class Soldier(Unit):

    def __init__(self, health_point, basic_damage=0):
        super().__init__(health_point, basic_damage)

    def info(self):
        hp_soldier = self.get_health_point() - self.get_basic_damage()
        return 'Количество очков здоровья солдата - {}'.format(hp_soldier)


class Citizen(Unit):

    def __init__(self, health_point, basic_damage=0):
        super().__init__(health_point, basic_damage)

    def change_damage(self):
        return 2 * self.get_basic_damage()

    def info(self):
        hp_citizen = self.get_health_point() - self.change_damage()
        return 'Количество очков здоровья солдата - {}'.format(hp_citizen)


soldier = Soldier(health_point=100, basic_damage=2)
citizen = Citizen(health_point=100, basic_damage=2)
print(soldier.info())
print(citizen.info())