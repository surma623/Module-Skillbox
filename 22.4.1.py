import os

file_name = 'numbers.txt'
file_path = os.path.abspath(file_name)
file = open(file_path, 'r')
summ = 0


for i_line in file:
    summ += int(i_line)

file.close()

file_result = open(' answer.txt', 'w')
file_result.write(str(summ))
file_result.close()
