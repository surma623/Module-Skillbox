
class Person:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return 'Имя: {}, возраст: {}'.format(self.__name, self.__age)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if isinstance(name, str):
            self.__name = name
        else:
            raise BaseException('Имя должно быть строкой')

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, age):
        if isinstance(age, str):
            self.__age = age
        else:
            raise 'Возраст должен быть строкой'




p_1 = Person(name= 'Mike', age='70')
p_2 = Person(name= 'Mik', age='60')
p_3 = Person(name= 'ike', age='40')

print(p_1)
lst = [p_1, p_2, p_3]
print(lst)

result = sorted(lst, reverse=False, key=lambda elem: int(elem.age))

for p in result:
    print(p)