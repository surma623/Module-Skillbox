prices = [float(input("Цена на товар: ")) for _ in range(5)]

first_year = int(input("Повышение на первый год: "))
second_year = int(input("Повышение на второй год: "))

all_prices = "Сумма цен за каждый год: "
for percent in 0, first_year, second_year:
    prices = [price * (1 + percent / 100) for price in prices]
    all_prices += f" {round(sum(prices), 2)}"

print(all_prices)