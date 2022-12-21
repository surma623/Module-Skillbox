from abc import ABC, abstractmethod
from typing import Any

class Transport (ABC):

    def __init__(self, colour: str, speed: int) -> None:
        self._colour = colour
        self._speed = speed

    @property
    def colour(self) -> str:
        return self._colour

    @colour.setter
    def colour(self, colour) -> None:
        if isinstance(colour, str):
            self._colour = colour

        else:
            raise BaseException('Не тот цвет')

    @property
    def speed(self) -> int:
        return self._speed

    @speed.setter
    def speed(self, speed):
        if 0 < speed < 100:
            self._speed = speed
        else:
            raise BaseException('Ошибка скорости')

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def honk(self):
        pass


class MusicMixin:

    def play_music(self) -> None:
        print('В Амфибии заиграл GreenDay')


class Cars(Transport):

    def __init__(self, colour: str, speed: int) -> None:
        super().__init__(colour, speed)
        self.horn = 'гудок'

    def honk(self) -> None:
        print('Машина подал сигнал через {}'.format(self.horn))

    def move(self) -> None:
        print('Машина поехал по земле со скоростью {}'.format(self._speed))


class Boats(Transport):

    def __init__(self, colour, speed):
        super().__init__(colour, speed)
        self.bell = 'колокол'

    def honk(self) -> None:
        print('Лодка подала сигнал через {}'.format(self.bell))

    def move(self) -> None:
        print('Лодка поплыла по воде со скорость {}'.format(self._speed))


class Amphibia(Transport, MusicMixin):
    def __init__(self, colour: str, speed: int) -> None:
        super().__init__(colour, speed)
        self.siren = 'сирена'

    def honk(self) -> None:
        print('Амфибия подала сигнал через {}'.format(self.siren))

    def move(self) -> None:
        print('Амфибия поплыла или поехала по земле со скорость {}'.format(self._speed))


car = Cars('red', 21)
boat = Boats('Green', 10)
amf = Amphibia('orange', 3)

amf.honk()
amf.move()
amf.play_music()
print(amf.speed)
print(amf.colour)
amf.speed = 99
print(amf.speed)


boat.move()
boat.honk()
print(boat.colour)
print(boat.speed)



car.honk()
car.move()
print(car.speed)
print(car.colour)

car.colour = 3

print(car.colour)

