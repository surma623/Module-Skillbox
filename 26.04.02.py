def calculate_generation(file):

    with open(file, 'r') as file_result:
        for i_line in file_result:
            yield i_line


file_name = 'numbers2.txt'
counter = 0

lines = calculate_generation(file_name)

for i_digits in lines:
    for i_digit in i_digits:
        if i_digit.isdigit():
            counter += 1

print(counter)