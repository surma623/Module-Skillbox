import os

file_name = 'group_1.txt'
file_name_2 = 'group_2.txt'

file_abspath = os.path.abspath(os.path.join('task', file_name))
file_2_abspath = os.path.abspath(os.path.join('task', 'Additonal_info', file_name_2))

file = open(file_abspath, 'r', encoding='utf-8')
file_2 = open(file_2_abspath, 'r', encoding='utf-8')

summa = 0
diff = 0
compose = 1

for i_line in file:
    info = i_line.split()
    summa += int(info[2])
    diff -= int(info[2])

for i_line in file_2:
    info = i_line.split()
    compose *= int(info[2])

file.close()
file_2.close()

print(summa)

print(diff)

print(compose)

