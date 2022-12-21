import os
import string


def get_list_strings(strings_lst, file_n):

    path = os.path.abspath(file_n)
    file = open(path, 'r')

    for i_line in file:
        strings_lst.append(i_line.lower())

    file.close()

    return strings_lst


def get_number_syms_and_rare_sym(lst):

    counter_sym = 0
    string_sym = ''

    for i_elem in lst:
        for sym in i_elem:
            if sym in alphabet:
                counter_sym += 1
                string_sym += sym

    sym_dict = dict()
    rare_sym = ''

    for sym in string_sym:
        if sym in sym_dict:
            sym_dict[sym] += 1
        else:
            sym_dict[sym] = 1
        if string_sym.index(sym) == 0:
            rare_sym = ''.join(sym)

    min_value = sym_dict[rare_sym]

    for key, values in sym_dict.items():
        if min_value > values:
            min_value = values
            rare_sym = key

    return counter_sym, rare_sym


def get_number_words(lst):

    counter_words = 0
    list_of_list_words = list()

    for i_elem in lst:
        list_of_list_words.append(i_elem.split())

    for i_list in list_of_list_words:
        counter_words += len(i_list)

    return counter_words


strings_list = list()

file_name = 'zen.txt'
alphabet = string.ascii_lowercase

list_zen = get_list_strings(strings_list, file_name)

number_sym, rare_symbol = get_number_syms_and_rare_sym(list_zen)

number_words = get_number_words(list_zen)


print('Количество букв в файле:', number_sym)
print('Количество слов в файле:', number_words)
print('Количество строк в файле:', len(list_zen))
print('Наиболее редкая буква:', *rare_symbol)

