class Ship:
    def __init__(self, model):
        self.__model = model

    def __str__(self):
        return '\n Модель корабля {}'.format(self.__model)

    def float(self):
        print('Корабль модель {} поплыл куда-то'.format(self.__model))


class WarShip(Ship):

    def __init__(self, model, gun):
        super().__init__(model)
        self.gun = gun

    def attack(self):
        print('Корабль атаковал с помощью своего оружия - {}'.format(self.gun))


class TradingShip(Ship):

    def __init__(self, model):
        super().__init__(model)
        self.tonnage = 0

    def load(self):
        print('На корабль загрузили товары.')
        self.tonnage += 1
        print('Текущая загруженность корабля составляет {}'.format(self.tonnage))

    def unload(self):
        if self.tonnage > 0:
            print('С корабля разгрузили товары.')
            self.tonnage -= 1
            print('Текущая загруженность корабля составляет {}'.format(self.tonnage))
        else:
            print('Нет товаров для разгрузки.')


warship = WarShip('aas2', 'пушки')
trade_ship = TradingShip('aawd3')

warship.attack()
trade_ship.unload()
print(warship)

