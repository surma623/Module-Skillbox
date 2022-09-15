ip_address = "{0}.{1}.{2}.{3}"
number_list = []
count = 0

while count < 4:
    number = int(input('Введите число: '))
    if 0 <= number <= 255:
        number_list.append(number)
        count += 1
    else:
        print('Ошибка ввода. Попробуйте еще раз.')

print('IP-адрес:', ip_address.format(*number_list))

