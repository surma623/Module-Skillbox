import random

squad_1 = [random.randint(50, 80) for _ in range(10)]
squad_2 = [random.randint(30, 60) for _ in range(10)]

squad_3_condition = [('Выжил' if squad_1[i_elem] + squad_2[i_elem] < 100 else 'Погиб')
                     for i_elem in range(10)]

print(squad_1)
print(squad_2)
print(squad_3_condition)
