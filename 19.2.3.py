def get_hist(string):
    sym_dict = dict()

    for sym in string:
        if sym in sym_dict:
            sym_dict[sym] += 1
        else:
            sym_dict[sym] = 1
    return sym_dict


text = input('Введите текст: ')

hist = get_hist(text)

for i_sym in sorted(hist.items()):
    print(i_sym, ':', hist[i_sym])

print('Максимальная частота:', max(hist.values()))
