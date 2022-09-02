num_employees = int(input('Введите количество сотрудников: '))
employees_list= []

for num_empl in range(num_employees):
    salary = int(input(f'Зарплата {num_empl + 1} сотрудника: '))
    employees_list.append(salary)

for sal in employees_list:
    if sal == 0:
        employees_list.remove(sal)

print('Осталось сотрудников', len(employees_list))
print('Зарплата: ', employees_list)

print('Максимальная зп:', max(employees_list))
print('Минимальная зп:', min(employees_list))
