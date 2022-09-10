original_prices = [1.25, -9.45, 10.22, 3.78, -5.92, 1.16]

nuw_list = [(i_elem if i_elem > 0 else 0) for i_elem in original_prices]

print(nuw_list)