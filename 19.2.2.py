incomes = {
    'apple': 5600.20,
    'orange': 3500.45,
    'banana': 5000.00,
    'bergamot': 3700.56,
    'durian': 5987.23,
    'grapefruit': 300.40,
    'peach': 10000.50,
    'pear': 1020.00,
    'persimmon': 310.00,
}

result_sum = 0
min_value = None
min_name = ""

for name, value in incomes.items():  # items() позволяет сразу обратиться и к ключам, и к значениям словаря
    result_sum += value
    if min_value is None or min_value > value:
        min_value = value
        min_name = name

incomes.pop(min_name)

print('Результат работы программы:')
print('Общий доход за год составил {} рублей'.format(result_sum))
print('Самый маленький доход у {0}. Он составляет {1} рублей'.format(min_name, min_value))
print(incomes)