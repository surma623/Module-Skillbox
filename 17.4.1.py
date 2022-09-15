import random


original_prices = [random.randint(-15, 20) for _ in range(6)]

new_prices = original_prices[:]
new_prices = [new_prices[i_elem] * 0 if new_prices[i_elem] < 0 else new_prices[i_elem]
              for i_elem in range(len(new_prices))]

print("Мы потеряли: ",  abs(sum(original_prices) - sum(new_prices)))

