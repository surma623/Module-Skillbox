import random


def make_fight(warrior_1, warrior_2):
    while warrior_1.health > 0 and warrior_2.health > 0:

        if warrior_1.has_attack():
            warrior_2.health -= 20
            print('Атаковал 1 юнит, у юнита 2 осталось {} очков здоровья'.format(warrior_2.health))
        else:
            warrior_1.health -= 20
            print('Атаковал 2 юнит, у юнита 1 осталось {} очков здоровья'.format(warrior_1.health))

    if warrior_1.health > warrior_2.health:
        print('Победил 1 юнит.')
    else:
        print('Победил 2 юнит.')


class Warrior:
    health = 100
    number_of_first_attack = 1

    def has_attack(self):

        if random.randint(1, 2) == self.number_of_first_attack:
            return True
        else:
            return False


first_warrior = Warrior()
second_warrior = Warrior()

make_fight(first_warrior, second_warrior)
