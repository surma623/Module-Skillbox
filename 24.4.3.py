class Potato:
    stages = {0: 'Отсутствует', 1: 'Росток', 2: 'Зеленая', 3: 'Зрелая'}

    def __init__(self, index):
        self.index = index
        self.stage = 0

    def grow(self):
        if self.stage < 3:
            self.stage += 1
        self.print_stage()

    def is_ripe(self):
        if self.stage == 3:
            return True
        return False

    def print_stage(self):
        print('Картошка {} сейчас в стадии {}'.format(
            self.index,
            Potato.stages[self.stage]
        ))


class PotatoGarden:

    def __init__(self, count):
        self.potatoes = [Potato(index) for index in range(1, count + 1)]

    def grow_all(self):
        print('Картошка прорастает!')
        for i_potato in self.potatoes:
            i_potato.grow()

    def are_all_ripe(self):
        if not all([i_potato.is_ripe() for i_potato in self.potatoes]):
            print('Картошка еще не созрела!\n')
        else:
            print('Вся картошка созрела. Можно собирать!\n')


my_garden = PotatoGarden(5)

for _ in range(2):
    my_garden.grow_all()

my_garden.are_all_ripe()