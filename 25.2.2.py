class Human:
    __count = 0

    def __init__(self, name, age):
        self.__name = ''
        self.__age = 0
        self.set_name(name)
        self.set_age(age)
        Human.__count += 1

    def __str__(self):
        return 'Имя человека {}, его возраст {}.\nКоличество человек {}'.format(
            self.__name,
            self.__age,
            Human.__count
        )

    def get_name(self):
        return self.__name

    def get_age(self):
        return self.__age

    def get_count(self):
        return self.__count

    def set_name(self, name):
        if not isinstance(name, str) and not name.isalpha():
            raise ValueError('Имя должно состоять только из букв.')
        else:
            self.__name = name

    def set_age(self, age):
        if isinstance(age, int) and age in range(0, 100):
            self.__age = age
        else:
            raise ValueError('Недопустимый возраст')


person_1 = Human('Artem', 99)
person_2 = Human('Misha', 70)
print(person_1)



