student_str = input(
    'Введите данные о студенте через пробел \n'
    '(имя, фамилия, город, место учебы, оценки): '
)

student_info = student_str.split()
student = dict()

student['Имя'] = student_info[0]
student['Фамилия'] = student_info[1]
student['Город'] = student_info[2]
student['Место учебы'] = student_info[3]
student['Оценки'] = [grate for grate in student_info[4:]]


student['Оценки'] = ' '.join(student['Оценки'])

for i_info in student:
    print(i_info, '-', student[i_info])
