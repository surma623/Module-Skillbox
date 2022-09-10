def get_rise_price(percent, price):
    return round(price * (1 + percent / 100), 2)


price = [1.09, 23.56, 57.84, 4.56, 6.78]

first_percent = int(input('Повышение на первый год: '))
second_percent = int(input('Повышение на второй год: '))


price_list_f = [get_rise_price(first_percent, i_price) for i_price in price]
price_list_s = [get_rise_price(second_percent, i_price) for i_price in price_list_f]


print('Сумма цен за каждый год:', round(sum(price), 2), round(sum(price_list_f), 2), round(sum(price_list_s), 2))