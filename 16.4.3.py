goods = [["яблоки", 50], ["апельсины", 190], ["груши", 100], ["нектарины", 200], ["бананы", 77]]

fruit_name = input('Введите название фрукта: ')
price = int(input('Введите цену данного фрукта: '))

goods.append([fruit_name, price])
print('Новый ассортимент:', goods)

# new_price_goods = []
# new_price_goods.extend(goods)

#for list_in_main in range(len(new_price_goods)):
    #for i_list in range(2):
        #if i_list == 1:
            #new_price_goods[list_in_main][i_list] += new_price_goods[list_in_main][i_list] * (8 / 100)

for good in goods:
    good[1] += good[1] * 8 / 100

print('\nНовый ассортимент с увел. ценой:', goods)
